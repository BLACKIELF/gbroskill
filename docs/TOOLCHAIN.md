# AiGoodBro 实际使用的工具链

清单更新：2026-10-28。公开包只包含 AiGoodBro 工作流及允许再分发的配套源码。逐项来源、许可证和固定版本见 [依赖清单](DEPENDENCIES.md)及 [机器清单](../dependencies.lock.json)。下表说明各环节实际由谁完成，避免把 Skill 说明误认为模型或已配置的服务。

| 环节 | 工具与职责 | 随包内容／接入条件 |
|---|---|---|
| 编排与核验 | gbro-social-workflow；anysearch、Agent-Reach 查找和读取来源 | 说明及清单所列源码；搜索服务、浏览器、账号自行配置 |
| 中文稿、标题 | human-writing、humanizer、title-matrix、creator-buddy 系列 | Skill 说明；推理由当前宿主模型执行，不内置固定文本模型 |
| 封面与图文 | gbro-cover-design、creator-buddy、imagegen | 可分发说明；生图模型、API 权限、品牌原素材未捆绑 |
| 本地语音转写 | OpenAI Whisper + large-v3-turbo，生成原语言文本及词级时间戳 | Python 包、模型权重和运行环境另装，首次取得模型需要网络和磁盘空间 |
| 中文字幕 | 宿主模型翻译原语言转写稿，结合上下文校正切句与时间轴 | 不绑定单独翻译 API；Whisper 的 translate 任务输出英语，不能当作英译中 |
| 字幕与成片 | FFmpeg，含 libass 的构建烧录字幕、保留原声、包装及编码 | 二进制、字幕字体另备；检查实际构建是否支持所需滤镜和编码器 |
| 呼吸晕染包装 | 浏览器原生 HTML/CSS、WebGL 2、Canvas 与本地 video | 随包提供可编辑 9:16 HTML、X 样式来源卡和横版透明循环；无网络依赖，需兼容浏览器和系统字体，最终音频与编码另行处理 |
| 可编辑剪辑 | 可选 jianying-headless + 用户的剪映环境 | 不捆绑源码、本机适配器或剪映应用；有单独许可和版本限制 |
| 其他语音后端 | faster-whisper、whisper.cpp | 可选替代项，不是默认同时运行，也不随包安装 |
| 背景音乐／素材 | 可选 Openverse 检索 | 未包含曲库；逐个核验许可、署名和商用条件 |
| 发布 | social-auto-upload、baoyu-post-to-x/weibo、biliup、autotok、stylewx；可选 Metricool 和官方 API | 可分发源码见清单；登录、宿主连接、平台权限分别配置 |
| 交付与归档 | 飞书 CLI / lark Skills、Obsidian Skills | 可分发源码／说明；收件方、账号与资料库自行配置，发送需任务授权 |

## 视频路线

默认：原视频 → Whisper 原语言转写和词级时间戳 → 中文翻译与人工/逐句复核 → FFmpeg 字幕、原声与包装 → 解码、画面和字幕验收。保留原片与时间戳来源，不能只看转写文字判断译文与音画一致。

需要删口误、调整段落、多轨或可编辑工程时，再选择剪映路线：转写 → 审阅剪辑计划 → 生成草稿 → 验证草稿 → 在兼容编辑器内检查并导出。静音、重复和口头词仅标记候选；未确认参数和删改决策前，不自动删片段。本公开包没有安装或接通本机 Whisper→剪映适配器，不承诺一键执行这条路线。

[jianying-headless 上游](https://github.com/mcncarl/jianying-headless)及其 [LICENSE](https://github.com/mcncarl/jianying-headless/blob/main/LICENSE)限个人学习／非商用，商业使用需上游书面许可，因此不作为 MIT 依赖打包。维护者测试的剪映 11.6 环境支持草稿构建，但不支持该工具的原生无头导出；使用前按上游兼容矩阵核对实际版本，不绕过完整性或许可检查。

## 费用与许可证

- Whisper 本地推理没有按分钟的云 API 费用，仍消耗本机算力、电力与存储。代码与模型按上游 MIT；依赖包保留各自许可。faster-whisper、whisper.cpp 是不同实现，不混称同一个引擎。
- FFmpeg 许可取决于构建选项与链接库；不能把含 GPL 组件的构建一概称为 LGPL，也不能用本仓库 MIT 覆盖。参考 [FFmpeg 官方许可说明](https://ffmpeg.org/legal.html)。
- 宿主文本／生图、搜索及发布服务是否收费由所用服务和账户方案决定，本仓库不含额度或授权。未接通的付费语音服务不列作当前能力。
- 模型权重、Python 虚拟环境、浏览器登录态、客户素材和收件人信息均不随发布包上传。

## 已验证与尚未验证

维护者本机记录：openai-whisper 20250625 + large-v3-turbo、FFmpeg 9.0.2 已完成样例转写、字幕合成及完整解码检查；whisper.cpp 1.9.5 完成 tiny.en / Metal 样例转写；faster-whisper 1.2.1 只确认安装版本。剪映路线完成样例草稿构建与结构校验。以上是本机测试版本，不是跨平台最低要求、固定安装版本或“始终最新”的承诺。

上述语音与剪辑验证沿用 1021v1 记录；本次新增包装模板的验证见下方分发记录。未替使用者安装这些运行时，未验证其目标设备、中文客户素材、剪映界面导出或任何社交平台发布。包的校验结果见 [VERIFICATION.md](VERIFICATION.md)。
