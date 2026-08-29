---
name: virtual-couple
description: >-
  Xiaohongshu virtual couple pipeline for Tom (受) and James (攻). ALWAYS uses
  two-turn protocol: Turn 1 analyze scene and post numbered style options in
  chat; Turn 2 generate after user replies. Use when user uploads scene photo,
  @mentions Tom, James, virtual-couple, 换脸, or 小红书 in creation_character.
---

# Virtual Couple Studio

## ⚠️ TWO-TURN PROTOCOL (read first)

| Turn | When | Do | Forbidden |
|------|------|-----|-----------|
| **1** | User uploads scene, no style choices yet | Analyze + **post numbered text options** + STOP | GenerateImage |
| **2** | User replies with choices | Write manifest → GenerateImage → QC | — |

Skip Turn 1 only if user's first message includes e.g. `全部保持原场景` or `角色默认，上衣藏青`.

**Mobile/cloud:** AskQuestion does NOT work. Always post text options in chat.

---

## Turn 1 — Ask (mandatory unless choices pre-specified)

After analyzing scene, reply with this exact structure:

```text
✅ 场景已分析（构图/动作/环境将保持不变）

换脸前请确认（回复数字或文字）：

【James】（单人时只列此块；情侣加 Tom 块）
1️⃣ 装饰物：1保持原场景({value}) 2角色默认 3墨镜 4耳机 5无装饰
2️⃣ 上衣颜色：1保持({value}) 2白 3藏青 4浅蓝 5黑
3️⃣ 上衣图案：1保持 2纯色 3条纹 4格子
4️⃣ 下装颜色：1保持({value}) 2黑 3灰 4藏青

快捷：「全部保持原场景」

⏸️ 请回复后我再生成图片。
```

**Then END this turn. Do not call GenerateImage.**

Character defaults: Tom → browline glasses; James → no glasses.

---

## Turn 2 — Generate (after user reply)

1. Parse user reply → write `outputs/drafts/customization_<task_id>.json` with `"user_confirmed": true`
2. Load characters from `characters/tom/`, `characters/james/`
3. Build prompt (include customization choices)
4. Call `GenerateImage` via CallDynamicTool:

```json
namespace: "cursor"
toolName: "GenerateImage"
arguments: {
  "description": "<prompt>",
  "filename": "xiaohongshu_<task_id>.png",
  "aspect_ratio": "3:4",
  "reference_image_paths": ["<scene>", "<character refs>"]
}
```

5. QC → save to `outputs/approved/` → caption + hashtags

---

## Characters

| Name | Role | Side | Reference |
|------|------|------|-----------|
| Tom | 受 | left | `characters/tom/references/face_01.jpeg` |
| James | 攻 | right | `characters/james/references/face_01.jpeg` |

## Rules

```
Character = IDENTITY (face, body, hair)
Scene = COMPOSITION + POSE + ENVIRONMENT
Customization = accessories/clothing (user confirms, may differ from scene)
LEFT = Tom | RIGHT = James — never swap
```

## Sub-skills (Turn 2 detail)

- `character-registry`, `scene-analyzer`, `scene-customizer`, `character-composer`, `prompt-builder`, `quality-control`, `xiaohongshu-post`

See also: `AGENTS.md` at project root.
