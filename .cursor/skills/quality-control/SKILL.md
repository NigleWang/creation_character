---
name: quality-control
description: >-
  Visual QC for generated Tom/James images — character consistency, scene
  preservation, Xiaohongshu suitability. Use after GenerateImage in
  creation_character pipeline.
---

# Quality Controller

## Input

- Generated image (from GenerateImage output)
- Character references: `characters/tom/references/face_01.jpeg`, `characters/james/references/face_01.jpeg`
- Scene reference (if provided)
- `generation_blueprint`

## Checks

### 1. Character consistency

- Tom looks like Tom? (glasses, buzz cut, slim build)
- James looks like James? (spiky hair, muscular, mature face)
- No face swap between Tom and James?

### 2. Scene consistency

- Composition roughly matches reference?
- Left/right positions correct?
- Pose and interaction preserved?

**pose-series mode:** Do not require source pose. Require same identity, outfit, and environment; pose must match the **chosen** catalog pose.

### 3. Couple consistency

- Correct number of people?
- No merged faces, extra hands, missing limbs?

### 4. Xiaohongshu quality

- 3:4 works as cover/thumbnail?
- Faces visible and attractive?
- Warm cinematic feel?
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
| Tom/James swapped | "CRITICAL: Tom MUST be on LEFT with glasses. James MUST be on RIGHT, muscular." |
| Face drift | "Match face reference images exactly. Do not alter facial features." |
| Pose lost | "Strictly copy body positions from scene reference." |
| Extra limbs | "Exactly two people, two arms each, anatomically correct." |
