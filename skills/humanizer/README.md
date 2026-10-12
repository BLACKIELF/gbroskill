# Humanizer-zh（Codex 适配版）

> 本机版本 0924v1：相较 0627 旧版，同步上游 2026-09-23 修订的 31 个检查点；补充事实、条件、归因、作者声音和 Markdown 结构保护，移除默认自评分与旧版会编造细节的示例。

## 来源

改编自 [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)，固定到提交 [`f4518a8e`](https://github.com/op7418/Humanizer-zh/commit/f4518a8eab97b8bfebc66a89d34320a89bef6930)。正文与该提交的 `SKILL.md` 一致；仅将 Claude 专属 frontmatter 替换为 Codex 可用的名称和触发说明，并保留 `agents/openai.yaml`。

上游[更新记录](https://github.com/op7418/Humanizer-zh/blob/f4518a8eab97b8bfebc66a89d34320a89bef6930/CHANGELOG.md)说明了这次修订。该 Skill 改进文字表达，不判断作者身份，也不保证通过 AI 检测器。

## 使用

显式调用 `$humanizer-zh`，或直接请求润色、去 AI 味、改得更自然。默认保留原意、事实、确定程度、作者语气及文件中的代码、链接、标题和数据。只审阅时给建议；要求改文件时才写回。

本机安装位置：`~/.codex/skills/humanizer/`。升级现有目录后，开启新一轮对话或刷新 Skill 列表以加载新内容。
