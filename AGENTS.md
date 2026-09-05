# AGENTS.md — Virtual Couple Studio + Tagame Anime

Cloud / mobile agents: read this file. Two-turn protocol is **mandatory**.

## Two tracks (do not mix)

| Track | Characters | Style | Skills |
|-------|------------|-------|--------|
| **Couple** | Teo（受, left）+ Kai（攻, right） | Photoreal Xiaohongshu | `virtual-couple` / `text-scene` / `pose-series` / `gemini-video` / `cover-collage` |
| **Tagame** | Tagame only | **Japanese anime** | `tagame-anime` |

@Tagame / `characters/Tagame` / `docs/anime.md` → **always** `tagame-anime`. Never photoreal. Never Teo/Kai faces. Never `gemini-video` photoreal paste.

## Project purpose

Generate Xiaohongshu photoreal images of **Teo（受, left）** and **Kai（攻, right）** from scene photos — **or** Tagame Japanese-anime stills + 10s i2v prompts (separate track).

## TWO-TURN PROTOCOL (non-negotiable)

### Turn 1 — Analyze + ask only

When user uploads a scene + mentions Teo/Kai/virtual-couple/换脸:

1. Analyze scene (composition, pose, environment)
2. Post **numbered text options** for accessories / clothing / patterns (see template below)
3. **END turn immediately**
4. **FORBIDDEN in Turn 1:** `GenerateImage`, writing `user_confirmed: true` in manifest

### Turn 2 — Generate only

When user replies with numbers or text choices (or said「全部保持原场景」in Turn 1):

1. Write `outputs/drafts/customization_<task_id>.json` with `user_confirmed: true`
2. Build prompt → call `GenerateImage` → QC → deliver

**If user did not confirm choices yet → stay in Turn 1. Do not generate.**

## Turn 1 reply template (copy this format)

```text
✅ 场景已分析（构图/动作/环境将保持不变）

换脸前请确认（回复数字或文字，例如：2,3,1,2）：

【{Character}】
1️⃣ 装饰物：1保持原场景({detected}) 2角色默认 3墨镜 4耳机 5无装饰
2️⃣ 上衣颜色：1保持({detected}) 2白 3藏青 4浅蓝 5黑
3️⃣ 上衣图案：1保持 2纯色 3条纹 4格子
4️⃣ 下装颜色：1保持({detected}) 2黑 3灰 4藏青

快捷：「全部保持原场景」或「角色默认，上衣藏青，下装灰」

⏸️ 请回复后我再生成图片。
```

Character defaults: Teo → browline glasses; Kai → no glasses.

## Skip Turn 1 only if

User's **first message** already includes explicit style choices, e.g.:
- `全部保持原场景`
- `角色默认，上衣藏青，下装灰`

## Skills location

`.cursor/skills/virtual-couple/SKILL.md` — 换脸：场景图定姿态，角色圣经定身份  
`.cursor/skills/scene-customizer/SKILL.md` — customization details  
`.cursor/skills/pose-series/SKILL.md` — 换姿态做系列：已有成图锁定形象/服装/场景，只换 pose  
`.cursor/skills/xiaohongshu-caption/SKILL.md` — 成图/系列 → 小红书发布文案（Teo/Kai，只出文案不出图）  
`.cursor/skills/text-scene/SKILL.md` — 文字场景：按人设补全场景卡，确认后生成一张  
`.cursor/skills/gemini-video/SKILL.md` — 成图 → Gemini 10s 图生视频提示词（台词假名，只出文案不出视频）  
`.cursor/skills/tagame-anime/SKILL.md` — Tagame 动漫：场景卡确认 → 一张静帧 → 10s 图生视频提示词（`docs/anime.md` 公式）  
`.cursor/skills/cover-collage/SKILL.md` — 系列成图 → 小红书首页拼接封面（Pillow，禁止 GenerateImage）

## Text scene (no photo)

When user describes a scene in **words** (文字场景 / 场景需求 / 按人设出图 / 没有参考图):

1. Turn 1: load bibles → fill gaps → post completed scene card → STOP
2. Turn 2: after `生成` / edits → one GenerateImage, save `outputs/approved/xiaohongshu_<task_id>.png`

Do **not** run virtual-couple 换脸 or pose-series for this case.

## Pose series (existing approved still)

When user has `outputs/approved/...` and asks for 系列 / 换姿态 / 其他 pose:

1. Turn 1: lock look + post numbered **pose** options + STOP
2. Turn 2: GenerateImage per selected pose (`aspect_ratio` 3:4, refs = [approved still, face ref])
3. Save the set to `outputs/approved/series/<task_id>/` as `01_<pose_id>.png`, `02_...` — never as loose files in `outputs/approved/`
4. Run `xiaohongshu-caption`: one 标题+正文+标签 for the set. Names **Teo**（受）/ **Kai**（攻）.

Single stills stay at `outputs/approved/xiaohongshu_<task_id>.png`.

## Cover collage (首页拼接)

When user has **2+ stills** (usually `outputs/approved/series/<task_id>/`) and asks 拼接 / 封面图 / 九宫格 / 拼图 / 首页封面:

1. Follow `.cursor/skills/cover-collage/SKILL.md`
2. Turn 1: post **3** layout schemes + 笔记文案 → STOP. Default cover has **no overlay text and no N图 badge**.
3. Turn 2: `python3 scripts/make_cover.py --config …` → one 1080×1440 PNG in the series folder
4. **Do not** call GenerateImage — this is Pillow pixel composite, not a redraw

Do **not** run virtual-couple 换脸 or pose-series 生图 for this case.

## GenerateImage

- Tool: `cursor` / `GenerateImage`
- aspect_ratio: `3:4`
- Teo/Kai: `reference_image_paths` = [scene if any, character face refs]; photoreal; match exposure
- Tagame: `reference_image_paths` = [Tagame face ref only]; **Japanese anime**, never photoreal
- Lighting: match the scene/source still exactly (direction, color, **exposure**). Do not brighten. Over-bright / glow / HDR looks AI-generated.

## Xiaohongshu caption (发布文案)

When pose-series Turn 2 finishes, **or** the user asks 文案 / 标题 / 标签 / 小红书发布:

1. Follow `.cursor/skills/xiaohongshu-caption/SKILL.md`
2. **Do not** call GenerateImage
3. Names in copy: **Teo**（受）/ **Kai**（攻）— never Tom/James
4. One title + 30–80字 body + 6–10 tags (`#TeoKai` `#TeoKaiDaily` always)

## Image-to-video prompt (Gemini)

When user has a **Teo/Kai** still (usually `outputs/approved/`) and asks 图生视频 / Gemini视频 / 10秒视频:

1. Follow `.cursor/skills/gemini-video/SKILL.md`
2. **Do not** call GenerateImage
3. Deliver one copy-paste English prompt; spoken lines in Japanese kana only
4. Sanitize for Gemini: fictional adults, G-rated. Kneeling/shoes = tying laces / picking up keys — never ankle-grip or "won't let go" (that refusal is "real people in situations like that")

If the still is **Tagame** / anime: use `tagame-anime` Turn C instead (anime lock + invite/heat/possession formula).

## Tagame anime (separate track)

When user @Tagame / `characters/Tagame` / `docs/anime.md` / 办公室肌肉上司 / 动漫画风:

1. Follow `.cursor/skills/tagame-anime/SKILL.md`
2. Turn 1: load Tagame bible → fill scene card → **STOP** for confirmation
3. Turn 2: one GenerateImage, **Japanese anime** (never photoreal), face ref `characters/Tagame/references/face_01.jpeg`, save `outputs/approved/tagame_<task_id>.png`
4. Then write 10s i2v prompt: invite → body-heat → possession; kana dialogue; first line at 2.0s. Do **not** call GenerateImage for the video step
5. Art style lock on every later Tagame request: high-quality Japanese anime / digital illustration

Do **not** run virtual-couple, text-scene, pose-series, or gemini-video for Tagame.
