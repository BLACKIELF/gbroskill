# AiGoodBro 配音复现

强制使用用户已接受的 G4 纯克隆路线与固定原始干声参考，除非用户明确要求换声线。`accepted-sample.wav` 是已确认的完整听感标准，`reference.wav` 仍是唯一克隆输入。固定模型版本、完整文件大小与 SHA-256 在 `model.json`，样音、参考准确文字与参数在 `skills/gbro-social-workflow/assets/voice/aigoodbro-g4/`。这不是训练出的 AiGoodBro 专用模型。

Derived from Breeze TTS 2 by BreezeBlue and licensed for research and non-commercial use only.

模型及输出受 [完整许可](LICENSE) 和 [NOTICE](NOTICE) 约束，不是 MIT 或可自由商用的模型。许可要求每位接收者在访问前独立接受协议，因此本公开仓库不直接镜像权重；获取脚本在接受许可前不下载。当前上游模型：[MLX 4bit 固定版本](https://huggingface.co/mlx-community/Breeze-TTS-2-mlx-4bit/tree/3a06d26b172ea4ae1da2f42d708383e9c79d5526)。完整模型约 3.04 GB；上游 MLX 转换不属于官方 BreezeBlue 发布。

先按[云端接手说明](../../docs/CLOUD-HANDOFF.md)确认环境。当前实际生成只接受 Apple Silicon Mac、Python 3.12、固定依赖和可用 Metal；Linux／Windows 没有随包已验证的同声音生成路线，不能自动换 TTS。

只读预检（未给模型或未就绪退出码为 2，独立材料工作继续）：

```bash
python3 runtime/voice/preflight.py
python runtime/voice/preflight.py --model /path/to/model
```

先复用并验证现有安装：

```bash
python3 runtime/voice/download_model.py --destination /path/to/model --check-only
```

首次获取时先阅读许可，自行确认接受后运行：

```bash
python3 runtime/voice/download_model.py --destination ./models/aigoodbro-voice-base --accept-license
```

脚本校验所有文件，遇到已有内容不同或不完整下载会停止，不覆盖现有模型。当前依赖在 Apple Silicon Mac / Python 3.12 上使用；MLX 版本见 `requirements.txt`，不声明 Windows CPU 或其他 GPU 已验证。用户需要新环境时自行建立独立环境，安装固定依赖，不覆盖已有环境。

准备完整 UTF-8 文本文件后先检查稿件配置，再生成无 BGM 的 WAV 和参数回执；`--dry-run` 只检查配置与输入，不证明运行环境可生成：

```bash
python runtime/voice/generate.py --model /path/to/model --text-file narration.txt --output speech.wav --dry-run
python runtime/voice/generate.py --model /path/to/model --text-file narration.txt --output speech.wav
```

生成器在调用模型前检查已接受配置：`instruction=""`、原始参考及参考文字、`seed=1447`、`temperature=0.8`、`repetition_penalty=1.1`、`top_p=1.0`、`top_k=50`、24 kHz。发生配置漂移即退出，不调用模型。`cfg_scale=4` 保留原调用值；空指令下本机模型不应用 CFG，回执记为 `effective_cfg=null`。原始声音设计指令仅作来源记录，不能用于当前配音。

默认把完整 UTF-8 口播稿作为一次生成输入，关闭按换行与句子拆段。任意一处出现声音问题时都重新生成全文（包括片尾），不会拼接旧音频。

实际生成前再次检查平台、依赖版本、Metal、声音资产和完整模型哈希，缺项时在调用模型前退出。实际生成离线运行，不下载模型、不调用付费 API。相同参考与种子不能保证任意正文的人耳听感完全一致；逐段对照样音，优先检查开头、中段、结尾与关键数字。字幕、混音和最终视频在作品工程中制作。新输出仍需听感验收，不能仅凭配置相同宣布声音一致。已经被用户接受的完整干声直接用于后期，不为合成视频重新随机生成。
