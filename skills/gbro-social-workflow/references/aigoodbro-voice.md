# AiGoodBro 品牌配音

AiGoodBro 配音**强制使用用户已确认的 G4「轻快伙伴」纯克隆声音**，除非用户明确要求换声线。以 [accepted-sample.wav](../assets/voice/aigoodbro-g4/accepted-sample.wav) 对照音色、语气、连贯度及英文读法；不能只因模型名、seed 或参数一致就宣称声音已匹配。其他品牌和已有原声按当前任务处理。

固定克隆输入仍是原始 G4 干声 [reference.wav](../assets/voice/aigoodbro-g4/reference.wav)，SHA-256 为 `3b08420d43718ae1a2e4dbbec833e4b2803f0f20394b1c7619ecc89c46a6aa21`。[原始样音试听](../assets/voice/aigoodbro-g4/sample.wav) 仅做恒定音量调整；已接受的整段样音 SHA-256 为 `ca4292b25007136a8d277692f4ff9638da174a9672877b199cb9bdc634b79c86`，只作听感标准，不替换克隆输入。准确参考文字、实际参数和样音文本见 [profile.json](../assets/voice/aigoodbro-g4/profile.json)。

## 生成

- 模型固定为 `mlx-community/Breeze-TTS-2-mlx-4bit`，revision `3a06d26b172ea4ae1da2f42d708383e9c79d5526`，使用 MLX-Audio 0.6.1、MLX 0.32.4。样音是参考，不是独立训练模型；模型获取与校验见仓库 `runtime/voice/README.md`。
- 必须使用纯克隆路线 `voice_clone_without_direction`：显式传入原始 `ref_audio`、逐字对应的 `ref_text`，并令 `instruction=""`。不得省略该字段后沿用服务默认值，也不得加入原始声音设计描述、语速、情绪、连读或其他风格指令。`source_voice_design_instruction` 只作来源追溯，不能用于配音。
- 固定 `seed=1447`、`temperature=0.8`、`repetition_penalty=1.1`、`top_p=1.0`、`top_k=50`、`sample_rate=24000`、`pronunciation=off`。`cfg_scale=4` 保留实际调用值；当前本机模型在空指令时不启用 CFG，回执必须记录 `effective_cfg=null`，不能声称 CFG 在控制声音。
- `split_pattern=None`、`stream=False`，一次输入完整正文及片尾，回执须为 `chunk_count=1`、`reused_audio_segments=0`。任意一处音色、语气、读法或停顿有问题，都从完整稿重新配整段；不得补一句、拼接旧段、保留旧片尾或剪掉停顿冒充重配。只有用户明确要求局部处理时例外。
- 复用已有可用安装。服务忙时等待，不重启抢占；缺少参考、模型或可用入口时只暂停依赖步骤，不静默换模型、参考音、声线或付费服务。不能自动把新作品、片尾或未接受候选升级为品牌参考或标准样音。
- 当前正文已经获准且配音被用户明确接受时，视频直接使用该完整音频文件及哈希，不为合成视频再次随机生成。混音放后期，保持原声音高与速度。
- AiGoodBro 为完整名称，字幕和 canonical 文本精确写 `AiGoodBro`。英文、数字、否定词及品牌读法按实际音频核对；必要修正只改新生成正文，不能改参考转写或添加风格指令。

## 验收与许可

每次新输出对照已接受样音，检查开头、中段和片尾的声线及连贯度；检查完整解码、非静音、削波、正文完整和画面同步。ASR 与哈希是辅助证据，不能代替听感和用户接受；当前已确认样音不自动代表以后每次生成都合格。保留原始参考、已接受完整干声和参数，新候选另存作品目录；不能用含 BGM 的成片作克隆参考。

随包样音、模型及输出受 BreezeBlue 研究与非商业许可证约束，仓库 MIT 只覆盖自有代码与说明。模型权重不直接放在公开 Git 或 Release；使用者须先阅读并接受完整许可，再从固定上游获取。本地已安装模型仍须核版本与文件哈希。没有额外授权不宣称可商用，也不复制用户的其他声音、私人路径或服务记录到公共包。
