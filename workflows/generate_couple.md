# Generate Couple Xiaohongshu Post

**Trigger:** `@virtual-couple` + scene upload + `@Tom` `@James`

## Steps

1. Save scene to `scenes/scene_<timestamp>.jpg`
2. Run pipeline per `@virtual-couple` skill
3. Deliver approved image + caption

## Example user message (mobile)

```text
@virtual-couple @Tom @James
[上传场景图]
情侣咖啡馆日常，保持构图，小红书竖图
```

## Expected output

- `outputs/approved/xiaohongshu_<task_id>.png`
- QC scores
- 标题 + 正文 + 标签
