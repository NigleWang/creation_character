# Generate Couple Xiaohongshu Post

**Trigger:** `@virtual-couple` + scene upload + `@Teo` `@Kai`

## Steps

1. Save scene to `scenes/scene_<timestamp>.jpg`
2. Run pipeline per `@virtual-couple` skill
3. **Agent 在聊天里发编号选项**（手机/Cloud 无弹窗，需文字回复）— 确认后再生图
4. Deliver approved image + caption

## Example user message (mobile)

```text
@virtual-couple @Teo @Kai
[上传场景图]
情侣咖啡馆日常，保持构图，小红书竖图
```

## Expected output

- Single: `outputs/approved/xiaohongshu_<task_id>.png`
- pose-series: `outputs/approved/series/<task_id>/01_<pose_id>.png`
- QC scores
- 标题 + 正文 + 标签
