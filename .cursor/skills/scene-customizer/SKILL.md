---
name: scene-customizer
description: >-
  Turn 1 style gate for the photoreal swap pipeline. Posts numbered text
  options for accessories, clothing colors, patterns in chat and STOPS —
  never generates in the same turn. Cast is Teo/Kai, or 小川/大海 when the
  user named those references. Use with virtual-couple when the user uploads
  a scene on mobile or cloud. GenerateImage forbidden until the user replies.
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

| Character | Default accessory | 角色默认服装（只有用户这么说才用） |
|-----------|-------------------|--------------------------------------|
| Teo | browline glasses | 不在这里改职业装 |
| Kai | no glasses | 不在这里改职业装 |
| 小川 | no glasses | 深灰圆领 T |
| 大海 | no glasses | 橄榄绿工装衬衫、黑工装裤、棕色工装靴 |

区块标题用当前 cast 的名字。双人两块都写。不要在小川/大海的选项里出现 Teo/Kai。

## After user replies

Write `outputs/drafts/customization_<task_id>.json`:

```json
{
  "user_confirmed": true,
  "kai": {
    "accessories": { "choice": "character_default" },
    "top": { "choice": "navy", "pattern": "solid" },
    "bottom": { "choice": "grey", "pattern": "solid" }
  }
}
```

JSON 的角色键用当前 cast：`teo` / `kai`，或 `ogawa` / `dahai`。不要把小川写成 `kai`。

Then hand off to prompt-builder → GenerateImage (Turn 2 only).

## Skip gate

User's first message already contains: `全部保持原场景` or explicit per-item choices.
