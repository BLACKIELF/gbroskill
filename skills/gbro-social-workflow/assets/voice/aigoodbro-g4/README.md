# AiGoodBro G4 声音样本

AiGoodBro 配音强制沿用用户已确认的 G4 纯克隆声音，除非用户明确要求换声线。`reference.wav` 是固定克隆输入，8.32 秒、24 kHz、单声道，SHA-256 为 `3b08420d43718ae1a2e4dbbec833e4b2803f0f20394b1c7619ecc89c46a6aa21`；`sample.wav` 是该原始样本仅做恒定音量调整的试听版。

`accepted-sample.wav` 是用户已接受的 67.36 秒完整纯克隆口播，用来对照实际音色、语气、连贯度及英文读法；不得把它再当克隆参考替换 `reference.wav`。其 SHA-256 为 `ca4292b25007136a8d277692f4ff9638da174a9672877b199cb9bdc634b79c86`。准确文本、参数与全部样本哈希见 `profile.json`。

执行时 `instruction` 必须显式为空，不叠加原始声线描述、语速、情绪或连读指令。`source_voice_design_instruction` 只记原始样音的来源，不能传入生成。所有口播一次生成完整正文与片尾，出现一处问题即整段重配；只有用户明确要求局部处理时例外。新输出或未验收候选不能自动覆盖已定标准。

样音由 Breeze TTS 2 MLX 4bit 生成，作为非商业研究与复现示例分享。模型和输出受随附 LICENSE 约束，不受仓库根目录 MIT 许可替代；商业使用需要权利人的单独授权。不授予商标、真人身份或其他素材权益。

Derived from Breeze TTS 2 by BreezeBlue and licensed for research and non-commercial use only.
