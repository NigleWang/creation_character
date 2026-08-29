---
name: scene-analyzer
description: >-
  Extracts scene blueprint from a reference image — composition, pose, lighting,
  environment — without identifying original people. Use when analyzing scene
  photos for the virtual couple pipeline.
---

# Scene Analyzer

## Input

- Scene reference image (user upload or `scenes/*`)
- Optional: number of characters expected (1 or 2)

## Task

Analyze the reference image. **Do NOT identify or describe original people.**

Extract only visual structure. Write result to `outputs/drafts/scene_blueprint_<task_id>.json`.

## Extraction checklist

1. Environment (location, time, indoor/outdoor)
2. Composition (framing, camera angle, aspect ratio hint)
3. Number of people
4. Each person's position (left/center/right)
5. Body direction and posture
6. Interaction type (eye contact, embrace, walking, etc.)
7. Hand positions
8. Head and gaze direction
9. Lighting (direction, warmth, cinematic/natural)
10. Color palette
11. Visual texture (film, digital, soft, grain)
12. Emotional atmosphere
13. **Customizable style elements** (for scene-customizer — per person: accessories, top/bottom color, pattern, material)

## Output schema

```json
{
  "scene": {
    "environment": {
      "location": "cafe",
      "time": "afternoon",
      "lighting": "warm sunlight through window"
    },
    "composition": {
      "framing": "medium shot",
      "camera_angle": "eye level",
      "aspect_ratio": "3:4"
    },
    "subjects": { "count": 2 },
    "positions": {
      "subject_1": {
        "position": "left",
        "body_direction": "facing right",
        "posture": "sitting"
      },
      "subject_2": {
        "position": "right",
        "body_direction": "facing left",
        "posture": "leaning forward"
      }
    },
    "interaction": {
      "type": "eye_contact",
      "emotional_tone": "intimate warm"
    },
    "pose": {
      "subject_1": { "gaze": "looking at subject_2", "hands": "holding cup" },
      "subject_2": { "gaze": "looking at subject_1", "posture": "leaning in" }
    },
    "visual_style": {
      "realism": "high",
      "lighting": "cinematic",
      "color_tone": "warm",
      "texture": "film photography"
    },
    "customizable_elements": {
      "subject_1": {
        "accessories": ["sunglasses"],
        "top": { "type": "shirt", "color": "white", "pattern": "solid" },
        "bottom": { "type": "pants", "color": "black", "pattern": "solid" }
      },
      "subject_2": {
        "accessories": [],
        "top": { "type": "jacket", "color": "navy", "pattern": "solid" },
        "bottom": { "type": "jeans", "color": "blue", "pattern": "solid" }
      }
    }
  }
}
```

Map subject_1 → left (Tom), subject_2 → right (James) in couple scenes.

## Rules

- Preserve original composition and action logic
- Never output names or identities of people in the reference
- If single person scene → `subjects.count: 1`, bind to @mentioned character only
- Subject_1 = leftmost person, subject_2 = rightmost person
