---
name: quality-control
description: >-
  Visual QC for generated photoreal images — Teo/Kai or 小川/大海 character
  consistency, scene preservation, Xiaohongshu suitability. Use after
  GenerateImage in the creation_character pipeline. Check the cast that was
  requested; do not pass a frame that mixed the two casts.
---

# Quality Controller

**Tagame / anime stills:** use the QC table in `tagame-anime` (default Japanese anime; CuteGuysArt only when that style was requested). This skill is photoreal: Teo/Kai, or 小川/大海.

## Input

- Generated image (from GenerateImage output)
- Character references for the active cast: Teo/Kai face jpegs, or `characters/小川/小川.png` and `characters/大海/大海.png`
- Scene reference (if provided)
- `generation_blueprint`

## Checks

### 1. Character consistency

Teo/Kai cast:

- Teo looks like Teo? (glasses, buzz cut, slim build)
- Kai looks like Kai? (spiky hair, muscular, mature face)
- No face swap between Teo and Kai?

小川/大海 cast:

- 小川 looks like the six-view sheet? (neat crop, light stubble, no glasses, not stocky)
- 大海 looks like the turnaround? (dry short hair, short beard, thick brows, wide jaw, stocky muscle)
- No face swap between 小川 and 大海?
- Sheet bleed is a fail: gray studio, view labels, color swatches, printed bible, panel grid
- Teo glasses, Teo buzz cut, or Kai spiky hair on either man is a fail

### 2. Scene consistency

- Composition roughly matches reference?
- Left/right positions correct?
- Pose and interaction preserved?
- Lighting matches the scene / source still (direction, warmth, **brightness**)?

**Lighting fail (common AI tell):** Output is brighter, flatter, glowy, or more evenly lit than the reference. Over-bright = regenerate. Do not "improve" exposure.

**Scene grime fail:** Reference had reflections, clutter, uneven shadows, or mixed indoor light — output cleaned them up, added studio evenness, or removed surface reflections. Regenerate with grime-preservation language from `docs/light.md`.

**Over-polished fail:** Plastic skin, airbrushed faces, hyper-sharp hair strands, clinically clean backgrounds, HDR glow. Regenerate with anti-AI module from `prompt-builder`.

**pose-series mode:** Do not require source pose. **Hard-lock** same face, hairstyle, outfit, environment, and **exposure** across the whole batch; pose must match the **chosen** catalog pose only. Any drift in hair/clothes between frames = regenerate that frame.

### 3. Couple consistency

- Correct number of people?
- No merged faces, extra hands, missing limbs?

### 4. Xiaohongshu quality

- 3:4 works as cover/thumbnail?
- Faces visible and attractive (without lifting overall exposure)?
- Natural photograph, not HDR / beauty-light / cinematic glow?
- Tasteful for platform (not explicit)?

## Pre-publish gate (mandatory before `accept`)

Run this checklist **every time** before saving to `outputs/approved/` or delivering to the user. Any fail → `regenerate` (max 1 retry) or `reject`; do **not** ship.

| Gate | Fail if |
|------|---------|
| Exposure | Brighter than reference / lifted shadows / glow |
| Scene grime | Reflections, clutter, or uneven shadows removed or smoothed |
| AI polish | Plastic skin, HDR, studio evenness, hyper-sharp everything |
| pose-series lock | Face, hair, or outfit differs from source still or from sibling frames |
| Series grade | Later frames brighter or cleaner than frame 01 |

Prompt fixes: `docs/light.md` §6 module + `prompt-builder` anti-AI block.

## Output

```json
{
  "score": 8.5,
  "character_consistency": 9,
  "scene_consistency": 8,
  "composition": 9,
  "social_quality": 8,
  "issues": [],
  "decision": "accept"
}
```

`decision`: `accept` | `regenerate` | `reject`

## Actions

| decision | Action |
|----------|--------|
| accept | Single: `outputs/approved/xiaohongshu_<task_id>.png`. pose-series: `outputs/approved/series/<task_id>/01_<pose_id>.png`. 归档路径不是手机预览路径；嵌图按该 skill 的「Cloud 客户端显示」 |
| regenerate | Tighten prompt for failed checks, retry GenerateImage (max 1 retry) |
| reject | Save to `outputs/rejected/` with issues, explain to user |

## Regenerate prompt fixes

| Issue | Add to prompt |
|-------|---------------|
| Teo/Kai swapped | "CRITICAL: Teo MUST be on LEFT with glasses. Kai MUST be on RIGHT, muscular." |
| 小川/大海 swapped | "CRITICAL: 小川 MUST be on LEFT, neat crop, light stubble, no glasses, not stocky. 大海 MUST be on RIGHT, short beard, stocky muscle." |
| Sheet bleed | "Identity only. Remove the gray turnaround studio, labels, swatches, and printed text. Keep the scene." |
| Face drift | "Match face reference images exactly. Do not alter facial features." |
| Pose lost | "Strictly copy body positions from scene reference." |
| Extra limbs | "Exactly two people, two arms each, anatomically correct." |
| Too bright / AI glow | "Match the reference exposure exactly. Do not brighten, lift shadows, add fill, HDR, rim glow, or beauty lighting. Keep original shadow density." |
| Scene too clean | "Preserve reflections, background clutter, uneven shadows, mixed light. Do not sanitize or polish the environment." |
| Over-polished / plastic | "natural available light, slightly imperfect exposure, natural skin texture, unretouched look, not overly sharp, not airbrushed. See docs/light.md." |
| pose-series outfit/hair drift | "Copy exact face, hairstyle, and clothing from the FIRST reference image. Only pose changes." |
