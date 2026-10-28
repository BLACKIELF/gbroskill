# 安装与配置

本包是源码集合，联网依赖未离线打包。先运行 `python3 scripts/verify_bundle.py`；完整核验清单为根目录 `SHA256SUMS.txt`。Mac/Linux 可用下述命令，Windows 的虚拟环境可执行文件位于 `Scripts`，不能照搬 `bin` 路径。未在所有操作系统、账号和平台执行真实发布测试。

## Skill

使用 README 中的安装器。默认预览、不覆盖；`--skill 名称` 可重复指定，只安装需要的项目。`--all` 仅安装顶层 31 个 Skill，不会安装 `vendor/` 内额外的上游 Skill。安装前发现重复需比较；同内容会跳过，有差异会退出。

别名 `gbro`、`gbroskill`、`goodbroskill` 使用同一个 `gbro-social-workflow`，不创建第二份可写规则。

## 呼吸晕染模板

安装主 Skill 后，直接用支持 WebGL 2 的浏览器打开 `assets/breathing-frame/portrait-template.html`。选择本地视频，点击画布文字编辑；文件只在本机读取，不上传。模板可独立离线预览，不需要安装 JavaScript 库。系统没有 PingFang SC 时会使用替代字体，交付前检查标题与字幕排版。

重置快讯使用 `assets/breathing-frame/reset-message-template.html`：点击文字编辑，选入本地来源头像，再用“保存当前模板”导出可再次打开的 HTML。公开空白模板不含真人照片、具体消息或日期，使用前填入本次已核实内容。

横版素材使用同目录的 `frame.html` 与 `loop.webm`，保留相对位置；规格和重新渲染方法见[边框说明](../skills/gbro-social-workflow/references/breathing-frame.md)。预览模板不代替最终视频编码与声音处理。

## SAU：抖音、小红书、B站、微博视频、视频号

需要 Python 3.10–3.12，建议 3.11；需要已安装的 Chrome／Chromium。源码带必要修正，版本和来源见依赖清单。请在仓库根目录执行：

```bash
python3.11 -m venv vendor/social-auto-upload/.venv
vendor/social-auto-upload/.venv/bin/python -m pip install -e ./vendor/social-auto-upload
export GBRO_CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
export PATH="$PWD/runtime/bin:$PATH"
gbro-publish doctor
gbro-publish xiaohongshu --help
```

其他系统把 `GBRO_CHROME` 改成实际浏览器可执行文件。这里未复制浏览器、Python 环境或浏览器登录。运行前必须已获安装依赖的授权；上述 pip 命令会联网获取依赖。

账号由使用者在工具自己的官方登录窗口扫码或验证。SAU 的 `upload-*` 通常真实提交，不能拿来测试连通。B站可能另行下载 biliup；源码也保留在 `vendor/biliup`，其原文构建指令和许可证随包提供。B站当前包装器没有转载来源字段，转载内容先换到能填写该字段的授权入口。

## X 与微博编辑器

需要 Bun、Chrome，以及各 Skill `scripts/package.json` 中的依赖；保留了原 `bun.lock`：

```bash
(cd skills/baoyu-post-to-x/scripts && bun install --frozen-lockfile)
(cd skills/baoyu-post-to-weibo/scripts && bun install --frozen-lockfile)
runtime/bin/gbro-publish x --help
runtime/bin/gbro-publish weibo --help
```

X 默认填稿，`--submit` 才提交；远程填稿也会把内容传到平台。微博普通帖／文章脚本不完成最终发布。独立浏览器不能自动继承内置浏览器的登录，用户限定内置浏览器时仍遵守该限制。

## TikTok CLI 与 MCP

autotok 为 AGPL-3.0-only，完整源码、NOTICE、依赖声明和构建文档在 `vendor/autotok`。桥接源码也使用 AGPL。

```bash
python3.11 -m venv vendor/autotok/.venv
vendor/autotok/.venv/bin/python -m pip install -e './vendor/autotok[mcp]'
runtime/bin/gbro-publish tiktok --help
```

运行桥接时会创建自己的数据目录，默认 `~/.local/share/gbroskill/private-tiktok`。不复制作者账号。MCP 示例见 `config/mcp.example.json`，把路径换成克隆目录的绝对路径再由宿主正常添加，示例不会自行修改任何全局配置。

TikTok 桥接保留品牌规则：含准确 `#AiGoodBro`，最多 5 个话题为本地运行预算；这不是所有地区统一官方硬限制。改为其他品牌时同时改品牌预设和桥接校验，并标明自己的修改。`upload_video` 是真实发布，默认公开；不得用私密发布冒充本地测试。MCP HTTP 入口仅允许本机回环地址，推荐 stdio。

## stylewx MCP：公众号排版与草稿

`vendor/stylewx` 是 0.6.0 对应上游源码，MIT。使用上游 `package.json` 中指定的 pnpm 版本，在该目录 `pnpm install --frozen-lockfile` 后 `pnpm build`。也可以自行按官方说明安装固定 `@stylewx/mcp-server@0.6.0`；包管理器安装会联网。

本包保留 `patches/stylewx-components-0.6.0.patch`，修正点击揭晓和字体属性转义。它针对 **0.6.0 的已构建文件**，不是已应用到 `vendor/stylewx` 的源码补丁。要复用，先确认目标组件版本和哈希，再在对应 `node_modules` 目录执行 `patch --dry-run -p1`；通过后再应用。构建源码得到的未修正版不能宣称已经具有该修复。

```bash
# 使用本仓库的已构建服务（需先完成上游构建）
export GBRO_STYLEWX_ROOT="$PWD/vendor/stylewx/apps/mcp-server"
node skills/stylewx-article/scripts/stylewx-local.mjs list
```

本地调用器默认不读取或自动继承微信凭证，只做排版／检查。`publish_draft` 需要使用者自己的官方接入和权限，草稿不是发表，也不是群发。连接器配置由使用者管理，不从别的工具导出密钥。

## 飞书、Obsidian 与媒体

- 飞书：四个必要 Skill 和官方 `vendor/lark-cli` 源码使用 MIT。CLI 的 Go/Node 运行要求及构建命令见其 README。用户须配置自己的 profile、应用权限、bot／user 身份和接收方。安装不授权发送消息。
- Obsidian：两个 Skill 已包含；Vault 路径由使用者提供或从其配置确认，不附带私人笔记。
- Agent-Reach：Skill 和源码已包含，但每个平台后端需单独安装、发现和验证。小红书 MCP/OpenCLI 不是 SAU，也未因安装本包接通。
- video-use：源码与 Skill 已包含；FFmpeg、配音／视频服务按当前任务另配。服务额度、模型权限和素材权利不包含在代码许可中。
- 生图：Apache-2.0 的 imagegen Skill 源码已附，不包含模型服务或额度。优先使用宿主实际提供的生图接口。

## Metricool、微信官方通道与可选组件

Metricool 是托管服务：在宿主的官方连接器或 [Metricool 官方接入指南](https://metricool.com/metricool-mcp-claude/)连接自己的账号，再按品牌绑定 TikTok／YouTube／X 等。不要从作者复制 brandId、Cookie 或 API token。工具发现、品牌绑定、排期与实际公开结果分别验证。

微信公众号、小程序继续使用用户自己的官方接入，代码、素材、草稿、群发和小程序提审权限分别验证。小程序不是通用发帖平台。

不能再分发或来源不明的项目在 [DEPENDENCIES.md](DEPENDENCIES.md) 列全；不是用占位实现假装完成接入。缺少的可选能力不影响本地写稿与已就绪的独立路线。

## 升级与回退

保留当前 Skill／源码和自己的配置备份，比较新旧版本再合并。不要用上游更新覆盖 `patches/` 中的修复。此发布包不覆盖本机原安装，也不携带生产凭据；安装器无自动覆盖开关，回退时只处理自己实际安装的目录。
