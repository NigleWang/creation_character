---
name: character-registry
description: >-
  Loads character bibles and reference paths. Teo/Kai are the photoreal couple
  pipeline; Tagame is the separate Japanese-anime office-superior pipeline.
  Ohno Kenichi (大野健一) is the night bus-depot patrol track in
  characters/Tagame-patrol. Use when resolving @Teo, @Kai, @Tagame,
  @Tagame-patrol, character identity, or face consistency in creation_character.
---

# Character Registry

## Registry

| ID | Display | Pipeline | Role | Bible | YAML | Reference |
|----|---------|----------|------|-------|------|-----------|
| `teo` | Teo | virtual-couple / text-scene | 受 | `characters/teo/bible.md` | `characters/teo/character.yaml` | `characters/teo/references/face_01.jpeg` |
| `kai` | Kai | virtual-couple / text-scene | 攻 | `characters/kai/bible.md` | `characters/kai/character.yaml` | `characters/kai/references/face_01.jpeg` |
| `tagame` | Tagame | **tagame-anime** | 办公室肌肉上司 | `characters/Tagame/bible.md` | `characters/Tagame/character.yaml` | `characters/Tagame/references/face_01.jpeg` |
| `ohno` | 大野健一 | **tagame-patrol** | 深夜场站调度 / 夜班巡逻 | `docs/patorl-tagame.md` | `.cursor/skills/tagame-patrol/storyline.md` | `characters/Tagame-patrol/full_body_char.jpeg` |

Teo+Kai relationship: `relationship/relationship.yaml`

**Do not mix pipelines.** Tagame is never photoreal and never paired with Teo/Kai. Teo/Kai are never restyled as anime Tagame. 大野健一 is not the office Tagame: do not swap their face references.

## Load procedure

For each requested character ID:

1. Read bible + yaml (paths from the registry table — `tagame` lives in `characters/Tagame/`, not `characters/tagame/`)
2. Note `reference_images.primary` path for GenerateImage

## Alias resolution

| User input | Maps to |
|------------|---------|
| Teo, teo, @Teo | `teo` |
| Kai, kai, @Kai | `kai` |
| 受 | `teo` |
| 攻 | `kai` |
| Tagame, tagame, @Tagame, characters/Tagame | `tagame` |
| Tagame-patrol, @Tagame-patrol, characters/Tagame-patrol, 大野健一, Ohno Kenichi, docs/patorl-tagame.md | `ohno` |

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

  tagame:
    role: office_dominant
    pipeline: tagame-anime
    art_style: japanese_anime
    reference: characters/Tagame/references/face_01.jpeg
    identity_prompt: |
      Tagame: mature East Asian man ~40, square jaw, dark-brown short
      slightly wavy spiked hair swept up, neat brown stubble/beard,
      thick angled brows, confident half-smile, extremely muscular
      broad shoulders, full chest, thick arms. High-quality Japanese
      anime / digital illustration, clean linework, not photorealistic.
      Office superior speaking to the viewer. Match the face reference.

  ohno:
    role: depot_patrol
    pipeline: tagame-patrol
    art_style: japanese_anime
    reference: characters/Tagame-patrol/full_body_char.jpeg
    sheet_read_only: characters/Tagame-patrol/detail_char.jpeg
    identity_prompt: |
      Ohno Kenichi, 32, night bus-depot dispatcher and security patrol.
      Match the full-body reference: square jaw, short dark-brown spiky hair,
      neat stubble, navy leather bomber, tight white shirt, burgundy tie,
      black trousers. Japanese anime, not photorealistic, not the office Tagame.
```

## Consistency rules

- Face identity from reference images has **highest priority**
- Do not merge Teo and Kai features
- Preserve glasses on Teo always
- Preserve Kai's mature muscular look always
- Tagame: default Japanese anime (never photoreal). If the user names CuteGuysArt, follow `.cursor/skills/cuteguysart/SKILL.md` and change only the rendering (bold contour lines, warm painterly skin, medium kind eyes, bright saturated lifestyle illustration). Keep the beard, dark-brown spiked hair, and his large natural muscle. Never slim, pretty-boy, or oversized anime eyes
- 大野健一: face and uniform from `characters/Tagame-patrol/full_body_char.jpeg`. Do not substitute the office Tagame reference. Scenes stay at the night bus depot
