#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate dry AiGoodBro speech with the bundled, hash-pinned voice reference."""
import argparse,hashlib,json,math,os,wave
from pathlib import Path
BASE=Path(__file__).resolve().parent
VOICE=BASE.parents[1]/'skills/gbro-social-workflow/assets/voice/aigoodbro-g4'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',required=True,type=Path);p.add_argument('--text-file',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path);p.add_argument('--dry-run',action='store_true')
    a=p.parse_args();profile=json.loads((VOICE/'profile.json').read_text())
    ref=VOICE/profile['reference_audio'];reference_hash=hashlib.sha256(ref.read_bytes()).hexdigest()
    if reference_hash!=profile['reference_sha256']:raise SystemExit('Reference hash mismatch')
    text=a.text_file.read_text().strip();parts=[text] if text else []
    if not parts:raise SystemExit('Empty text')
    if not (a.model/'model.safetensors').is_file():raise SystemExit('Model missing; use download_model.py or verify the existing model.')
    receipt=a.output.with_suffix('.json')
    if a.output.exists() or receipt.exists():raise SystemExit('Output exists; choose a new version.')
    if a.dry_run:
        print(json.dumps({'chunks':len(parts),'reference_sha256':reference_hash,'text':text,'model_revision':json.loads((BASE/'model.json').read_text())['revision'],'generated':False},ensure_ascii=False));return
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TOKENIZERS_PARALLELISM']='false'
    import numpy as np
    from mlx_audio.tts import load
    model=load(str(a.model));audio=[];tokens=[]
    for i,part in enumerate(parts):
        budget=min(12000,max(750,math.ceil(len(part)*8.5)))
        for result in model.generate(text=part,instruct=profile['instruction'],ref_audio=str(ref),ref_text=profile['reference_text'],cfg_scale=profile['cfg_scale'],seed=profile['seed'],temperature=profile['temperature'],repetition_penalty=profile['repetition_penalty'],max_tokens=budget,stream=False,split_pattern=None):
            if result.token_count>=budget:raise SystemExit('Generation budget reached; audio not saved. Retry the entire narration with an adequate budget; do not splice a partial replacement.')
            if result.sample_rate!=profile['sample_rate']:raise SystemExit('Unexpected sample rate')
            data=np.asarray(result.audio,dtype=np.float32).reshape(-1)
            if not data.size or not np.isfinite(data).all():raise SystemExit('Invalid audio')
            audio.append(data);tokens.append(int(result.token_count))
        if i+1<len(parts):audio.append(np.zeros(round(profile['sample_rate']*.18),dtype=np.float32))
    if len(tokens)!=1:raise SystemExit('Expected one continuous generation; audio not saved')
    pcm=np.concatenate(audio)
    if abs(pcm).max()<.0001:raise SystemExit('Silent audio')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('xb') as raw:
        with wave.open(raw,'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(profile['sample_rate']);w.writeframes((np.clip(pcm,-1,1)*32767).astype('<i2').tobytes())
    record={'text':text,'seconds':len(pcm)/profile['sample_rate'],'reference_sha256':reference_hash,'model_revision':json.loads((BASE/'model.json').read_text())['revision'],'profile':profile,'token_counts':tokens,'chunk_count':len(tokens),'generation_mode':'whole_narration','reused_audio_segments':0,'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'listening_acceptance':'pending'}
    receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'seconds':record['seconds'],'sha256':record['sha256'],'output':str(a.output)}))
if __name__=='__main__':main()
