---
name: ai-memory-bridge-installer
description: 安装 AI_MEMORY bridge 到新建或已有项目。Use when the user asks to connect a repo/project to AI_MEMORY, install AGENTS.md or CLAUDE.md bridge rules, create or merge AI_MEMORY Bridge sections, set up AI_MEMORY_ROOT, or adjust Bridge Switches while preserving existing AGENTS.md/CLAUDE.md content.
---

# AI_MEMORY Bridge Installer

## 核心规则

- 只为目标项目安装 bridge；不要为了安装 bridge 读取整棵 `AI_CONTEXT/`。
- 默认保留 `AI_MEMORY_ROOT = ${AI_MEMORY_ROOT}`。
- `AGENTS.md` 是唯一真实 bridge 文件；`CLAUDE.md` 应尽量作为指向 `AGENTS.md` 的 symlink。
- 如果目标项目已有 `AGENTS.md` 或独立 `CLAUDE.md`，必须合并，不要覆盖。
- 合并时保留所有原有内容，在独立的 `AI_MEMORY Bridge` section 中追加或更新 bridge。
- 如果已有项目规则与 bridge 规则存在 material conflict，保留双方内容并报告用户。

## 推荐流程

1. 判断目标 agent setup：
   - Codex / AGENTS ecosystem -> install or merge `AGENTS.md`
   - Claude Code -> install or merge `AGENTS.md`, then create `CLAUDE.md -> AGENTS.md` symlink when safe
2. 运行脚本安装或合并 bridge：

```bash
python <skill-dir>/scripts/install_bridge.py --target <project-dir> --agent codex
python <skill-dir>/scripts/install_bridge.py --target <project-dir> --agent claude
```

3. 如果用户指定模式，传入 `--mode`：

```bash
python <skill-dir>/scripts/install_bridge.py --target <project-dir> --agent codex --mode medium
```

可用模式：

- `template`：保持 template 默认值。
- `small`：只打开 `GLOBAL_WORKFLOW_RO`。
- `medium`：打开 `GLOBAL_WORKFLOW_RO`、`SKILLS_RO`、`PROJECT_MEMORY_RO`。
- `large`：六个 `Bridge Switches` 全部打开。

4. 安装后运行验证：

```bash
python "$AI_MEMORY_ROOT/scripts/bridge_config_check.py" <target-agent-file> --require-root
```

如果无法运行验证命令，说明原因，不要声称已验证。

## 脚本行为

`scripts/install_bridge.py` 会：

- 从 `AI_MEMORY_ROOT/templates/AGENTS.bridge.md` 读取唯一 bridge template。
- 如果 `AI_MEMORY_ROOT` 未设置，且脚本运行在 AI_MEMORY repo 内，则自动回溯找到 repo root。
- 如果目标 agent file 不存在，直接用 template 创建。
- 如果目标 agent file 已存在：
  - 保留原文件所有内容；
  - 用 `<!-- BEGIN AI_MEMORY_BRIDGE -->` / `<!-- END AI_MEMORY_BRIDGE -->` 包住 bridge section；
  - 若 markers 已存在，则原地更新该 block；
  - 若 markers 不存在但已有 `## AI_MEMORY Bridge` heading，则替换该 section；
  - 否则在文件末尾追加新 section。
- 当 `--agent claude` 时：
  - 如果 `CLAUDE.md` 不存在，则创建指向 `AGENTS.md` 的 symlink；
  - 如果 `CLAUDE.md` 已经是指向 `AGENTS.md` 的 symlink，则保持不变；
  - 如果 `CLAUDE.md` 是独立文件，则不覆盖，提示用户先合并。

## 注意事项

- 不要把平台相关 absolute path 写入目标项目，除非用户明确要求。
- 不要自动打开 `PROJECT_MEMORY_RW` 或 `ROUTE_LOG_RW`，除非用户明确指定 `large` 或要求写入 memory。
- 如果目标项目已有独立 `AGENTS.md` 和 `CLAUDE.md` 且二者内容不同，先保留两者并报告用户；不要静默选择哪个更权威。
