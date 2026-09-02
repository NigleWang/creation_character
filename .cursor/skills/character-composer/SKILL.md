---
name: character-composer
description: >-
  Binds Teo and Kai to scene blueprint positions — left=Teo(受), right=Kai(攻).
  Use after scene analysis in the virtual couple pipeline.
---

# Character + Scene Composer

## Input

- `character_bundle` from character-registry
- `scene_blueprint` from scene-analyzer
- `relationship/relationship.yaml`

## Binding rules (mandatory)

```
subject_1 (left)  → Teo  (受)
subject_2 (right) → Kai (攻)
```

If `subjects.count == 1`:
- Use only the user-requested character (@Teo or @Kai)
- Inherit that subject's pose from scene

## Output: generation_blueprint

Write to `outputs/drafts/generation_blueprint_<task_id>.json`:

```yaml
subjects:
  left_person:
    character: teo
    role: shou
    identity: { use_character_bible: true }
    pose: { inherit_from: subject_1 }

  right_person:
    character: kai
    role: gong
    identity: { use_character_bible: true }
    pose: { inherit_from: subject_2 }

interaction:
  inherit_scene: true

environment:
  inherit_scene: true   # includes lighting direction, color, and exposure — do not brighten

composition:
  preserve_scene: true

constraints:
  - Character controls IDENTITY
  - Scene controls COMPOSITION and ACTION
  - Do not swap Teo and Kai
  - Do not add or remove people
```

## Role energy in pose

When interpreting interaction for prompt:

| Element | Teo (受) | Kai (攻) |
|---------|----------|------------|
| Gaze | softer, receiving | leading, initiating |
| Posture | relaxed, leaning in | upright, leaning toward |
| Touch | being held | arm around, hand on shoulder |

These are **energy** cues — actual pose comes from scene blueprint.
