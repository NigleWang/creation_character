---
name: scene-customizer
description: >-
  Before face-swap generation, extracts customizable style elements from the scene
  and asks the user to choose accessories, clothing colors, and patterns that
  may differ from the reference. Use after scene-analyzer, before prompt-builder
  and GenerateImage in creation_character.
---

# Scene Customizer — 换脸前差异化询问

## Purpose

Generated images must **preserve pose/composition/environment** from the scene, but **may differ** in styling details. Before calling GenerateImage, **stop and ask the user** to confirm customization choices.

## When to run

After `scene-analyzer`, before `prompt-builder` and `GenerateImage`.

**Do NOT generate images until the user confirms customization choices** (or explicitly says「全部保持原场景 / 默认」).

## What CAN change (vs scene reference)

| Category | Examples |
|----------|----------|
| 装饰物 accessories | 墨镜、眼镜、耳机、帽子、项链、手表 |
| 衣服颜色 clothing color | 上衣/下装/外套颜色 |
| 图案 pattern | 纯色、条纹、格子、logo、印花 |
| 材质 texture | 棉、亚麻、皮革、针织 |
| 款式细节 style detail | 领口、袖长、扣开/扣合（保持同类服装） |

## What MUST NOT change

- 构图、镜头角度、人物位置（左 Tom / 右 James）
- 动作、姿势、互动关系
- 环境、背景、光影逻辑
- 角色脸部身份（Tom/James face from reference）

## Step 1 — Extract customizable elements

From `scene_blueprint`, build `customizable_elements` per character:

```json
{
  "customizable_elements": {
    "tom": {
      "accessories": ["sunglasses"],
      "top": { "type": "tank top", "color": "white", "pattern": "ribbed" },
      "bottom": { "type": "shorts", "color": "black", "pattern": "solid" }
    },
    "james": {
      "accessories": ["sunglasses"],
      "top": { "type": "linen shirt", "color": "white", "pattern": "solid", "detail": "unbuttoned" },
      "bottom": { "type": "shorts", "color": "black", "pattern": "solid" }
    }
  }
}
```

Also note **character identity defaults** that should appear as recommended options:

| Character | Identity default |
|-----------|------------------|
| Tom | browline glasses（角色设定，推荐） |
| James | no glasses（角色设定） |

## Step 2 — Ask user (required)

**Customization gate is mandatory on ALL platforms** (desktop, mobile, cloud).  
**Do NOT call GenerateImage in the same turn** — stop and wait for the user's next message.

### Platform behavior (important)

| Platform | How to ask |
|----------|------------|
| **Mobile / Cloud** | **Text inquiry only** — post numbered options in chat (see template below). AskQuestion often does NOT render; never rely on it alone. |
| **Desktop** | Try AskQuestion if available; **always also post the same text options** as fallback so user can reply with numbers. |

If unsure which platform → use **text inquiry** (works everywhere).

### Text inquiry template (mobile/cloud — primary method)

After scene analysis, reply with a compact numbered menu. User replies with numbers or short text.

```text
✅ 场景构图/动作/环境已分析（将保持不变）

换脸前请确认装饰与服装（可与原场景不同）。直接回复数字或文字即可：

【James】
1️⃣ 装饰物：1保持原场景(___) 2角色默认(无眼镜) 3墨镜 4耳机 5无装饰
2️⃣ 上衣颜色：1保持(___) 2白 3藏青 4浅蓝 5黑
3️⃣ 上衣图案：1保持 2纯色 3条纹 4格子
4️⃣ 下装颜色：1保持(___) 2黑 3灰 4藏青

快捷：回复「全部保持原场景」或「角色默认+藏青上衣+灰裤」

⚠️ 确认后我再生成图片。
```

For couple scenes, add Tom block with same format. For single character, only list that character.

**Rules for text inquiry:**
- Fill in `___` with values detected from scene
- Keep it scannable on a phone screen (short lines, emoji numbers ok)
- End with explicit「确认后我再生成」so user knows to reply
- **STOP — do not generate until user replies**

### AskQuestion (desktop optional enhancement)

May use AskQuestion in addition to text, never instead of text on mobile/cloud.

**Accessories (per character):**
- 保持原场景（{scene_value}）
- 角色默认（Tom→眉框眼镜 / James→无）
- 墨镜
- 不佩戴装饰
- 耳机（头戴式）
- 其他（用户下一条消息说明）

**Top color:**
- 保持原场景（{color}）
- 白 / 黑 /  navy 藏青 / 浅蓝 / 米杏 / 其他

**Top pattern:**
- 保持原场景
- 纯色 / 条纹 / 格子 / 无图案

**Bottom color / pattern:** same pattern as top.

### Example AskQuestion batch (couple scene)

```
Q1 tom_accessories: Tom 装饰物？
Q2 james_accessories: James 装饰物？
Q3 tom_top_color: Tom 上衣颜色？
Q4 james_top_color: James 上衣颜色？
Q5 tom_top_pattern: Tom 上衣图案？
Q6 james_top_pattern: James 上衣图案？
Q7 tom_bottom_color: Tom 下装颜色？
Q8 james_bottom_color: James 下装颜色？
```

For single-character scenes, only ask for that character.

If scene has no accessories, still offer accessory options (用户可能想加差异化元素).

## Step 3 — User shortcuts

If user message already contains explicit choices, skip AskQuestion and parse directly:

| User says | Action |
|-----------|--------|
| 全部保持原场景 / 默认 / 跟场景一样 | All fields → `keep_scene` |
| Tom 戴耳机，衣服换成 navy | Parse per-character overrides |
| 不要墨镜，Tom 用眼镜 | Apply to customization_manifest |

If ambiguous, use **text inquiry** (not AskQuestion alone). On mobile/cloud, text inquiry is mandatory.

## Step 4 — Write customization_manifest

Save to `outputs/drafts/customization_<task_id>.json`:

```json
{
  "task_id": "20260829_001",
  "user_confirmed": true,
  "tom": {
    "accessories": { "choice": "browline_glasses", "source": "character_default" },
    "top": { "choice": "keep_scene", "scene_value": "white ribbed tank top" },
    "bottom": { "choice": "navy", "pattern": "solid" }
  },
  "james": {
    "accessories": { "choice": "sunglasses", "source": "keep_scene" },
    "top": { "choice": "light_blue", "pattern": "solid", "detail": "unbuttoned linen shirt" },
    "bottom": { "choice": "keep_scene" }
  },
  "differentiation_note": "Intentionally differs from scene in listed fields only."
}
```

`choice` values: `keep_scene` | `character_default` | specific value (e.g. `navy`, `headphones`, `no_accessories`)

## Step 5 — Handoff

Pass `customization_manifest` to **prompt-builder**. Only then proceed to GenerateImage.

## Reply before asking

Post **text inquiry** in chat (required on mobile/cloud). Optionally also try AskQuestion on desktop.

```text
✅ 场景构图与动作已分析（将保持不变）。换脸前请确认以下选项：
[numbered menu per character]
确认后我再生成图片。
```

Do NOT generate in this turn.
