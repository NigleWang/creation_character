---
name: text-scene
description: >-
  From a text scene brief (no photo), expand a complete Xiaohongshu scene using
  Teo and Kai character bibles, then generate one image after the user
  confirms. Use when the user describes a scene in words, 文字场景, 场景需求,
  按人设出图, 完善场景, 没有参考图, or asks to generate from a written prompt.
---

# Text Scene — Brief → Complete → One Image

首先按照用户的场景需求（文字）完善场景，然后再生成一张图片。

No scene photo. Identity comes from character bibles + face refs.

| Pipeline | Input | First action |
|----------|--------|----------------|
| `virtual-couple` | 场景**照片** | 换脸服装选项 |
| `pose-series` | 已有成图 | 姿态选项 |
| **`text-scene`** | **文字**场景 | **补全场景卡，停** |

## ⚠️ TWO-TURN PROTOCOL

| Turn | When | Do | Forbidden |
|------|------|-----|-----------|
| **1** | User sent a text brief, has not confirmed the filled scene | Load bibles → **fill gaps** → post scene card → STOP | GenerateImage |
| **2** | User replies `生成` / `可以` / 修改意见 | Write blueprint → GenerateImage **one** still → QC | — |

Skip wait only if the **same** first message already says `直接生成` or `不用确认` **and** includes a usable brief — still post the filled card in that reply, then generate.

**Mobile/cloud:** post the card in chat. AskQuestion may not work.

---

## Turn 1 — 完善场景

1. Load `character-registry` (bibles + yaml, including **occupation**).
2. Parse who is in frame: `@Teo` / `@Kai` / 两人 / 我们. Default **couple** if unspecified and the brief is 日常/约会; default the @mentioned person if only one name.
3. Fill every gap using the checklist below. User text **overrides** defaults. Bibles override any request that would swap faces, drop Teo's glasses, or bulk Teo up.
4. Write `outputs/drafts/text_scene_<task_id>.json` with `"user_confirmed": false`.
5. Reply with the card. **END. Do not call GenerateImage.**

### Gap-fill checklist

| Slot | If user omitted | Default |
|------|-----------------|---------|
| Who | — | Couple, Teo left / Kai right |
| Place | — | Match occupation or 居家 |
| Time | — | Late afternoon unless 夜/晨 specified |
| Light | — | Natural indoor, match real room brightness — not cover-bright, not cinematic glow |
| Teo pose | — | Softer, receiving, still, looking through glasses |
| Kai pose | — | Leading, upright or leaning in, initiating contact |
| Teo clothes | — | Occupation or scene: linen/neutral; **always browline glasses** |
| Kai clothes | — | Occupation or scene: shirt, no glasses |
| Props | — | 1–2 that belong to the place (样品 / 双屏 / 杯子) |
| Framing | — | 3:4 medium, faces in upper two-thirds |
| Tone | — | Intimate, tasteful, not explicit |

Do not add extra people. Do not put Teo in Kai's fluorescent cubicle unless the brief says so (or the reverse for Teo's studio).

### Turn 1 reply template

```text
✅ 场景已按人设补全（构图/动作如下，可改）

【谁】{双人 Teo左 Kai右 / 仅Teo / 仅Kai}
【时间地点】{...}
【构图】3:4 {中景/近景}，{机位}
【动作】Teo：{...} ｜ Kai：{...}
【服装】Teo：{眼镜+}{上衣/下装} ｜ Kai：{上衣/下装}
【光与道具】{...}
【人设】{一句：受/攻能量、职业细节}

改法直接说，例如：改成只有Teo、Kai穿藏青衬衫、再近一点。
快捷：「生成」

⏸️ 请确认后再出图。
```

---

## Turn 2 — 生成一张

1. Merge user edits into `outputs/drafts/text_scene_<task_id>.json` with `"user_confirmed": true`.
2. Save prompt to `outputs/drafts/prompt_<task_id>.txt`.
3. Call GenerateImage **once** (`aspect_ratio` `3:4`):

```json
namespace: "cursor"
toolName: "GenerateImage"
arguments: {
  "description": "<prompt>",
  "filename": "xiaohongshu_<task_id>.png",
  "aspect_ratio": "3:4",
  "reference_image_paths": ["<teo face if in frame>", "<kai face if in frame>"]
}
```

No scene photograph in `reference_image_paths`. Face refs only.

4. QC → `outputs/approved/xiaohongshu_<task_id>.png` (single still, not a series folder).
5. Caption via `xiaohongshu-caption`.

After this still exists, 换姿态 → `pose-series`.

---

## Prompt (Turn 2)

```text
[CHARACTER IDENTITY — highest priority]

{If couple:} Two recurring virtual East Asian men. LEFT is Teo (受): {teo identity_prompt}. RIGHT is Kai (攻): {kai identity_prompt}.
{If single:} Only {Teo or Kai}: {identity_prompt}. One person.

Use attached face references. Teo: browline glasses, buzz cut, slim athletic, not bulky. Kai: spiky hair, mature, muscular, no glasses. Do not swap them. Do not merge faces.

[SCENE — filled brief]

{place}, {time}.
{environment details and props}.

[LIGHTING]

{lighting}. Natural room light at real exposure — do not brighten for a cover look.
Do not add beauty lighting, rim glow, HDR, or even studio fill. Keep shadows.
Over-bright or glowing light looks AI-generated — forbidden.

[COMPOSITION]

Vertical 3:4. {framing}. {camera}.
Teo on the left, Kai on the right (if both). Faces in the upper two-thirds.

[POSE]

Teo: {filled pose}. Kai: {filled pose}.
{interaction}. Tasteful, natural, not staged-glamour.

[CLOTHING]

Teo: {filled}. Kai: {filled}.

[VISUAL STYLE]

Photorealistic natural photography, not cinematic glow. Xiaohongshu cover.
Same grain and contrast as a real phone photo in this room. No text, watermark, logo.

[CONSTRAINTS]

Identity from references. One frame, correct headcount. No extra limbs. No 总裁秘书 costume unless the user asked.
Do not overexpose or make the scene look brighter than a real indoor photograph.
```

---

## JSON schema

```json
{
  "task_id": "20260829_weekend_kitchen",
  "user_confirmed": false,
  "user_brief": "周末早上两个人在厨房",
  "cast": ["teo", "kai"],
  "scene": {
    "place": "home kitchen",
    "time": "weekend morning",
    "lighting": "soft window light, natural indoor exposure, not bright",
    "framing": "medium 3:4",
    "teo": { "pose": "...", "clothes": "..." },
    "kai": { "pose": "...", "clothes": "..." },
    "props": [],
    "interaction": "Kai cooking, Teo leaning on counter watching"
  }
}
```

## Sub-skills

`character-registry`, `character-composer` (left/right), `quality-control`, `xiaohongshu-caption`

See [examples.md](examples.md).
