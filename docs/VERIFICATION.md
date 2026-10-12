# 分发验证记录 · 1012v1

核验日期：2026-10-12。验证对象为此公开分发副本；本机有效 Skill、生产登录态和全局配置未修改。

| 检查 | 实际结果 | 边界 |
|---|---|---|
| Skill 官方 quick_validate | 顶层 31 个入口全部通过 | 结构可加载不证明外部账号已接通 |
| 非覆盖安装器 | 预览无写入、临时目录安装、同名修改冲突时整批停止均通过 | 没有覆盖本机现有 Skills |
| 完整性与依赖清单 | 逐文件 SHA-256、唯一组件 ID、组件目录及许可证检查通过 | 记录范围内的源码，不是所有互联网传递依赖的离线包 |
| 隐私扫描 | 未发现作者本机路径、已知账号／群标识、登录数据或高置信度密钥格式 | 扫描不代替审阅；13 个未改动上游文件含示例路径，已逐文件固定哈希例外，详见 config/scanner-fixtures.json |
| 代码静态检查 | 发布包装器 shell 语法、6 个 Python 文件 AST、stylewx 本地调用器语法通过 | 未全量重测第三方上游代码 |
| SAU 包装器帮助 | 小红书命令成功列出 login/check/upload-video/upload-note | 使用本机已有 Python 依赖解释器，运行的是分发源码；未登录、未投稿 |
| TikTok CLI 帮助 | 使用独立空数据目录通过 | 新数据目录父目录已补充自动创建；没有读取生产会话 |
| TikTok MCP | 使用分发源码 initialize/listTools 成功；autotok 2.0.1，8 个工具 | 仅发现工具，未调用登录、会话验证、上传、代理或排期 |
| ZIP | 打包器执行 CRC 与逐文件清单，产出 SHA-256 校验文件 | 对下载包使用随 Release 的校验文件复核 |

TikTok MCP 实际发现：`list_accounts`、`check_account`、`list_videos`、`upload_video`、`login`、`login_status`、`set_proxy`、`test_proxy`。工具名不是执行回执。

未在新机器重装全部网络依赖，未重新绑定 Metricool、YouTube、微信，未执行任何社交平台发布。stylewx 的 0.6.0 修复以单独运行文件补丁提供，本分发未重新构建并做微信实机验收；保留上游原源码和明确应用步骤。

可以复跑的无账号检查：

```bash
python3 scripts/verify_bundle.py
runtime/bin/gbro-publish --help
runtime/bin/gbro-publish doctor
```

发布工作流的 CI 只运行离线分发校验。公共仓库的 Actions 结果与实际平台投稿结果无关。
