# Metadata Schema

Markdown 是 canonical source of truth；YAML front matter 为文档提供可检查的 metadata。

## Canonical Schema v1

```yaml
schema_version: 1              # 新文件建议使用；旧文件兼容
id: optional-stable-id         # 可选稳定标识
type: required                 # 所有 AI_CONTEXT Markdown 必填
scope: global | project/...    # operational file 必填
status: active | deprecated    # operational file 必填；validator 兼容更多历史状态
last_updated: YYYY-MM-DD       # operational file 建议填写
last_reviewed: YYYY-MM-DD      # 可选
trust_level: optional          # 可选
```

## Compatibility

- 缺少 `schema_version` 的旧文档会得到 `FM100` info，不会因此失败。
- 非法 `type`、`status` 或日期仍是 error。
- `status: active` 且超过 stale threshold 的文档是 review warning，不等于 schema failure。
- 不应为了消除 warning 机械刷新 `last_updated`；只有内容实际 review 或更新后才修改日期。
