# AGENTS.md — Virtual Couple Studio

Cloud / mobile agents: read this file. Two-turn protocol is **mandatory**.

## Project purpose

Generate Xiaohongshu images of **Tom（受, left）** and **James（攻, right）** from scene reference photos.

## TWO-TURN PROTOCOL (non-negotiable)

### Turn 1 — Analyze + ask only

When user uploads a scene + mentions Tom/James/virtual-couple/换脸:

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

Character defaults: Tom → browline glasses; James → no glasses.

## Skip Turn 1 only if

User's **first message** already includes explicit style choices, e.g.:
- `全部保持原场景`
- `角色默认，上衣藏青，下装灰`

## Skills location

`.cursor/skills/virtual-couple/SKILL.md` — 换脸：场景图定姿态，角色圣经定身份  
`.cursor/skills/scene-customizer/SKILL.md` — customization details  
`.cursor/skills/pose-series/SKILL.md` — 换姿态做系列：已有成图锁定形象/服装/场景，只换 pose

## Pose series (existing approved still)

When user has `outputs/approved/...` and asks for 系列 / 换姿态 / 其他 pose:

1. Turn 1: lock look + post numbered **pose** options + STOP
2. Turn 2: GenerateImage per selected pose (`aspect_ratio` 3:4, refs = [approved still, face ref])

Do **not** run virtual-couple 换脸流程 for this case.

## GenerateImage

- Tool: `cursor` / `GenerateImage`
- aspect_ratio: `3:4`
- reference_image_paths: [scene, character face refs]
