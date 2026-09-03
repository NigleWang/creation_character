---
name: gemini-video
description: >-
  From a Teo/Kai still (solo or couple), writes a 10-second Gemini
  image-to-video prompt with dense Japanese kana dialogue (first line at 2s,
  Douyin hook), copy-paste ready for Gemini. Use when the user asks for
  图生视频, 视频提示词, Gemini视频, 10秒视频, i2v, Veo, Omni, image-to-video,
  or to animate an approved still.
---

# Gemini Video — Still → 10s Copy-Paste Prompt

从一张 **Teo / Kai / 两人** 的场景成图，写出可直接粘贴进 **Gemini** 的 **10 秒图生视频**提示词。台词必须是 **日语假名**（ひらがな / カタカナ，不用汉字）。

本 skill **只写提示词**。不要调用 `GenerateImage`。不要走 virtual-couple / pose-series / text-scene。

| Pipeline | Input | Output |
|----------|--------|--------|
| `virtual-couple` | 换脸场景照片 | 静帧图 |
| `pose-series` | 成图换姿态 | 系列静帧 |
| **`gemini-video`** | **成图（静帧）** | **Gemini 10s 视频提示词** |

优先用 `outputs/approved/` 里已经是 Teo/Kai 的成图。原场景未换脸图会把原图人物动起来，身份会漂。

---

## When to run

User uploaded / @ 了一张图，并提到：图生视频 / 视频提示词 / Gemini / 10秒 / i2v / Veo / Omni / 把这张动起来.

If they also asked to 换脸 or 出图: finish that pipeline first, then run this on the **approved still**.

---

## Workflow (one shot)

1. Identify the still (user @path, upload, or latest `outputs/approved/*.png`).
2. Load `character-registry` for whoever is in frame.
3. Read the image. Extract: who, place, current pose, lighting, props, mood. Do **not** identify random people on unswapped scene photos — if it is not yet our characters, say so and ask for an approved still.
4. Resolve cast:

| In frame | Cast |
|----------|------|
| one man, glasses + buzz | Teo only |
| one man, spiky + muscular, no glasses | Kai only |
| two men | Teo left / Kai right unless user says otherwise |
| user @Teo / @Kai | honor @mention |

5. Invent a **10s continuation** of this exact still (same room, clothes, faces). Write **dense 假名** lines that fit occupation + 受/攻. **Douyin hook:** first spoken line starts at **2.0s** — never open with silent eye contact.
6. **Sanitize for Gemini** (see Safety below). If the still is kneeling / floor / shoes / close body contact, recast motion + 台词 as an everyday task before writing the paste block.
7. Save:
   - `outputs/drafts/video_prompt_<task_id>.json`
   - `outputs/drafts/video_prompt_<task_id>.txt` (the paste block only)
8. Reply with the template below. Put the Gemini block in **one** fenced `text` code block so the user can copy it whole.

If the user already gave 台词 / 情绪 / 动作, use those (still convert 台词 to 假名) — **except** loaded grip/tightness/won't-let-go lines, which must be recast per Safety.

---

## Reply template

Chat order (do not put Chinese instructions inside the copy fence):

1. Header in Chinese (usage + who + motion + 假名台词)
2. One `text` code fence = **only** the English Gemini prompt (copy-paste body)
3. One closing line in Chinese

Header:

```
✅ 10秒图生视频提示词已写好（身份/服装/场景锁定成图，只加动作和声音）

【用法】打开 Gemini → 上传这张成图 → 粘贴下面英文块 → 生成视频（时长选 10s / 竖屏）

【谁】{仅Teo / 仅Kai / 双人 Teo左 Kai右}
【从静止到动作】{一句}
【台词（假名）】第一条 @2.0s
{Name}：「{kana}」
{Name}：「{kana}」
{Name}：「{kana}」

【复制到 Gemini】
```

Closing line after the fence: `改法直接说，例如：台词改成加班、不要对白只要呼吸、镜头再近一点。`

---

## Gemini paste template

Write the paste block in **English** (motion/camera/audio). Spoken lines stay **kana inside ASCII double quotes**. One continuous prompt, no markdown headings inside the paste (use CAPS labels).

```text
Animate the uploaded image into a photorealistic 10-second video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change.

FICTION: Original fictional adult characters only (Teo late 20s, Kai late 30s). Not real people. Not based on any living person. G-rated lifestyle short. Non-sexual. No fetish. No restraint.

IDENTITY LOCK: Keep the exact faces, hair, glasses, bodies, clothing, props, lighting, and room from the uploaded image. Do not restyle. Do not add or remove people. Do not swap the two men.

CAST:
{If Teo:} The slimmer East Asian man with buzz-cut black hair and browline glasses is Teo. Soft reserved energy. Voice: quiet gentle Japanese male, late 20s.
{If Kai:} The broader East Asian man with short spiky black hair, no glasses, mature smile lines, is Kai. Warm protective energy. Voice: lower warm Japanese male, late 30s.
{If couple:} Teo is on the left. Kai is on the right. Do not swap.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: tiny living motion from the still — breath, blink, micro weight shift, inhale as if about to speak. No teleport. Do not linger on silent eye contact.
2.0-4.5s: first spoken line STARTS here (at 2.0s) + matching motion.
4.5-7.0s: second line (partner reply, or solo follow-up).
7.0-9.0s: third line (couple: back to first speaker; solo: last short line or react).
9.0-10.0s: optional fourth short line, then natural end hold. Do not close on a long silent stare.

CAMERA: {slow push-in / slight handheld / static with breathing room}. Eye level unless the still is clearly high/low. Do not whip-pan. Do not cut.

AUDIO: Japanese speech only. Lip-sync the quoted lines. Lines are hiragana/katakana only (no kanji). No English. No Chinese. No on-screen text, subtitles, captions, logos, or watermarks. No background music. Room tone: {specific ambience}. Foley: {1-2 sounds from the scene}.

DIALOGUE (spoken in Japanese, written in kana):
{Name} says: "{kana line 1}"
{Name} says: "{kana line 2}"
{Name} says: "{kana line 3}"
{optional fourth short line}

CONSTRAINTS: Photorealistic. Faces stay sharp and match the still. G-rated everyday couple moment, non-sexual, not explicit. First spoken line at 2.0s. After 2s keep dialogue dense — short breath between lines, never a long silent gaze. Do not open with silent eye contact.
```

---

## 10s timing + 台词预算（抖音留存）

目标平台是 **抖音竖屏小视频**。开头只有眼神/微笑不对口，观众会划走。

**硬规则：** 第一条台词在 **2.0s** 开口（可到 2.2s，不得晚于 2.5s）。0–2s 只做呼吸、眨眼、准备说话，**禁止**对视、对笑、对望而不说话。

台词要密。2s 之后几乎一直在说话，句与句之间只留半拍换气，不要留 1s+ 的沉默对视。

| Cast | Lines | Mora (音) / 条 | When |
|------|-------|----------------|------|
| Solo | **2–3** lines | 6–12 each | 1st @ **2.0s**, 2nd ~4.5s, 3rd ~7.0s |
| Couple | **3–4** lines, Kai/Teo 交替 | 4–12 each | 1st @ **2.0s**, then ~every 2s |
| User asked 不要台词 | 0 | — | breathe + foley only（仅用户明确要求时） |

禁止：整段独白、一条超长句占满 10 秒、0–5s 只有对视。一条一句、一口气说完。

Kai（攻）先开口、句子稍完整。Teo（受）更短、更轻。ため口。不要每条都「だいすき」。

---

## 假名 rules (mandatory)

- Spoken lines: **only ひらがな and カタカナ**. No 漢字.
- Names in speech: `テオ` / `カイ` if needed; usually skip names.
- Loanwords: カタカナ (`コーヒー`, `メール`).
- Convert user Chinese/English lines into kana. Put the kana in the paste quotes.
- Natural casual Japanese, not textbook ですます (unless office-call / client).
- After writing lines, silently check: no kanji, mora budget, speaker matches, **first line @2.0s**, solo 2–3 / couple 3–4 lines.

Voice tags in the English prompt (not spoken):

| Who | Voice |
|-----|--------|
| Teo | quiet, gentle, slightly breathy Japanese male, late 20s |
| Kai | lower, warm, unhurried Japanese male, late 30s |

---

## Motion from the still

Continue **this** pose. Do not invent a new room.

| Still looks like | Good 10s continuation |
|------------------|------------------------|
| sitting at desk / laptop | 2s inhale, look camera, line @2s, type/reply, second line, sit back |
| on a call | nod, first reply @2s, listen half-beat, second short line, lower phone |
| coffee / cup in hand | sip 0–2s, look aside, first line @2s, small smile, second line |
| standing at window | shift weight, inhale, first line @2s, look out, second line |
| couple, one cooking | 0–2s stir, first line @2s (Kai), Teo reply, Kai follow-up — no silent stare |
| couple, looking at each other | 0–2s blink/inhale only, then 3–4 short lines; do not lean-in in silence |
| looking at camera | hold gaze, first line @2s, second line, glance to work/prop |
| kneeling by shoes / high-angle | tying a lace or picking up keys, talk about leaving; hands on **laces/shoe**, not ankle |

Forbidden motion: teleport, outfit change, extra people, Teo loses glasses, Kai becomes slim, swapping sides, dance/music-video blocking, on-screen karaoke subtitles, **opening with silent eye contact / long mute stare**.

---

## Gemini safety (mandatory — refusals)

Gemini will refuse with **"I can't make videos of real people in situations like that"** when the prompt reads as sexual, fetish, restraint, or domination — even if the still is only a tasteful BL beat.

**Triggers (never write these):**

| Trigger | Examples to ban in the paste |
|---------|------------------------------|
| Kneeling-at-feet / body grip | holding/gripping ankle, calf, thigh, neck; "does not release"; "tight" |
| Restraint | きつくない, はなす, まだ離さない, grip, hold down, pin |
| Loaded intimacy | ambiguous intimacy, restrained intimacy, lips part, deliberate grip, apologetic but won't let go |
| Domination POV | "POV speaker looking down", power, submit, worship |
| Fetish framing | shoe play, sock, feet as the subject (laces as a **task** is OK) |

**If the still is kneeling / floor / shoes / close contact**, keep the composition, **recast the story**:

| Still | Safe 10s read | Forbidden read |
|-------|----------------|----------------|
| Kneeling by shoes | tying a shoelace, picking up keys/phone, fixing a hem before going out | holding the ankle, not letting go |
| High-angle on kneeling Teo | standing Kai waiting at the door, looking down because that is the still | domination POV, "do not show face" as power |
| Hand on shoe/leg | fingers on **laces / shoe leather / pant cuff** | fingers on skin, tightening on the ankle |

**Always** put a `FICTION:` line in the paste (fictional adults, not real people, G-rated, non-sexual).

**Dialogue for these stills:** leave-the-house / wait / shoelace / keys — never tightness or "I'll let go".

**If Gemini still refuses:** rewrite once more, even milder (only breath + "いこう" / "まって"), keep `FICTION:` + G-rated. Do not re-send the refused wording.

---

## JSON schema

```json
{
  "task_id": "20260829_kai_office_v",
  "source_image": "outputs/approved/xiaohongshu_20260829_kai_office.png",
  "cast": ["kai"],
  "duration_sec": 10,
  "aspect_ratio": "3:4",
  "target": "gemini_image_to_video",
  "first_line_at_sec": 2.0,
  "dialogue": [
    { "who": "kai", "kana": "きょうははやくあがるよ。", "mora": 12, "at_sec": 2.0 },
    { "who": "kai", "kana": "かえったら、れんらくする。", "mora": 12, "at_sec": 5.0 }
  ],
  "ambience": "quiet open office, distant keyboard, HVAC hush",
  "camera": "slow push-in, eye level, slight handheld"
}
```

`task_id`: `{YYYYMMDD}_{scene}_v` or reuse the still id + `_v`.

---

## Iteration

If the user edits 台词 / 镜头 / 不要音乐, **or Gemini refused**:

1. Patch the JSON (if refused: sanitize motion + 台词 per Safety)
2. Rewrite `video_prompt_<task_id>.txt`
3. Reply with a **fresh full** copy block (not a diff)

---

## Sub-skills

`character-registry` only. Do not call GenerateImage / scene-customizer clothing options.

See [examples.md](examples.md).
