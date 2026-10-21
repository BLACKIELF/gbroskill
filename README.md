# GBro Skill · AiGoodBro 内容工作流

把资料、链接和视频整理成可核验的稿件、封面、字幕与分平台发布素材。包含当前 GBro 规则，以及可再分发的配套 Skill、CLI 与 MCP 源码。

**版本：1021v1 · 清单更新：2026-10-21**

[安装与配置](docs/INSTALL.md) · [用了哪些工具](docs/TOOLCHAIN.md) · [完整依赖清单](docs/DEPENDENCIES.md) · [工具能力边界](docs/TOOL-BOUNDARIES.md) · [平台尺寸与话题](skills/gbro-social-workflow/references/platform-specs.md) · [下载发布包](https://github.com/BLACKIELF/gbroskill/releases/latest)

## 能做什么

- 来源核验、中文写作、标题、封面与内页、视频交付、Obsidian 归档。
- 小红书、微博、X、抖音、TikTok、B站、微信公众号、视频号、YouTube 的分平台准备与已授权发布。
- 把「查笔记／评论」与「投稿」分开选择工具，把草稿、排期、审核、公开发布分别验收。
- 维护每个平台的封面比例、上传预算、话题数量和工具限制；临发布再核目标账号当前入口。

## 发布续接

发布前先读取用户指定的来源对话与作品回执，复用已成功入口；重置消息第一句话先说日期、具体时间与时区，再说行动提示。见[续接与时间首句](skills/gbro-social-workflow/references/publishing-continuity.md)。

需要固定来源对话时，按[空配置示例](config/publishing-continuity.example.json)填写本机 `~/.local/share/gbro-publish/config/publishing-continuity.local.json`。实际对话 ID、路径和回执只保留在本机；公开包不携带原作者的对话或自动发布授权。

## 公开范围

本仓库仅分发 AiGoodBro 内容工作流及其可再分发依赖，不包含其他项目的课程、客户材料、品牌资产、媒体或私有配置。工具清单列出实际职责与分发状态；列为可选不代表已接通，源码随包也不代表运行环境已安装。

## 包里有什么

31 个顶层 Skill；上传器、autotok TikTok MCP、stylewx MCP、Agent-Reach、biliup、video-use、飞书 CLI 等源码；许可证、来源版本、必要本地补丁、脱敏配置示例和逐文件校验清单。

Skill 是操作说明，MCP／CLI 才执行具体动作。安装说明不等于配置工具、登录账号或获得发布权限。浏览器页面与平台权限可能变化；本包不承诺无人值守发布。

```text
skills/                 主工作流与可安装的配套 Skill
vendor/                 固定版本的第三方源码，保留各自许可证
runtime/                可移植发布入口及 TikTok MCP 桥接
patches/                原安装的必要修正及说明
config/                 不含账号的配置模板
scripts/                预检、非覆盖安装、验证和打包
LICENSES/               额外许可依据
dependencies.lock.json  全量组件清单（包括未捆绑项）
THIRD_PARTY_NOTICES.md   版权、许可证及修改说明
```

## 快速开始

Python 3.10+ 用于本仓库脚本。先预览安装计划；同名安装有差异会停止，不覆盖现有 Skill：

```bash
python3 scripts/install_skills.py --destination "$HOME/.codex/skills"
python3 scripts/install_skills.py --destination "$HOME/.codex/skills" --apply
```

默认只装主 Skill。选装全部：

```bash
python3 scripts/install_skills.py --destination "$HOME/.codex/skills" --all
python3 scripts/install_skills.py --destination "$HOME/.codex/skills" --all --apply
```

重启或刷新支持 Skills 的宿主后使用 `gbro`。可复制的调用示例：

```text
用 gbro 把这份材料做成小红书和微博稿，沿用红蓝白。先交本地正文、封面、视频和各平台话题，不发布。陌生术语在首图或第二张解释。
```

运行工具需要按[安装说明](docs/INSTALL.md)另行准备。安装器不修改 Codex 全局配置，不登录、不发送消息、不发布、不创建排期。

## 品牌预设与授权

红蓝白、`AiGoodBro` 固定话题、小红书 10 个话题以及视频画幅是此工作流的品牌预设，不是对所有账号的强制平台规定。其他品牌先配置自己的品牌、话题和资产。代码许可不授予商标权，也不代表原账号背书。

开源版已移除作者私人路径、账号快照、聊天目标和历史自动发布授权。任何第三方 Skill 中的安装／写入建议，仍须服从当前用户授权和宿主工具限制。私人参考图、二维码、素材版权和账号权益不随包转让。

## 开源许可

GBro 自有文件使用 [MIT](LICENSE)。第三方文件保留原许可；autotok 与 `runtime/tiktok-entry.py` 使用 **AGPL-3.0-only**，不能用根目录 MIT 覆盖。修改、分发或作为网络服务使用时，应按相应许可履行义务。完整对应源码随包提供。

Metricool、微信官方 API、宿主浏览器／生图服务需要用户自己的接入；许可不明的私人 Skill 未复制。详见[逐项清单](docs/DEPENDENCIES.md)与[第三方声明](THIRD_PARTY_NOTICES.md)。本包是来源清楚的工作流集合，不宣称拥有第三方项目。

## 参与维护

参见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [SECURITY.md](SECURITY.md)。提交平台规则变更时附来源、日期和入口；提交失败记录前移除身份、密钥、Cookie、带凭证 URL 和私人媒体。
