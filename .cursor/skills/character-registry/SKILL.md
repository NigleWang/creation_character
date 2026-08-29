---
name: character-registry
description: >-
  Loads Tom and James character bibles and reference paths for the virtual couple
  pipeline. Use when resolving @Tom, @James, character identity, or face
  consistency in creation_character.
---

# Character Registry

## Registry

| ID | Display | Role | Bible | YAML | Reference |
|----|---------|------|-------|------|-----------|
| `tom` | Tom | 受 | `characters/tom/bible.md` | `characters/tom/character.yaml` | `characters/tom/references/face_01.jpeg` |
| `james` | James | 攻 | `characters/james/bible.md` | `characters/james/character.yaml` | `characters/james/references/face_01.jpeg` |

Relationship: `relationship/relationship.yaml`

## Load procedure

For each requested character ID:

1. Read `characters/<id>/bible.md`
2. Read `characters/<id>/character.yaml`
3. Note `reference_images.primary` path for GenerateImage

## Alias resolution

| User input | Maps to |
|------------|---------|
| Tom, tom, @Tom | `tom` |
| James, james, @James | `james` |
| 受 | `tom` |
| 攻 | `james` |

## Output: character_bundle

Append to task manifest:

```yaml
character_bundle:
  tom:
    role: shou
    default_side: left
    reference: characters/tom/references/face_01.jpeg
    identity_prompt: |
      Tom: East Asian man ~28, oval face, almond eyes, browline glasses
      (black top/silver bottom frame), buzz cut black hair, short stubble,
      warm tan skin, slim athletic build. Calm gentle reserved expression.
      Independent interior designer (small studio, material samples).

  james:
    role: gong
    default_side: right
    reference: characters/james/references/face_01.jpeg
    identity_prompt: |
      James: East Asian man ~38, square jaw, warm smile with smile lines,
      short spiky black hair, groomed stubble, golden tan skin, muscular
      broad build. Confident protective mature expression.
      Product director at a health-tech company (office, dual monitors).
```

## Consistency rules

- Face identity from reference images has **highest priority**
- Do not merge Tom and James features
- Preserve glasses on Tom always
- Preserve James's mature muscular look always
