---
name: quality-control
description: >-
  Visual QC for generated Teo/Kai images — character consistency, scene
  preservation, Xiaohongshu suitability. Use after GenerateImage in
  creation_character pipeline.
---

# Quality Controller

## Input

- Generated image (from GenerateImage output)
- Character references: `characters/teo/references/face_01.jpeg`, `characters/kai/references/face_01.jpeg`
- Scene reference (if provided)
- `generation_blueprint`

## Checks

### 1. Character consistency

- Teo looks like Teo? (glasses, buzz cut, slim build)
- Kai looks like Kai? (spiky hair, muscular, mature face)
- No face swap between Teo and Kai?

### 2. Scene consistency

- Composition roughly matches reference?
- Left/right positions correct?
- Pose and interaction preserved?
- Lighting matches the scene / source still (direction, warmth, **brightness**)?

**Lighting fail (common AI tell):** Output is brighter, flatter, glowy, or more evenly lit than the reference. Over-bright = regenerate. Do not "improve" exposure.

**pose-series mode:** Do not require source pose. Require same identity, outfit, environment, and **exposure**; pose must match the **chosen** catalog pose.

### 3. Couple consistency

- Correct number of people?
- No merged faces, extra hands, missing limbs?

### 4. Xiaohongshu quality

- 3:4 works as cover/thumbnail?
- Faces visible and attractive (without lifting overall exposure)?
- Natural photograph, not HDR / beauty-light / cinematic glow?
- Tasteful for platform (not explicit)?

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
| accept | Single: `outputs/approved/xiaohongshu_<task_id>.png`. pose-series: `outputs/approved/series/<task_id>/01_<pose_id>.png` |
| regenerate | Tighten prompt for failed checks, retry GenerateImage (max 1 retry) |
| reject | Save to `outputs/rejected/` with issues, explain to user |

## Regenerate prompt fixes

| Issue | Add to prompt |
|-------|---------------|
| Teo/Kai swapped | "CRITICAL: Teo MUST be on LEFT with glasses. Kai MUST be on RIGHT, muscular." |
| Face drift | "Match face reference images exactly. Do not alter facial features." |
| Pose lost | "Strictly copy body positions from scene reference." |
| Extra limbs | "Exactly two people, two arms each, anatomically correct." |
| Too bright / AI glow | "Match the reference exposure exactly. Do not brighten, lift shadows, add fill, HDR, rim glow, or beauty lighting. Keep original shadow density." |
