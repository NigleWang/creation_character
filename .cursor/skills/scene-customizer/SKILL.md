---
name: scene-customizer
description: >-
  Turn 1 style gate for virtual couple pipeline. Posts numbered text options
  for accessories, clothing colors, patterns in chat and STOPS — never generates
  in same turn. Use with virtual-couple when user uploads scene on mobile or
  cloud. GenerateImage forbidden until user replies.
---

# Scene Customizer — Turn 1 Style Gate

## Single job

**Post text options. Stop. Wait for user reply.**

Do NOT call GenerateImage. Do NOT write `user_confirmed: true` until user has replied.

## Output in chat (required)

Fill `{value}` from detected scene. One block per character.

```text
✅ 场景已分析（构图/动作/环境将保持不变）

【{Character}】
1️⃣ 装饰物：1保持原场景({value}) 2角色默认 3墨镜 4耳机 5无装饰
2️⃣ 上衣颜色：1保持({value}) 2白 3藏青 4浅蓝 5黑
3️⃣ 上衣图案：1保持 2纯色 3条纹 4格子
4️⃣ 下装颜色：1保持({value}) 2黑 3灰 4藏青

⏸️ 请回复后我再生成图片。
```

## Character defaults

| Character | Default accessory |
|-----------|-------------------|
| Tom | browline glasses |
| James | no glasses |

## After user replies

Write `outputs/drafts/customization_<task_id>.json`:

```json
{
  "user_confirmed": true,
  "james": {
    "accessories": { "choice": "character_default" },
    "top": { "choice": "navy", "pattern": "solid" },
    "bottom": { "choice": "grey", "pattern": "solid" }
  }
}
```

Then hand off to prompt-builder → GenerateImage (Turn 2 only).

## Skip gate

User's first message already contains: `全部保持原场景` or explicit per-item choices.
