# Bridge Install Guide for AI Agents

当用户让 AI 把 AI_MEMORY bridge 安装到另一个工程项目时，只读本文件和对应 bridge template 即可。不要为了安装 bridge 去加载整棵 `AI_CONTEXT/`。

## 目标

把 AI_MEMORY bridge 安装到目标项目，让目标项目通过 `AI_MEMORY_ROOT` 引用集中式 memory repo。

## 只读取这些文件

1. 本文件。
2. `templates/AGENTS.bridge.md`（**唯一** bridge 模板，v0.5 起已工具无关化）。
3. 如果目标项目已经存在 agent 文件，读取目标项目里的 `AGENTS.md` 或 `CLAUDE.md`。

> `templates/CLAUDE.bridge.md` 已废弃，不再用于新安装。新项目统一使用 `AGENTS.bridge.md` + 符号链接。

简单 bridge install 任务不需要读取 `AI_CONTEXT/` 或 `reference/`。只有用户明确要求 project memory setup、memory validation 或深入集成时，才按需读取更多上下文。

## 必须遵守的行为

- 默认保留 `AI_MEMORY_ROOT = ${AI_MEMORY_ROOT}`。
- 除非用户明确要求 project-local override，不要把平台相关 absolute path 写进目标项目。
- 保留目标项目已有的本地规则。
- 如果目标项目已有 `AGENTS.md` 或 `CLAUDE.md`，把 bridge 内容合入原文件，不要覆盖原文件。
- 如果原文件已经有 `AI_MEMORY Bridge` section，就原地更新这个 section。
- 如果原文件没有 bridge section，就在文件末尾追加新的 `AI_MEMORY Bridge` section。
- 不要删除、重写或重排已有项目规则，除非用户明确要求。
- 如果已有项目规则和 bridge 规则存在 material conflict，保留双方内容，并向用户报告冲突；不要静默裁决。

## 安装步骤

### 新项目（无已有 agent 文件）

1. 复制 `templates/AGENTS.bridge.md` → 目标项目根目录的 `AGENTS.md`。
2. 创建 `CLAUDE.md` 作为指向 `AGENTS.md` 的符号链接：

   ```bash
   # macOS / Linux
   cd <project_root>
   ln -s AGENTS.md CLAUDE.md

   # Windows PowerShell（需要 Developer Mode 或管理员权限）
   cd <project_root>
   New-Item -ItemType SymbolicLink -Path CLAUDE.md -Target AGENTS.md

   # Windows cmd（需要 Developer Mode 或管理员权限）
   cd <project_root>
   mklink CLAUDE.md AGENTS.md
   ```

3. 如果无法创建符号链接（权限不足、文件系统不支持、或用户拒绝），则**复制** `AGENTS.md` → `CLAUDE.md`，并告知用户两个文件需手动保持同步。
4. 根据用户指定的模式调整顶部的 `Bridge Switches`。

### 已有 AGENTS.md 的项目

1. 读取目标项目的 `AGENTS.md`。
2. 检查是否已有 `AI_MEMORY Bridge` section：
   - **没有**：在文件末尾追加 `AI_MEMORY Bridge` section（从 `AGENTS.bridge.md` 提取 switches + loading rules）。
   - **已有**：原地更新该 section 保持与最新 template 对齐。
3. 保留所有已有项目本地内容不变。
4. 检查是否存在 `CLAUDE.md`：
   - **不存在**：按上面新项目的命令创建符号链接。
   - **存在且已是 symlink → AGENTS.md**：无需操作。
   - **存在且是独立文件**：进入「两者同时存在」处理流程（见下文）。

### 已有 CLAUDE.md 但无 AGENTS.md 的项目

1. 读取 `CLAUDE.md`，将其内容作为基础。
2. 创建 `AGENTS.md`，把 bridge 内容合入（保留原 `CLAUDE.md` 的项目本地规则）。
3. 删除原 `CLAUDE.md`，创建为指向 `AGENTS.md` 的符号链接。

### 两者同时存在（AGENTS.md + CLAUDE.md 均为独立文件）

这种情况常见于用户之前分别从两个模板安装了 bridge。处理原则：**以内容较完整的一方为基底，合并另一方独有的项目规则，最终统一为一个 AGENTS.md + symlink**。

1. 读取 `AGENTS.md` 和 `CLAUDE.md` 的完整内容。

2. 提取两个文件的结构：
   - `AI_MEMORY Bridge` section（含 switches 和加载规则）
   - 项目本地规则（bridge section 之外的 markdown 内容）

3. 判断内容关系，选择合并策略：

   | 情况 | 策略 |
   |---|---|
   | 两者完全一致 | 保留 `AGENTS.md`，删 `CLAUDE.md` 改 symlink |
   | 仅 bridge section 不同 | 用最新 template 的 bridge section，合并两边项目本地规则 |
   | 项目本地规则不同且互不冲突 | 合并本地规则到 `AGENTS.md`，明确标注来源 |
   | 存在冲突（同一规则两边不同） | **报告冲突给用户**，保留双方内容，不要静默裁决 |
   | 一方是另一方的超集 | 保留超集版本作为 `AGENTS.md` |

4. 合并时，对项目本地规则的标注方式：
   ```markdown
   ## 本项目本地上下文

   ### 项目目标
   <!-- 来自原 AGENTS.md -->
   ...

   ### 来自原 CLAUDE.md 的本地规则
   <!-- 以下内容从原 CLAUDE.md 迁移 -->
   ...
   ```

5. 确认合并结果后：
   - 写入合并后的 `AGENTS.md`
   - 删除 `CLAUDE.md`（先备份或确保 git 可恢复）
   - 创建符号链接 `ln -s AGENTS.md CLAUDE.md`

6. **必须向用户报告**：
   - 两文件的内容关系（一致 / 超集 / 有差异 / 有冲突）
   - 合并了哪些内容
   - 是否有无法自动裁决的冲突
   - 原 `CLAUDE.md` 被替换为 symlink 的事实

## 符号链接说明

**为什么用符号链接而不是两份独立文件？**

- `AGENTS.bridge.md` 和旧 `CLAUDE.bridge.md` 内容 95% 相同，差异仅在于标题行。
- Codex 读取 `AGENTS.md`，Claude Code 同时支持 `CLAUDE.md` 和 `AGENTS.md`。
- 符号链接让两个文件名指向同一份内容，修改任意一个自动同步，避免两份文件内容不同步。

**跨平台注意事项：**

| 平台 | 命令 | 前提条件 |
|---|---|---|
| macOS / Linux | `ln -s AGENTS.md CLAUDE.md` | 无（原生支持） |
| Windows PowerShell | `New-Item -ItemType SymbolicLink -Path CLAUDE.md -Target AGENTS.md` | Developer Mode 或管理员权限 |
| Windows cmd | `mklink CLAUDE.md AGENTS.md` | Developer Mode 或管理员权限 |

Git 在 macOS/Linux 上原生跟踪符号链接。Windows 上需要 `git config core.symlinks true` 且开启 Developer Mode。

**符号链接不可用时的 fallback：**
- 复制 `AGENTS.md` → `CLAUDE.md`
- 告知用户两个文件需手动保持同步
- 建议用户开启 Developer Mode（Windows）或检查文件系统权限

## 推荐合入格式

合入已有 agent file 时，用这个 section wrapper：

```markdown
## AI_MEMORY Bridge

<!-- AI_MEMORY_ROOT = ${AI_MEMORY_ROOT} -->

<!-- Bridge Switches ... -->

<!-- bridge content copied or adapted from the template -->
```

这样未来更新 bridge 时容易定位，也能避免把目标项目本地规则和 AI_MEMORY portable bridge 规则混在一起。

## 默认模式

如果用户没有指定模式，使用 template 默认值：

- `GLOBAL_WORKFLOW_RO = on`
- `SKILLS_RO = on`
- `MEMORY_POLICY_RO = off`
- `PROJECT_MEMORY_RO = off`
- `PROJECT_MEMORY_RW = off`
- `ROUTE_LOG_RW = off`

长期项目如果要打开 project memory read/write switches，先询问用户。

## 验证

编辑目标项目后：

1. 告诉用户创建或更新了哪个文件。
2. 说明这是 new install 还是 merge into existing file。
3. 确认 `CLAUDE.md` 符号链接已创建（或说明 fallback 情况）。
4. 如果可行，运行：

```bash
python "$AI_MEMORY_ROOT/scripts/bridge_config_check.py" <target-file> --require-root
```

如果无法运行验证命令，明确说明 validation 未执行。
