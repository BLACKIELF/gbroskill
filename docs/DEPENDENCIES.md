# 依赖与分发清单

清单更新：2026-10-21；原有捆绑源码版本保持不变，不表示上游已全部重新核验为最新版。完整机器可读记录在 [dependencies.lock.json](../dependencies.lock.json)。本表覆盖直接工作流依赖、已使用的发布／读取入口和被引用的可选能力；安装环境、账号数据及所有包管理器传递依赖未作为离线环境复制。

## 已捆绑

| 组件 | 类型 | 许可 | 目录与来源 |
|---|---|---|---|
| gbro-social-workflow | skill | MIT | `skills/gbro-social-workflow` · [https://github.com/BLACKIELF/gbroskill](https://github.com/BLACKIELF/gbroskill) |
| human-writing | skill | MIT | `skills/human-writing` · 未建立可公开验证的上游入口 |
| humanizer | skill | MIT | `skills/humanizer` · [https://github.com/op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) |
| title-matrix | skill | MIT | `skills/title-matrix` · [https://github.com/zhouwei713/title-matrix](https://github.com/zhouwei713/title-matrix) |
| anysearch | skill | Apache-2.0 | `skills/anysearch` · [https://github.com/anysearch-ai/anysearch-skill](https://github.com/anysearch-ai/anysearch-skill) |
| gbro-cover-design | skill | MIT | `skills/gbro-cover-design` · [https://github.com/pyang5166/gbro-cover-design](https://github.com/pyang5166/gbro-cover-design) |
| space-xhs-writer | skill | MIT | `skills/space-xhs-writer` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| space-xhs-title | skill | MIT | `skills/space-xhs-title` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| space-xhs-cover | skill | MIT | `skills/space-xhs-cover` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| space-xhs-image | skill | MIT | `skills/space-xhs-image` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| space-xhs-hotspot | skill | MIT | `skills/space-xhs-hotspot` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| space-xhs-note-analytics | skill | MIT | `skills/space-xhs-note-analytics` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| space-xhs-account-audit | skill | MIT | `skills/space-xhs-account-audit` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| space-xhs-positioning | skill | MIT | `skills/space-xhs-positioning` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| xhs-html | skill | MIT | `skills/xhs-html` · [https://github.com/SpaceZephyr/creator-buddy](https://github.com/SpaceZephyr/creator-buddy) |
| agent-reach | skill | MIT | `skills/agent-reach` · [https://github.com/Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) |
| imagegen | skill | Apache-2.0 | `skills/imagegen` · OpenAI bundled imagegen Skill (Apache-2.0 license included locally) |
| baoyu-post-to-x | skill | MIT | `skills/baoyu-post-to-x` · [https://github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) |
| baoyu-post-to-weibo | skill | MIT | `skills/baoyu-post-to-weibo` · [https://github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) |
| douyin-upload | skill | MIT | `skills/douyin-upload` · [https://github.com/dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) |
| xiaohongshu-upload | skill | MIT | `skills/xiaohongshu-upload` · [https://github.com/dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) |
| bilibili-upload | skill | MIT | `skills/bilibili-upload` · [https://github.com/dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) |
| stylewx-article | skill | MIT | `skills/stylewx-article` · [https://github.com/wjunhere/stylewx](https://github.com/wjunhere/stylewx) |
| obsidian-cli | skill | MIT | `skills/obsidian-cli` · [https://github.com/kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| obsidian-markdown | skill | MIT | `skills/obsidian-markdown` · [https://github.com/kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| tiktok-upload | skill | MIT | `skills/tiktok-upload` · [https://github.com/BLACKIELF/gbroskill](https://github.com/BLACKIELF/gbroskill) |
| social-auto-upload | tool-source | MIT | `vendor/social-auto-upload` · [https://github.com/dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) |
| autotok | mcp-source | AGPL-3.0-only | `vendor/autotok` · [https://github.com/makiisthenes/TiktokAutoUploader](https://github.com/makiisthenes/TiktokAutoUploader) |
| video-use | tool-source | MIT | `vendor/video-use` · [https://github.com/browser-use/video-use](https://github.com/browser-use/video-use) |
| stylewx | mcp-source | MIT | `vendor/stylewx` · [https://github.com/wjunhere/stylewx](https://github.com/wjunhere/stylewx) |
| agent-reach-runtime | tool-source | MIT | `vendor/agent-reach` · [https://github.com/Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) |
| biliup | tool-source | MIT | `vendor/biliup` · [https://github.com/biliup/biliup](https://github.com/biliup/biliup) |
| cheat-on-content | optional-tool-source | MIT | `vendor/cheat-on-content` · [https://github.com/XBuilderLAB/cheat-on-content](https://github.com/XBuilderLAB/cheat-on-content) |
| video-use-skill | skill | MIT | `skills/video-use` · [https://github.com/browser-use/video-use](https://github.com/browser-use/video-use) |
| lark-shared | skill | MIT | `skills/lark-shared` · [https://github.com/larksuite/cli](https://github.com/larksuite/cli) |
| lark-im | skill | MIT | `skills/lark-im` · [https://github.com/larksuite/cli](https://github.com/larksuite/cli) |
| lark-doc | skill | MIT | `skills/lark-doc` · [https://github.com/larksuite/cli](https://github.com/larksuite/cli) |
| lark-drive | skill | MIT | `skills/lark-drive` · [https://github.com/larksuite/cli](https://github.com/larksuite/cli) |
| lark-cli | tool-source | MIT | `vendor/lark-cli` · [https://github.com/larksuite/cli](https://github.com/larksuite/cli) |
| gbro-tiktok-bridge | mcp-bridge | AGPL-3.0-only | `runtime/tiktok-entry.py` · [https://github.com/BLACKIELF/gbroskill](https://github.com/BLACKIELF/gbroskill) |

## 未捆绑：原因及获取路径

这些项目没有用伪造占位实现替代。云端权限由使用者接入，许可未明确的源码需取得许可后才能复制。

| 组件 | 原因／使用边界 | 来源 |
|---|---|---|
| browser-skill | Installed bsk/bundled documentation has no confirmed redistribution license. Use the browser interface supported by your host. | 未建立可公开验证的上游入口 |
| metricool | Hosted connector/service; no service implementation or account authorization can be redistributed. Connect your own account in your host. | [https://metricool.com](https://metricool.com) |
| weixin-reader | Tool available in the original host; implementation provenance and redistribution license not established. No server source bundled. | 未建立可公开验证的上游入口 |
| wechat-official | Bring your own official account, scopes and credentials. Draft, publish and mass-send permissions are separate. | [https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html) |
| miniprogram-official | Bring your own app and official integration. Not a generic social-post endpoint. | [https://developers.weixin.qq.com/miniprogram/dev/framework/](https://developers.weixin.qq.com/miniprogram/dev/framework/) |
| yichen-content-archive | Installed personal content archive has no confirmed redistribution license. Not copied. Use an authorized browser or Agent-Reach backend for equivalent supported reads. | 未建立可公开验证的上游入口 |
| yichen-wechat-mp-batch-exporter | Installed private/local workflow has no confirmed redistribution license; article archives, keys and databases excluded. | 未建立可公开验证的上游入口 |
| jev-use | Local wrapper/service with no established redistribution grant. Not required for the main workflow. | 未建立可公开验证的上游入口 |
| feishu-document-layout | Local custom Skill; upstream rights not established for public redistribution. Not copied. | 未建立可公开验证的上游入口 |
| xiaohongshu-ops-skill | No LICENSE found in upstream repository; no source copied. OpenClaw-specific workflow is optional. | [https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill](https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill) |
| wechat-apple-layout | No confirmed open-source license. Not copied; use separately acquired rights. | [https://github.com/S-N-Lewis/wechat-apple-layout](https://github.com/S-N-Lewis/wechat-apple-layout) |
| liquid-glass | Personal design workflow with project references; no confirmed redistribution grant. Use your own licensed visual tool. | 未建立可公开验证的上游入口 |
| iphone-use | Host plugin and real-device permissions are separate; not bundled. | 未建立可公开验证的上游入口 |
| documents | Use the document capability supplied by your host; no proprietary plugin source bundled. | 未建立可公开验证的上游入口 |
| general-collaboration-habits | Personal collaboration/paths/recipient policy not distributed; generic authorization and delivery boundaries are written directly into GBro. | 未建立可公开验证的上游入口 |
| xiaohongshu-mcp | Documented optional read backend, not installed or used in the audited local route. Obtain upstream separately if chosen. | [https://github.com/xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) |
| opencli | Documented optional read backend; not installed in the audited local route. Browser extension and your own authorized session required. | [https://github.com/jackwener/opencli](https://github.com/jackwener/opencli) |

## 版本证据

`revision` 是核验上游／运行源码的固定提交。标为 installed snapshot 的 Skill 保留本机已维护文案，可能含本地修改，不保证逐字等于该上游提交。无法证明具体提交的组件使用 null，不编造版本。逐文件分发字节见 `files.sha256.json`。宿主云端工具的实际功能以当前 schema 和账号权限为准。

## 依赖不等于已接通

源码已附、依赖安装、MCP 被发现、账号登录、身份核验、作品公开可读是六个独立状态。本包仅保证发布时记录的源码与包完整性，不把作者机器上的历史登录、界面成功或账号额度转移到其他安装。

## 视频与素材运行时（均未捆绑）

用途、费用、验证范围见[实际工具链](TOOLCHAIN.md)。

| 组件 | 许可／边界 | 来源 |
|---|---|---|
| openai-whisper | MIT；Main local ASR: large-v3-turbo, word timestamps. Code, weights and Python environment not bundled. Local tested package 20250625; not a required version. | [上游](https://github.com/openai/whisper) |
| ffmpeg | LGPL-2.1-or-later; build-dependent GPL；Local audio extraction, subtitles through libass, composition and encode. Binary, fonts and codecs not bundled; inspect the chosen build. Local tested version 9.0.2. | [上游](https://ffmpeg.org) |
| faster-whisper | MIT；Optional alternative ASR, not the default route. Local installed package 1.2.1; not bundled or claimed to have end-to-end route validation. | [上游](https://github.com/SYSTRAN/faster-whisper) |
| whisper.cpp | MIT；Optional local ASR backend. Local 1.9.5 tiny.en sample passed on Metal; not equivalent to main large-v3-turbo validation. No binaries or weights bundled. | [上游](https://github.com/ggml-org/whisper.cpp) |
| jianying-headless | LicenseRef-Upstream-Noncommercial；Optional external editable-draft workflow. Personal learning/non-commercial license; commercial use requires upstream written permission. Source, adapter, proprietary editor and fonts not bundled. Local 11.6 draft build verified; native headless export unsupported for that tested version. | [上游](https://github.com/mcncarl/jianying-headless) |
| openverse | Per-asset license；Optional music/media discovery; source asset license and attribution must be checked separately. No media, client or service bundled. | [上游](https://openverse.org) |
