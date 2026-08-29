---
name: character-composer
description: >-
  Binds Tom and James to scene blueprint positions — left=Tom(受), right=James(攻).
  Use after scene analysis in the virtual couple pipeline.
---

# Character + Scene Composer

## Input

- `character_bundle` from character-registry
- `scene_blueprint` from scene-analyzer
- `relationship/relationship.yaml`

## Binding rules (mandatory)

```
subject_1 (left)  → Tom  (受)
subject_2 (right) → James (攻)
```

If `subjects.count == 1`:
- Use only the user-requested character (@Tom or @James)
- Inherit that subject's pose from scene

## Output: generation_blueprint

Write to `outputs/drafts/generation_blueprint_<task_id>.json`:

```yaml
subjects:
  left_person:
    character: tom
    role: shou
    identity: { use_character_bible: true }
    pose: { inherit_from: subject_1 }

  right_person:
    character: james
    role: gong
    identity: { use_character_bible: true }
    pose: { inherit_from: subject_2 }

interaction:
  inherit_scene: true

environment:
  inherit_scene: true

composition:
  preserve_scene: true

constraints:
  - Character controls IDENTITY
  - Scene controls COMPOSITION and ACTION
  - Do not swap Tom and James
  - Do not add or remove people
```

## Role energy in pose

When interpreting interaction for prompt:

| Element | Tom (受) | James (攻) |
|---------|----------|------------|
| Gaze | softer, receiving | leading, initiating |
| Posture | relaxed, leaning in | upright, leaning toward |
| Touch | being held | arm around, hand on shoulder |

These are **energy** cues — actual pose comes from scene blueprint.
