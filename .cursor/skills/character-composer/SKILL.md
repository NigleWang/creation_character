---
name: character-composer
description: >-
  Binds the active photoreal cast to scene positions. Teo/Kai: left=Teo(受),
  right=Kai(攻). 小川/大海: left=小川, right=大海, no 受/攻 labels. Use after
  scene analysis in the virtual couple pipeline.
---

# Character + Scene Composer

## Input

- `character_bundle` from character-registry
- `scene_blueprint` from scene-analyzer
- `relationship/relationship.yaml` when the cast is Teo/Kai
- `relationship/ogawa_dahai.yaml` when the cast is 小川/大海

## Binding rules (mandatory)

Teo/Kai:

```
subject_1 (left)  → Teo  (受)
subject_2 (right) → Kai (攻)
```

小川/大海:

```
subject_1 (left)  → 小川
subject_2 (right) → 大海
```

Do not put both casts in one blueprint. If the user named sides, use those sides for the whole image.

If `subjects.count == 1`:
- Use only the user-requested character
- Inherit that subject's pose from scene
- A 小川/大海 request with both names and one person: ask which face before writing the blueprint

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
  inherit_scene: true   # lighting direction, color, exposure, grime — do not brighten or sanitize

composition:
  preserve_scene: true

constraints:
  - Character controls IDENTITY
  - Scene controls COMPOSITION and ACTION
  - Scene grime (reflections, clutter, uneven shadows) must pass through to prompt-builder
  - Do not swap the two people in the active cast
  - Do not add or remove people
  - Do not copy a character-sheet backdrop into the scene
```

For 小川/大海, `role` is `left` / `right`, not `shou` / `gong`.

## Role energy in pose

Teo/Kai only. Actual pose still comes from the scene blueprint.

| Element | Teo (受) | Kai (攻) |
|---------|----------|------------|
| Gaze | softer, receiving | leading, initiating |
| Posture | relaxed, leaning in | upright, leaning toward |
| Touch | being held | arm around, hand on shoulder |

小川/大海：不套这张表。小川更静，大海更稳，但手、视线、谁靠谁都跟场景。不要因为人在右边就加搂肩。
