---
name: tiktok-upload
description: 使用本机 GBro 入口登录、校验和发布国际 TikTok 视频，或启动已安装的 TikTok MCP。适用于美国或国际 TikTok；抖音使用 douyin-upload。
---

# TikTok 视频发布

运行依赖为 [makiisthenes/TiktokAutoUploader](https://github.com/makiisthenes/TiktokAutoUploader) 的 autotok，使用独立 Python 环境与本机 Chrome。统一入口为 `gbro-publish`，账号文件仅存于 `${GBRO_RUNTIME_ROOT}/private-tiktok/accounts/`。来源、版本和验证边界见仓库 `docs/INSTALL.md`。

环境同时提供 Metricool 时，按 [GBro 发布入口](https://github.com/BLACKIELF/gbroskill/blob/main/skills/gbro-social-workflow/references/platform-tools.md#metricool-连接器)先核品牌与 TikTok 绑定。Metricool 可用于已连接账号的排期，本页命令仅适用于本机 autotok；两者的账号、媒体、结果和限制分别验证，不因本机已登录就宣称云端已绑定，不向两条通道重复提交同一作品。

## 登录与检查

```bash
gbro-publish tiktok --help
gbro-publish tiktok login -n AiGoodBro
gbro-publish tiktok accounts list
gbro-publish tiktok accounts check AiGoodBro
```

`AiGoodBro` 是本地别名，不证明平台身份。用户在工具自带独立窗口完成登录或扫码；不代输验证码，不跨用抖音或其他平台身份。保存会话后，仍需核对 TikTok 的显示名、@用户名或个人主页 URL；`accounts check` 只验证会话可用于上传，不证明账号姓名或美国账号地区。只读取必要状态，不展示 cookie、sessionid 或代理认证信息。

## 发布

先读取 [GBro 平台规格与话题](https://github.com/BLACKIELF/gbroskill/blob/main/skills/gbro-social-workflow/references/platform-specs.md)，核对已授权的账号、文件、正文、可见性、时间和内容声明。运行 `gbro-publish tiktok upload --help` 获取当前真实参数，再填入本篇已批准内容。

- AiGoodBro 品牌预设所有实际支持话题／标签的入口都必须带品牌项；TikTok 用 `#AiGoodBro`，大小写照此保留，当前按最多 5 个话题执行，包含品牌话题。这是保守运行数量上限，本账号和此工具的当前投稿入口尚未实证，不能称为所有地区、入口的官方硬限制。统一入口会拒绝缺少品牌话题或超过此运行上限的正文。
- 话题放在 caption 中，采用 `#话题`；上游会生成可点击的 hashtag 标记，不能只写普通文字。上游 caption 最长 2200 字符是工具校验预算，平台当前规则应临发布核实。
- `upload` 和 MCP `upload_video` 都会实际发帖，默认公开；私密帖仍是真实发布，没有本机草稿预览模式。安装和登录授权不等于任意作品发布授权。
- 用户指定内置浏览器时，实际发布继续在该浏览器执行；本工具打开独立 Chrome 的登录授权不改变浏览器要求，未解除该限制时不调用此 CLI/MCP 提交。
- 工具本次接入视频发布与定时，不凭空承诺图文、独立封面设置或商业内容声明。`brandorganic`/`brandcontent` 兼容参数被上游忽略；需要商业内容披露时先核实际官方投稿入口，不把忽略参数当功能。
- AI 声明、评论、合拍、拼接与可见性按事实及用户要求选择，保留平台强制提示。`--schedule` 使用秒，MCP `schedule_in_minutes` 使用分钟；提前时间的上游范围不能替代本账号当前权限。
- 只进行一次真实提交。遇到 `PublishUncertainError`、超时或结果未知，停止重试，先在 TikTok 核对作品是否存在；不能重复提交来探测结果。成功返回 video id 后还要回读真实作品及 URL，记录实际凭据，不能仅靠退出码声称发布成功。

## MCP

```bash
gbro-publish tiktok-mcp
```

该命令启动 stdio MCP；客户端配置样例在 [tiktok-mcp.example.json](${GBRO_RUNTIME_ROOT}/config/tiktok-mcp.example.json)，尚未写入 Codex 全局配置。可用工具为 `list_accounts`、`check_account`、`list_videos`、`upload_video`、`login`、`login_status`、`set_proxy`、`test_proxy`。`login` 要由用户完成，`login_status` 需在启动登录的同一 MCP 进程内轮询；保存后可重新读取账号文件状态。

`list_accounts` 的 `logged_in` 仅说明本机存在会话；`check_account` 才联网核会话。默认不调用上传工具做连通测试。HTTP 无认证，仅允许本机 loopback；不暴露公网。此安装固定使用本机 Chrome，不选择云浏览器或付费代理，不改全局代理、auth.json 或 config.toml。
