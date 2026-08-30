---
name: character-registry
description: >-
  Loads Teo and Kai character bibles and reference paths for the virtual couple
  pipeline. Use when resolving @Teo, @Kai, character identity, or face
  consistency in creation_character.
---

# Character Registry

## Registry

| ID | Display | Role | Bible | YAML | Reference |
|----|---------|------|-------|------|-----------|
| `teo` | Teo | 受 | `characters/teo/bible.md` | `characters/teo/character.yaml` | `characters/teo/references/face_01.jpeg` |
| `kai` | Kai | 攻 | `characters/kai/bible.md` | `characters/kai/character.yaml` | `characters/kai/references/face_01.jpeg` |

Relationship: `relationship/relationship.yaml`

## Load procedure

For each requested character ID:

1. Read `characters/<id>/bible.md`
2. Read `characters/<id>/character.yaml`
3. Note `reference_images.primary` path for GenerateImage

## Alias resolution

| User input | Maps to |
|------------|---------|
| Teo, teo, @Teo | `teo` |
| Kai, kai, @Kai | `kai` |
| 受 | `teo` |
| 攻 | `kai` |

Do **not** use Tom / James. Those names are retired.

Legacy `outputs/` paths may still contain `tom` / `james` in the filename; they are Teo / Kai stills. Do not treat them as different people. New files use `teo` / `kai`.

## Output: character_bundle

Append to task manifest:

```yaml
character_bundle:
  teo:
    role: shou
    default_side: left
    reference: characters/teo/references/face_01.jpeg
    identity_prompt: |
      Teo: East Asian man ~28, oval face, almond eyes, browline glasses
      (black top/silver bottom frame), buzz cut black hair, short stubble,
      warm tan skin, slim athletic build. Calm gentle reserved expression.
      Independent interior designer (small studio, material samples).

  kai:
    role: gong
    default_side: right
    reference: characters/kai/references/face_01.jpeg
    identity_prompt: |
      Kai: East Asian man ~38, square jaw, warm smile with smile lines,
      short spiky black hair, groomed stubble, golden tan skin, muscular
      broad build. Confident protective mature expression.
      Product director at a health-tech company (office, dual monitors).
```

## Consistency rules

- Face identity from reference images has **highest priority**
- Do not merge Teo and Kai features
- Preserve glasses on Teo always
- Preserve Kai's mature muscular look always
