---
name: character-registry
description: >-
  Loads character bibles and reference paths. Teo/Kai are the photoreal couple
  pipeline. 小川 and 大海 are a separate photoreal swap cast
  (characters/小川, characters/大海): same scene pipeline, different faces.
  Tagame is the Japanese-anime office-superior pipeline. Ohno Kenichi
  (大野健一) is the night bus-depot patrol track in characters/Tagame-patrol.
  Use when resolving @Teo, @Kai, @小川, @大海, @Tagame, @Tagame-patrol,
  character identity, or face consistency in creation_character.
---

# Character Registry

## Registry

| ID | Display | Pipeline | Role | Bible | YAML | Reference |
|----|---------|----------|------|-------|------|-----------|
| `teo` | Teo | virtual-couple / text-scene | 受 | `characters/teo/bible.md` | `characters/teo/character.yaml` | `characters/teo/references/face_01.jpeg` |
| `kai` | Kai | virtual-couple / text-scene | 攻 | `characters/kai/bible.md` | `characters/kai/character.yaml` | `characters/kai/references/face_01.jpeg` |
| `tagame` | Tagame | **tagame-anime** | 办公室肌肉上司 | `characters/Tagame/bible.md` | `characters/Tagame/character.yaml` | `characters/Tagame/references/face_01.jpeg` |
| `ohno` | 大野健一 | **tagame-patrol** | 深夜场站调度 / 夜班巡逻 | `docs/patorl-tagame.md` | `.cursor/skills/tagame-patrol/storyline.md` | `characters/Tagame-patrol/full_body_char.jpeg` |
| `ogawa` | 小川 | virtual-couple / text-scene | 写实，双人默认左 | `characters/小川/bible.md` | `characters/小川/character.yaml` | `characters/小川/小川.png` |
| `dahai` | 大海 | virtual-couple / text-scene | 写实，双人默认右 | `characters/大海/bible.md` | `characters/大海/character.yaml` | `characters/大海/大海.png` |

Teo+Kai relationship: `relationship/relationship.yaml`  
小川+大海 pair: `relationship/ogawa_dahai.yaml`

**Do not mix pipelines.** Tagame is never photoreal and never paired with Teo/Kai or 小川/大海. Teo/Kai are never restyled as anime Tagame. 大野健一 is not the office Tagame: do not swap their face references. 小川/大海 are photoreal and never share a frame with Teo/Kai. Their sheets are identity locks, not scenes.

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
| 小川, @小川, Ogawa, ogawa, characters/小川 | `ogawa` |
| 大海, @大海, Dahai, dahai, characters/大海 | `dahai` |

Do **not** use Tom / James. Those names are retired.

## Active cast

Resolve **before** loading bibles. One image uses one cast.

| User asked | Cast | Load |
|------------|------|------|
| @Teo / @Kai / virtual-couple，且没点小川或大海 | `teo_kai` | teo, kai |
| @小川 / @大海 / `characters/小川` / `characters/大海` / 「换成这两个」 | `ogawa_dahai` | ogawa, dahai |
| 两个 cast 都点了 | 停下来问要哪一对。不要生成。 | — |

`ogawa_dahai` 不读 Teo/Kai 的眼镜、圆寸、刺发、受攻。`teo_kai` 不读这两张设定表。

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

  ogawa:
    role: left
    pipeline: photoreal-swap
    reference: characters/小川/小川.png
    identity_prompt: |
      小川: East Asian man ~32, oval-rectangular face, straight brows,
      almond eyes, straight nose, calm closed mouth, light even stubble,
      no glasses. Short black hair with a little texture and lift on top,
      shorter faded sides, neat hairline. Not a buzz cut, not spiky, not
      a dry receding crop. Lean-to-average build, not stocky.
      Photoreal. The reference is a six-view head sheet: use it only for
      face and hair. Do not copy the gray backdrop or the panel grid.

  dahai:
    role: right
    pipeline: photoreal-swap
    reference: characters/大海/大海.png
    identity_prompt: |
      大海: East Asian Chinese man, 35–45, 175–180cm, stocky muscular
      build, broad back, thick arms. Short black hair, slightly messy and
      dry, a little recession at the temples. Thick brows, steady gaze,
      full cheeks, slightly wide square jaw, short beard and mustache.
      No glasses. Warm when smiling, otherwise the same face.
      Photoreal, grounded. The reference is a turnaround sheet: use the
      face and full-body views only. Do not copy the gray studio, the
      Front/45°/Side labels, the color swatches, or the printed text.
      Default clothes only when the user asked for 角色默认: olive-green
      work shirt, black cargo pants, brown work boots.
```

## Consistency rules

- Face identity from reference images has **highest priority**
- Do not merge Teo and Kai features
- Preserve glasses on Teo always
- Preserve Kai's mature muscular look always
- Tagame: default Japanese anime (never photoreal). If the user names CuteGuysArt, follow `.cursor/skills/cuteguysart/SKILL.md` and change only the rendering (bold contour lines, warm painterly skin, medium kind eyes, bright saturated lifestyle illustration). Keep the beard, dark-brown spiked hair, and his large natural muscle. Never slim, pretty-boy, or oversized anime eyes
- 大野健一: face and uniform from `characters/Tagame-patrol/full_body_char.jpeg`. Do not substitute the office Tagame reference. Scenes stay at the night bus depot
- 小川: face and hair from `characters/小川/小川.png` only. No glasses. Do not bulk him into 大海. Do not copy the six-view gray studio
- 大海: face, beard, hair, and stocky body from `characters/大海/大海.png`. Do not slim him. Do not copy the sheet layout or its printed bible
- 小川/大海 never share a frame with Teo/Kai. Double scenes default left=小川, right=大海 unless the user named the sides
