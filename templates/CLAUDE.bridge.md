---
type: template
name: claude_bridge
scope: global
version: 0.5
status: deprecated
description: 自 v0.5 起，CLAUDE.md 应创建为指向 AGENTS.md 的符号链接，不再需要独立模板。
             AGENTS.bridge.md 是唯一的 bridge 模板，内容已工具无关化，同时适用于 Codex 和 Claude Code。
             本文件保留仅作为迁移参考。新项目请使用 AGENTS.bridge.md + symlink。
superseded_by: templates/AGENTS.bridge.md
---

# ⚠ 本模板已废弃

自 v0.5 起，bridge 安装方式改为：

1. 复制 `templates/AGENTS.bridge.md` → 项目根目录 `AGENTS.md`
2. 创建符号链接 `CLAUDE.md` → `AGENTS.md`

这样 Codex 和 Claude Code（以及其他兼容 AGENTS.md 的工具）读取的是同一份文件，修改任意一个即可同步。

## 为什么废弃

`AGENTS.bridge.md` 和 `CLAUDE.bridge.md` 的内容 95% 相同，差异仅在于标题行。维护两份模板没有意义，还容易导致实际项目中的两个文件内容不同步。

统一方案：
- `AGENTS.md` = 唯一真实文件（从 `AGENTS.bridge.md` 复制）
- `CLAUDE.md` = 指向 `AGENTS.md` 的符号链接

## 跨平台创建符号链接

```bash
# macOS / Linux
ln -s AGENTS.md CLAUDE.md

# Windows (PowerShell, 需要 Developer Mode 或管理员权限)
New-Item -ItemType SymbolicLink -Path CLAUDE.md -Target AGENTS.md

# Windows (cmd, 需要 Developer Mode 或管理员权限)
mklink CLAUDE.md AGENTS.md
```

如果不能创建符号链接（权限不足或文件系统不支持），则复制 `AGENTS.md` → `CLAUDE.md`，但需注意两个文件需手动保持同步。

## 迁移已有项目

如果项目已有独立的 `CLAUDE.md`（从旧模板复制而来）：
1. 对比 `AGENTS.md` 和 `CLAUDE.md`，确认哪个的内容更新
2. 把较新/较完整的内容合并到 `AGENTS.md`
3. 删除 `CLAUDE.md`
4. 按上述命令创建符号链接
---
