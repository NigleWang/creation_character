---
name: text-scene
description: >-
  From a text scene brief (no photo), expand a complete Xiaohongshu scene
  using the active photoreal bibles, then generate one image after the user
  confirms. Default cast is Teo and Kai. If the brief names 小川, 大海,
  characters/小川, or characters/大海, use that cast instead. Use for 文字场景,
  场景需求, 按人设出图, 完善场景, 没有参考图, or a written prompt. Do not use
  for Tagame — that is tagame-anime.
---

# Text Scene — Brief → Complete → One Image

首先按照用户的场景需求（文字）完善场景，然后再生成一张图片。

No scene photo. Identity comes from character bibles + face refs.

| Pipeline | Input | First action |
|----------|--------|----------------|
| `virtual-couple` | 场景**照片** | 换脸服装选项 |
| `pose-series` | 已有成图 | 姿态选项 |
| **`text-scene`** | **文字**场景（Teo/Kai） | **补全场景卡，停** |
| `tagame-anime` | @Tagame / 动漫上司 | 动漫场景卡 → 静帧 → 台词选项 → 10s 视频词 → 抖音文案 |

**Route out:** @Tagame → `tagame-anime`（动漫画风，禁止走本 skill 的写实提示词）。

## Cast

没点小川或大海 → Teo 左 / Kai 右，下面的 Teo/Kai 默认值照用。  
点了小川或大海 → 只用这一对。左小川，右大海。参考图是设定表，`reference_image_paths` 只放被点名的那张或两张，不要再放 Teo/Kai 脸图。提示词禁止灰底分格和印刷文字。

小川/大海的空缺默认：

| Slot | Default |
|------|---------|
| Who | 双人，小川左 / 大海右。只点一个名字就单人 |
| Place | 用户写的地方；没写就普通居家或街边，不要设计工作室，也不要健康科技办公室 |
| 小川 pose | 静，表情少。不要写成被搂的受 |
| 大海 pose | 站得稳。不要自动加搂肩 |
| 小川 clothes | 深灰圆领 T，无眼镜 |
| 大海 clothes | 橄榄绿工装衬衫，黑工装裤，棕色工装靴，无眼镜 |
| 人设句 | 小川安静，大海厚实可靠。不写受/攻 |

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
2. Parse who is in frame. 小川/大海优先于 Teo/Kai。这一对里只点了一个名字就单人。两个 cast 都点了就停下问。Teo/Kai：`@Teo` / `@Kai` / 两人 / 我们；没点名且是日常/约会时默认双人。
3. Fill every gap. 小川/大海用上面的 Cast 表，不要用 Teo 的眼镜或 Kai 的职业。User text **overrides** defaults. Bibles override a request that would swap faces, drop Teo's glasses, bulk Teo or 小川 up, or slim 大海 down.
4. Write `outputs/drafts/text_scene_<task_id>.json` with `"user_confirmed": false`.
5. Reply with the card. **END. Do not call GenerateImage.**

### Gap-fill checklist

| Slot | If user omitted | Default |
|------|-----------------|---------|
| Who | — | Couple, Teo left / Kai right |
| Place | — | Match occupation or 居家 |
| Time | — | Late afternoon unless 夜/晨 specified |
| Light | — | Natural indoor, match real room brightness — not cover-bright, not cinematic glow; uneven shadows OK (`docs/light.md`) |
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

【谁】{双人 Teo左 Kai右 / 仅Teo / 仅Kai / 双人 小川左 大海右 / 仅小川 / 仅大海}
【时间地点】{...}
【构图】3:4 {中景/近景}，{机位}
【动作】{左}：{...} ｜ {右}：{...}
【服装】{左}：{...} ｜ {右}：{...}
【光与道具】{...}
【人设】{Teo/Kai：受/攻与职业。小川/大海：安静 / 厚实可靠，不写受攻}

改法直接说，例如：改成只有小川、大海穿白衬衫、再近一点。
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
  "reference_image_paths": ["<face ref or character sheet for each person in frame>"]
}
```

No scene photograph in `reference_image_paths`. Face refs only.

4. QC → `outputs/approved/xiaohongshu_<task_id>.png` (single still, not a series folder).
5. Caption via `xiaohongshu-caption`.
6. 按下面「Cloud 客户端显示」嵌图。`outputs/` 只作归档，不拿来当预览图。

**Pre-publish:** pass `quality-control` anti-AI gate before save.

After this still exists, 换姿态 → `pose-series`.

---

## Prompt (Turn 2)

```text
[CHARACTER IDENTITY — highest priority]

{If teo_kai couple:} Two recurring virtual East Asian men. LEFT is Teo (受): {teo identity_prompt}. RIGHT is Kai (攻): {kai identity_prompt}.
{If ogawa_dahai couple:} Two recurring photoreal East Asian men. LEFT is 小川: {ogawa identity_prompt}. RIGHT is 大海: {dahai identity_prompt}. Not a 受/攻 script.
{If single:} Only {named person}: {identity_prompt}. One person.

Use the attached references for identity only. Teo: browline glasses, buzz cut, slim athletic. Kai: spiky hair, muscular, no glasses. 小川: neat crop, light stubble, no glasses, not stocky. 大海: short beard, stocky muscle, no glasses. Do not copy a character-sheet studio. Do not swap them. Do not merge faces. Do not mix the two casts.

[SCENE — filled brief]

{place}, {time}.
{environment details and props}.

[LIGHTING]

{lighting}. Natural room light at real exposure — do not brighten for a cover look.
Do not add beauty lighting, rim glow, HDR, or even studio fill. Keep shadows uneven.
Over-bright or glowing light looks AI-generated — forbidden.
Preserve plausible clutter and surface reflections for this place.

[COMPOSITION]

Vertical 3:4. {framing}. {camera}.
Locked sides if both: Teo left / Kai right, or 小川 left / 大海 right. Faces in the upper two-thirds.

[POSE]

Left person: {filled pose}. Right person: {filled pose}.
{interaction}. Tasteful, natural, not staged-glamour.

[CLOTHING]

Left person: {filled}. Right person: {filled}.

[VISUAL STYLE]

Photorealistic natural photography, not cinematic glow. Xiaohongshu cover.
Same grain and contrast as a real phone photo in this room. No text, watermark, logo.

[REALISM — reduce AI look]

natural available light, soft uneven lighting, slightly imperfect exposure,
natural skin texture, subtle photographic grain, unretouched photographic look,
not overly sharp, not airbrushed. See docs/light.md §6.

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

## Cloud 客户端显示

手机端 / 远程 Cloud 不会自动贴出 `GenerateImage` 卡片。最终回复里这张图单独一行 Markdown，只用一个路径。不要只写「路径在 xxx」，不要用 HTML `<img>`，不要再嵌一条备用路径。

不要 embed `outputs/`（含 `/workspace/outputs/approved/…`）或 `/home/ubuntu/.cursor/projects/…/assets/…`。

1. 归档到 `outputs/approved/xiaohongshu_<task_id>.png`。磁盘上是 JPEG 时用 Pillow 转成真 PNG，禁止 `cp` 改后缀。
2. 再复制到 `/workspace/artifacts/`（本地是仓库根 `artifacts/`，不提交）。扩展名跟二进制走：文件头 `FF D8` 用 `.jpg`，`89 50 4E 47` 用 `.png`。
3. 回复嵌工具已经写入的 `/opt/cursor/artifacts/assets/` 路径（通常是 `.jpg`）。该目录不存在时，改嵌第 2 步的绝对路径。

```markdown
![成图](/opt/cursor/artifacts/assets/xiaohongshu_<task_id>.jpg)
```

## Sub-skills

`character-registry`, `character-composer` (left/right), `quality-control`, `xiaohongshu-caption`

See [examples.md](examples.md).
