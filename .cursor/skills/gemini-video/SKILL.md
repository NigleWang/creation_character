---
name: gemini-video
description: >-
  From a Teo/Kai still (solo or couple), writes a 10-second Gemini
  image-to-video prompt with Japanese kana dialogue, copy-paste ready for
  Gemini. Use when the user asks for 图生视频, 视频提示词, Gemini视频, 10秒视频,
  i2v, Veo, Omni, image-to-video, or to animate an approved still.
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

5. Invent a **10s continuation** of this exact still (same room, clothes, faces). Write short **假名** lines that fit occupation + 受/攻.
6. Save:
   - `outputs/drafts/video_prompt_<task_id>.json`
   - `outputs/drafts/video_prompt_<task_id>.txt` (the paste block only)
7. Reply with the template below. Put the Gemini block in **one** fenced `text` code block so the user can copy it whole.

If the user already gave 台词 / 情绪 / 动作, use those (still convert 台词 to 假名).

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
【台词（假名）】
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

IDENTITY LOCK: Keep the exact faces, hair, glasses, bodies, clothing, props, lighting, and room from the uploaded image. Do not restyle. Do not add or remove people. Do not swap the two men.

CAST:
{If Teo:} The slimmer East Asian man with buzz-cut black hair and browline glasses is Teo. Soft reserved energy. Voice: quiet gentle Japanese male, late 20s.
{If Kai:} The broader East Asian man with short spiky black hair, no glasses, mature smile lines, is Kai. Warm protective energy. Voice: lower warm Japanese male, late 30s.
{If couple:} Teo is on the left. Kai is on the right. Do not swap.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: tiny living motion from the still — breath, blink, micro weight shift. No teleport.
2.0-5.5s: {beat 1 matching the still}.
5.5-8.0s: {beat 2}.
8.0-10.0s: settle — small smile or hold eye line, natural end hold.

CAMERA: {slow push-in / slight handheld / static with breathing room}. Eye level unless the still is clearly high/low. Do not whip-pan. Do not cut.

AUDIO: Japanese speech only. Lip-sync the quoted lines. Lines are hiragana/katakana only (no kanji). No English. No Chinese. No on-screen text, subtitles, captions, logos, or watermarks. No background music. Room tone: {specific ambience}. Foley: {1-2 sounds from the scene}.

DIALOGUE (spoken in Japanese, written in kana):
{Name} says: "{kana line 1}"
{optional second line}

CONSTRAINTS: Photorealistic. Faces stay sharp and match the still. Tasteful intimate couple energy, not explicit. Natural pauses between lines. Do not fill all 10 seconds with talking.
```

---

## 10s timing + 台词预算

Speech is short. Most of the 10s is motion + silence.

| Cast | Lines | Mora (音) | When |
|------|-------|-----------|------|
| Solo | 1 line | 8–16 | start ~2.5s |
| Couple | Kai then Teo (or reverse if Teo starts) | 8–14 then 4–10 | ~2.5s and ~6.5s |
| User asked 不要台词 | 0 | — | breathe + foley only |

Do not write a monologue. One breath per line. Leave 1s+ pause after speech.

Kai（攻）先开口、句子稍完整。Teo（受）更短、更轻。ため口。不要每条都「だいすき」.

---

## 假名 rules (mandatory)

- Spoken lines: **only ひらがな and カタカナ**. No 漢字.
- Names in speech: `テオ` / `カイ` if needed; usually skip names.
- Loanwords: カタカナ (`コーヒー`, `メール`).
- Convert user Chinese/English lines into kana. Put the kana in the paste quotes.
- Natural casual Japanese, not textbook ですます (unless office-call / client).
- After writing a line, silently check: no kanji, fits mora budget, matches who is speaking.

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
| sitting at desk / laptop | type 2s, glance at camera or phone, one line, sit back |
| on a call | listen, nod, short reply, lower the phone slightly |
| coffee / cup in hand | sip, look aside, small smile, one line |
| standing at window | shift weight, look out, inhale, one line |
| couple, one cooking | stir, glance at partner, line + short reply |
| couple, looking at each other | lean in a little, blink, two short lines |
| looking at camera | hold gaze, small smile, one line, look down to work/prop |

Forbidden motion: teleport, outfit change, extra people, Teo loses glasses, Kai becomes slim, swapping sides, dance/music-video blocking, on-screen karaoke subtitles.

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
  "dialogue": [
    { "who": "kai", "kana": "きょうははやくあがるよ。", "mora": 12 }
  ],
  "ambience": "quiet open office, distant keyboard, HVAC hush",
  "camera": "slow push-in, eye level, slight handheld"
}
```

`task_id`: `{YYYYMMDD}_{scene}_v` or reuse the still id + `_v`.

---

## Iteration

If the user edits 台词 / 镜头 / 不要音乐:

1. Patch the JSON
2. Rewrite `video_prompt_<task_id>.txt`
3. Reply with a **fresh full** copy block (not a diff)

---

## Sub-skills

`character-registry` only. Do not call GenerateImage / scene-customizer clothing options.

See [examples.md](examples.md).
