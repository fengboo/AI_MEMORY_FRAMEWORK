# Bridge Install Guide for AI Agents

当用户让 AI 把 AI_MEMORY bridge 安装到另一个工程项目时，只读本文件和对应 bridge template 即可。不要为了安装 bridge 去加载整棵 `AI_CONTEXT/`。

## 目标

把 AI_MEMORY bridge 安装到目标项目，让目标项目通过 `AI_MEMORY_ROOT` 引用集中式 memory repo。

## 只读取这些文件

1. 本文件。
2. 一个对应的 bridge template：
   - Codex / AGENTS ecosystem：`templates/AGENTS.bridge.md`
   - Claude Code：`templates/CLAUDE.bridge.md`
3. 如果目标项目已经存在 agent 文件，读取目标项目里的 `AGENTS.md` 或 `CLAUDE.md`。

简单 bridge install 任务不需要读取 `AI_CONTEXT/`。只有用户明确要求 project memory setup、memory validation 或深入集成时，才按需读取更多上下文。

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

1. 确认目标 agent file：
   - Codex / AGENTS ecosystem -> `AGENTS.md`
   - Claude Code -> `CLAUDE.md`
2. 读取对应 bridge template。
3. 检查目标文件是否已经存在。
4. 如果目标文件不存在，用 template 创建新文件。
5. 如果目标文件已经存在：
   - 读取完整文件；
   - 保留所有已有内容；
   - 追加或更新名为 `AI_MEMORY Bridge` 的 section；
   - 将 template 中的 `AI_MEMORY_ROOT`、`Bridge Switches` 和 loading rules 合入该 section；
   - 保持本地项目规则在 bridge section 之外不变。
6. 除非用户另有要求，保持 `AI_MEMORY_ROOT = ${AI_MEMORY_ROOT}`。
7. 只有用户指定模式时，才调整六个 `Bridge Switches`。

## 推荐合入格式

合入已有 agent file 时，用这个 section wrapper：

```markdown
## AI_MEMORY Bridge

<!-- AI_MEMORY_ROOT = ${AI_MEMORY_ROOT} -->

<!-- Bridge Switches ... -->

<!-- bridge content copied or adapted from the selected template -->
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
3. 如果可行，运行：

```bash
python "$AI_MEMORY_ROOT/scripts/bridge_config_check.py" <target-file> --require-root
```

如果无法运行验证命令，明确说明 validation 未执行。
