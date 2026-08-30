# AGENTS.md — Virtual Couple Studio

Cloud / mobile agents: read this file. Two-turn protocol is **mandatory**.

## Project purpose

Generate Xiaohongshu images of **Teo（受, left）** and **Kai（攻, right）** from scene reference photos.

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

Do **not** run virtual-couple 换脸流程 for this case.

## GenerateImage

- Tool: `cursor` / `GenerateImage`
- aspect_ratio: `3:4`
- reference_image_paths: [scene, character face refs]

## Xiaohongshu caption (发布文案)

When pose-series Turn 2 finishes, **or** the user asks 文案 / 标题 / 标签 / 小红书发布:

1. Follow `.cursor/skills/xiaohongshu-caption/SKILL.md`
2. **Do not** call GenerateImage
3. Names in copy: **Teo**（受）/ **Kai**（攻）— never Tom/James
4. One title + 30–80字 body + 6–10 tags (`#TeoKai` `#TeoKaiDaily` always)

## Image-to-video prompt (Gemini)

When user has a still (usually `outputs/approved/`) and asks 图生视频 / Gemini视频 / 10秒视频:

1. Follow `.cursor/skills/gemini-video/SKILL.md`
2. **Do not** call GenerateImage
3. Deliver one copy-paste English prompt; spoken lines in Japanese kana only
