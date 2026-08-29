---
name: text-scene
description: >-
  From a text scene brief (no photo), expand a complete Xiaohongshu scene using
  Tom and James character bibles, then generate one image after the user
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
2. Parse who is in frame: `@Tom` / `@James` / 两人 / 我们. Default **couple** if unspecified and the brief is 日常/约会; default the @mentioned person if only one name.
3. Fill every gap using the checklist below. User text **overrides** defaults. Bibles override any request that would swap faces, drop Tom's glasses, or bulk Tom up.
4. Write `outputs/drafts/text_scene_<task_id>.json` with `"user_confirmed": false`.
5. Reply with the card. **END. Do not call GenerateImage.**

### Gap-fill checklist

| Slot | If user omitted | Default |
|------|-----------------|---------|
| Who | — | Couple, Tom left / James right |
| Place | — | Match occupation or 居家 |
| Time | — | Late afternoon unless 夜/晨 specified |
| Light | — | Natural/cinematic, 小红书封面 |
| Tom pose | — | Softer, receiving, still, looking through glasses |
| James pose | — | Leading, upright or leaning in, initiating contact |
| Tom clothes | — | Occupation or scene: linen/neutral; **always browline glasses** |
| James clothes | — | Occupation or scene: shirt, no glasses |
| Props | — | 1–2 that belong to the place (样品 / 双屏 / 杯子) |
| Framing | — | 3:4 medium, faces in upper two-thirds |
| Tone | — | Intimate, tasteful, not explicit |

Do not add extra people. Do not put Tom in James's fluorescent cubicle unless the brief says so (or the reverse for Tom's studio).

### Turn 1 reply template

```text
✅ 场景已按人设补全（构图/动作如下，可改）

【谁】{双人 Tom左 James右 / 仅Tom / 仅James}
【时间地点】{...}
【构图】3:4 {中景/近景}，{机位}
【动作】Tom：{...} ｜ James：{...}
【服装】Tom：{眼镜+}{上衣/下装} ｜ James：{上衣/下装}
【光与道具】{...}
【人设】{一句：受/攻能量、职业细节}

改法直接说，例如：改成只有Tom、James穿藏青衬衫、再近一点。
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
  "reference_image_paths": ["<tom face if in frame>", "<james face if in frame>"]
}
```

No scene photograph in `reference_image_paths`. Face refs only.

4. QC → `outputs/approved/xiaohongshu_<task_id>.png` (single still, not a series folder).
5. Caption via `xiaohongshu-post` (单人帖用对方第一人称).

After this still exists, 换姿态 → `pose-series`.

---

## Prompt (Turn 2)

```text
[CHARACTER IDENTITY — highest priority]

{If couple:} Two recurring virtual East Asian men. LEFT is Tom (受): {tom identity_prompt}. RIGHT is James (攻): {james identity_prompt}.
{If single:} Only {Tom or James}: {identity_prompt}. One person.

Use attached face references. Tom: browline glasses, buzz cut, slim athletic, not bulky. James: spiky hair, mature, muscular, no glasses. Do not swap them. Do not merge faces.

[SCENE — filled brief]

{place}, {time}. {lighting}.
{environment details and props}.

[COMPOSITION]

Vertical 3:4. {framing}. {camera}.
Tom on the left, James on the right (if both). Faces in the upper two-thirds.

[POSE]

Tom: {filled pose}. James: {filled pose}.
{interaction}. Tasteful, natural, not staged-glamour.

[CLOTHING]

Tom: {filled}. James: {filled}.

[VISUAL STYLE]

Photorealistic, cinematic film, Xiaohongshu cover. No text, watermark, logo.

[CONSTRAINTS]

Identity from references. One frame, correct headcount. No extra limbs. No 总裁秘书 costume unless the user asked.
```

---

## JSON schema

```json
{
  "task_id": "20260829_weekend_kitchen",
  "user_confirmed": false,
  "user_brief": "周末早上两个人在厨房",
  "cast": ["tom", "james"],
  "scene": {
    "place": "home kitchen",
    "time": "weekend morning",
    "lighting": "soft window light",
    "framing": "medium 3:4",
    "tom": { "pose": "...", "clothes": "..." },
    "james": { "pose": "...", "clothes": "..." },
    "props": [],
    "interaction": "James cooking, Tom leaning on counter watching"
  }
}
```

## Sub-skills

`character-registry`, `character-composer` (left/right), `quality-control`, `xiaohongshu-post`

See [examples.md](examples.md).
