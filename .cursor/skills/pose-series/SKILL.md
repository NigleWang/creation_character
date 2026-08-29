---
name: pose-series
description: >-
  From an approved Tom/James image, lock face, body, outfit, and environment,
  then generate a Xiaohongshu pose series. Two-turn: analyze look + post
  numbered pose options and STOP; generate only after user picks poses. Use
  when user has outputs/approved (or similar) and asks for 系列, 换姿态, 其他pose,
  同一形象, 锁定形象, pose series, or look-lock variants.
---

# Pose Series — Look Lock + New Poses

Sibling of `virtual-couple`. Different job:

| Pipeline | Lock | Change |
|----------|------|--------|
| `virtual-couple` | pose + composition + environment | character identity (换脸) |
| `pose-series` | identity + outfit + environment | pose only (换姿态做系列) |

## ⚠️ TWO-TURN PROTOCOL

| Turn | When | Do | Forbidden |
|------|------|-----|-----------|
| **1** | User points at an existing character image, no pose picks yet | Analyze look-lock + **post numbered pose options** + STOP | GenerateImage |
| **2** | User replies with numbers/text | Write manifest → GenerateImage per pose → QC | — |

Skip Turn 1 only if the first message already lists poses, e.g. `1,3,5` or `伏案工作、看镜头、靠背放松`.

**Mobile/cloud:** AskQuestion may not work. Always post text options in chat.

---

## Turn 1 — Analyze + ask (mandatory)

1. Identify source image (user @path, `outputs/approved/*.png`, or latest approved).
2. Resolve character: `@James` / `@Tom` / filename / visual match. Load bible via `character-registry`.
3. Extract **look-lock** (do not identify random people; this source is already our character):
   - face, hair, glasses, body
   - top / bottom / accessories (exact colors, fit, rolled sleeves, etc.)
   - environment, lighting, camera height, 3:4 framing
   - **current pose** (so options are not duplicates)
4. Write `outputs/drafts/look_lock_<task_id>.json`
5. Read [pose-catalog.md](pose-catalog.md). Pick **6–8 poses** that fit this environment. Drop poses that clash (e.g. beach poses in an office).
6. Reply with the template below. **END turn. Do not call GenerateImage.**

### Turn 1 reply template

```text
✅ 形象已锁定（人物外貌 / 服装 / 场景将保持不变，只换姿态）

【锁定】{Character} · {environment} · {outfit one-liner} · {accessories}

当前姿态：{one sentence}

请选系列姿态（可多选，例如：1,3,5）：

1️⃣ {pose name}：{one-line action}
2️⃣ ...
8️⃣ ...

快捷：「日常三连」({id},{id},{id}) 或「全套」

⏸️ 请回复后我再生成图片。
```

---

## Turn 2 — Generate (after user reply)

1. Parse picks → write `outputs/drafts/pose_series_<task_id>.json` with `"user_confirmed": true`
2. For **each** selected pose (one image per pose, never collage):
   - Build prompt from template below
   - Save `outputs/drafts/prompt_<task_id>_<pose_id>.txt`
   - Call GenerateImage:

```json
namespace: "cursor"
toolName: "GenerateImage"
arguments: {
  "description": "<prompt>",
  "filename": "xiaohongshu_<task_id>_<pose_id>.png",
  "aspect_ratio": "3:4",
  "reference_image_paths": [
    "<source approved image>",
    "<character face ref>"
  ]
}
```

3. QC (pose-series mode) → **mkdir a series folder**, copy accepted files in pick order
4. Deliver: images + brief QC + 小红书系列文案 + **folder path**

### Save paths (mandatory)

| Kind | Where | Filename |
|------|--------|----------|
| **pose-series (一组)** | `outputs/approved/series/<task_id>/` | `01_<pose_id>.png`, `02_<pose_id>.png`, … |
| **single still** | `outputs/approved/` | `xiaohongshu_<task_id>.png` |

Never dump a series as loose files next to singles. Create the folder **before** copying. Number prefix = user pick order (01, 02, …). Keep GenerateImage `filename` as `xiaohongshu_<task_id>_<pose_id>.png` for the tool; after QC, copy/rename into the series folder.

Example:

```text
outputs/approved/xiaohongshu_20260829_tom_studio.png          ← 单图（源成图）
outputs/approved/series/20260829_tom_studio_series/
  01_look_camera.png
  02_phone_call.png
  03_chin_hand.png
```

Default 3 poses if user says 「日常三连」without ids. Max **8** images per turn.

---

## Look-lock schema

```json
{
  "task_id": "20260829_james_office_series",
  "source_image": "outputs/approved/xiaohongshu_20260829_james_office.png",
  "characters": ["james"],
  "lock": {
    "identity": "James bible + source image face/body/hair",
    "outfit": {
      "accessories": [],
      "top": { "type": "button-down", "color": "navy", "detail": "sleeves rolled mid-forearm, tight fit" },
      "bottom": { "type": "dress trousers", "color": "dark grey" }
    },
    "environment": { "location": "office", "details": "...", "lighting": "..." },
    "composition": { "framing": "medium shot", "camera_angle": "slightly low", "aspect_ratio": "3:4" },
    "source_pose": "sitting, arms crossed, gaze to the right"
  }
}
```

## Pose-series manifest (Turn 2)

```json
{
  "task_id": "20260829_james_office_series",
  "user_confirmed": true,
  "source_image": "outputs/approved/xiaohongshu_20260829_james_office.png",
  "selected_poses": ["desk_work", "look_camera", "lean_back"]
}
```

---

## Prompt template (Turn 2)

Same continuous `description` every pose; only the `[NEW POSE]` block changes.

```text
[IDENTITY LOCK — highest priority]

Single recurring virtual character: {Tom or James}.
{identity_prompt from character-registry}

The FIRST reference image is the locked look: copy this exact face, hair,
skin, body build, clothing, and accessories. Do not restyle the outfit.
Do not add or remove glasses unless the locked look already has them.

[ENVIRONMENT LOCK]

Same location as the first reference: {environment.details}.
Same lighting, color grade, furniture, and background clutter.
Same 3:4 vertical framing and similar camera height unless the new pose
requires standing (then keep the same room, pull back slightly).

[NEW POSE — this is the only change]

{pose name}: {catalog action, hands, gaze, weight, chair/desk contact}.
Do not copy the source pose (source was: {source_pose}).

[VISUAL STYLE]

Photorealistic, same texture and lighting as the first reference.
Xiaohongshu cover quality. No text, watermark, or logo.

[CONSTRAINTS]

Preserve: identity, outfit, environment.
Change: body pose, hands, gaze, and micro-expression only.
One person only (unless source is a couple series).
No extra limbs, no face morph, no outfit redesign.
```

**reference_image_paths order:** `[source approved image, characters/<id>/references/face_01.jpeg]`  
Source image is the look-lock; face ref is identity backup.

---

## QC (overrides quality-control "preserve pose")

| Check | Pass |
|-------|------|
| Identity | Same person as source + bible |
| Outfit | Same clothes/colors/fit/accessories |
| Environment | Same room / lighting language |
| Pose | Matches the **chosen** pose, not the source pose |
| Series | Same grade across images in this batch |

`scene_consistency` here means environment lock, **not** pose copy.

`accept` → `outputs/approved/series/<task_id>/` (numbered files)  
`regenerate` → tighten pose/outfit lock, max 1 retry  
`reject` → `outputs/rejected/`

---

## Routing vs virtual-couple

- New **scene photo** + 换脸 → `virtual-couple` (keep pose)
- Existing **approved character still** + 换姿态/系列 → **this skill**
- User wants both new clothes AND new poses → still this skill, but Turn 1 must also post clothing options (reuse `scene-customizer` template) before generating

## Sub-skills

- `character-registry` — identity prompt + face path
- `quality-control` — use pose-series QC table above
- `xiaohongshu-post` — series caption (`1/n` in title ok)
