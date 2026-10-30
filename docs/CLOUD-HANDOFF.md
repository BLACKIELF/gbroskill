# 云端接手 GBro

云端从完整仓库或 Release 解压目录开始，先读 [主 Skill](../skills/gbro-social-workflow/SKILL.md) 和[随 Skill 的接手规则](../skills/gbro-social-workflow/references/cloud-handoff.md)。只安装 Skill 不会带上仓库根的 `runtime/voice/`，需要配音时必须保留完整仓库结构。

## 当前可执行范围

| 工作 | 条件与边界 |
|---|---|
| 稿件、来源对账、分平台正文、分镜与排版源 | 可在有 Python 3 的云端准备；来源网页、截图与品牌资产仍要真实提供和检查 |
| 9:16 视频与封面渲染、已有干声混音 | 目标环境需具备 FFmpeg／ffprobe、所选渲染器、WebGL 2 和已授权固定字体；逐项实测后才算可用。仓库包含模板，不内置云端渲染服务 |
| 新生成指定 G4 配音 | 当前只在 Apple Silicon Mac、Python 3.12、MLX 0.32.4、MLX-Audio 0.6.1、NumPy 2.5.4 与可用 Metal 上实测；按固定模型和参考执行 |
| 普通 Linux／Windows 云主机生成 G4 | 本包没有已验证的同声线生成路线。不得自动换 TTS、模型、参考音、声线或把其他引擎宣称为同一声音 |
| 发布、飞书交付 | 目标环境自己的已授权账号、接收方和可用入口；安装包不携带登录态，也不自动授予发布权限 |

模型文件可以在有 Python 的环境做下载与哈希核对；文件下载成功不证明该主机可生成声音。下面的预检不安装依赖、不下载、不生成声音、不修改文件或读取账号凭据。

```bash
python3 scripts/verify_bundle.py
python3 runtime/voice/preflight.py
```

未指定现有模型或环境不匹配时，第二条退出码为 `2`，JSON 的 `voice.can_generate` 为 `false`；其他能独立完成的文字、截图和排版工作继续。媒体工具、字体、浏览器渲染和实际播放分别验收，预检不代替成片审阅。

## 声音资料与模型

以下资料在仓库和 Release 中都有实际文件，可从链接单独获取；三个音频的作用不同：

- [reference.wav](../skills/gbro-social-workflow/assets/voice/aigoodbro-g4/reference.wav)：原始 G4 克隆输入，SHA-256 `3b08420d43718ae1a2e4dbbec833e4b2803f0f20394b1c7619ecc89c46a6aa21`。
- [sample.wav](../skills/gbro-social-workflow/assets/voice/aigoodbro-g4/sample.wav)：原始声音的试听版，仅恒定音量处理，不替换克隆输入。
- [accepted-sample.wav](../skills/gbro-social-workflow/assets/voice/aigoodbro-g4/accepted-sample.wav)：用户已接受的完整听感标准，SHA-256 `ca4292b25007136a8d277692f4ff9638da174a9672877b199cb9bdc634b79c86`；样音中的新闻正文和片尾不是新任务的默认稿。
- [profile.json](../skills/gbro-social-workflow/assets/voice/aigoodbro-g4/profile.json)：准确中文参考转写、固定参数及样音哈希。
- [model.json](../runtime/voice/model.json)：`mlx-community/Breeze-TTS-2-mlx-4bit` 的固定 revision `3a06d26b172ea4ae1da2f42d708383e9c79d5526`，14 个文件的大小与 SHA-256。

模型约 3.04 GB，不在 GitHub 附件内镜像。先阅读 [模型许可](../runtime/voice/LICENSE) 和 [NOTICE](../runtime/voice/NOTICE)；研究与非商业限制覆盖模型及相关输出，仓库 MIT 不替代该许可。只有接收者独立接受后，才可显式运行获取脚本；已有模型先只读校验。

```bash
python3 runtime/voice/download_model.py --destination ./models/aigoodbro-voice-base --check-only
```

首次获取且已接受许可时：

```bash
python3 runtime/voice/download_model.py --destination ./models/aigoodbro-voice-base --accept-license
```

在已确认的 Apple Silicon 环境、使用固定依赖的 Python 中执行：

```bash
python runtime/voice/preflight.py --model ./models/aigoodbro-voice-base
python runtime/voice/generate.py --model ./models/aigoodbro-voice-base --text-file narration.txt --output speech.wav --dry-run
python runtime/voice/generate.py --model ./models/aigoodbro-voice-base --text-file narration.txt --output speech.wav
```

`--dry-run` 只核配置和完整文本，不证明运行环境可生成。实际生成会再次检查平台、固定依赖、Metal、声音资产和模型逐文件哈希，未就绪即停止，绝不自动换引擎。保留输出 WAV 与同名 JSON 回执，试听开头、中段、片尾及英文、数字和否定词；技术通过不等于用户接受。

## Linux 云端与配音端协作

1. 云端准备完整 UTF-8 口播稿，附本篇已确认片头、正文和片尾及文本哈希。中文和英文分别完整交接；已确认内容不得擅自改写。
2. 新配音需要上述已验证的 Apple Silicon 执行端，使用同一仓库、原始参考和固定参数。只传本篇必要稿件和素材；不自动部署代理、暴露本机端口、复制凭据或新增付费服务。
3. 配音端一次生成完整正文与片尾，交回原始干声、生成回执、稿件和 SHA-256。英文只改变待配正文，原始参考及中文 `ref_text` 逐字不动。
4. 云端核对音频哈希、稿件和验收状态后合成，保留原速度与音高。如果已有本篇已接受的完整干声，直接复用，不为换画幅再次生成；没有可用干声时先完成独立材料，并明确配音待交接。
5. 任一处声音、语气、读法或停顿有问题，重新配完整稿，包括片尾；不能补一句、拼旧段。用户明确要求局部处理才例外。新候选不自动替换 `reference.wav` 或已接受样音。

## 本篇交接材料

每篇沿用一份作品清单。交接包至少包含来源 URL 与完整真实截图、获准使用的 Logo／人物原图、当前完整中文／英文稿、已确认片头片尾、独立封面要求、已接受干声及其回执和哈希、成片与字幕工程、各平台状态和实际回执。每项标明“用户已接受”“技术核验通过”或“待验收”，不能用新版号代替接受状态。

本篇的特定结尾、某张宣传卡的删改及只保留某英文版本，写在这份作品清单，不写成所有作品的通用口号或语言豁免。私人作品、聊天目标、凭据和云主机地址不提交到公共 GitHub。当前规则及示例均不授权重发已存在的帖子。

给云端执行者的启动指令可单独复制：

```text
使用 BLACKIELF/gbroskill 的当前完整 Release，先读主 Skill 与 docs/CLOUD-HANDOFF.md，校验清单并运行只读预检。按本篇作品清单和已确认稿件制作，全平台视频统一9:16，封面按各平台独立规格；TikTok和X用真实英文口播和英文稿。声音只能用固定G4路线，缺已验证运行环境时继续文字与排版，复用本篇已接受干声或交接给已验证配音端，不自行换模型或改片尾。先交可审阅成品，按本次已有平台授权交付并回读。
```
