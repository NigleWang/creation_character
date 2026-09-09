---
name: prompt-builder
description: >-
  Builds the final GenerateImage prompt from character bibles, scene blueprint,
  and content type. Use before calling Cursor GenerateImage in creation_character.
---

# Prompt Builder

**Route out:** Tagame stills → `.cursor/skills/tagame-anime/SKILL.md` (anime prompt). This builder is Teo/Kai photoreal only.

## Input

- `character_bundle`
- `generation_blueprint`
- `scene_blueprint`
- `customization_manifest` from scene-customizer (**required** unless user said 全部保持原场景)
- `content_type` (default: `xiaohongshu_post`)

## Apply customization

For each character, resolve clothing/accessories from `customization_manifest`:

| `choice` | Prompt behavior |
|----------|-----------------|
| `keep_scene` | Use `scene_value` from scene blueprint |
| `character_default` | Teo → browline glasses; Kai → no glasses |
| specific value | Use user's color/item/pattern explicitly |

Add block to prompt:

```text
[STYLE CUSTOMIZATION — may differ from scene reference]

Teo accessories: {resolved}
Teo top: {color} {pattern} {type}
Teo bottom: {color} {pattern}

Kai accessories: {resolved}
Kai top: ...
Kai bottom: ...

Pose, composition, environment unchanged. Only these style details differ from scene where specified.
```

## Lighting lock (always)

Every GenerateImage prompt **must** include an explicit lighting block:

- Copy the scene / source still: direction, color temperature, contrast, **exposure**
- Do **not** brighten, lift shadows, add fill, beauty lighting, rim glow, HDR, or studio evenness
- Over-bright or glowing light looks AI-generated — treat as a hard fail
- Never write "cinematic", "cover-bright", or "warm studio" unless the reference actually looks that way
- Preserve **scene grime**: reflections on glass/metal, background clutter, uneven shadow falloff, mixed color temperature — do not clean up or polish the environment
- Vocabulary for realism: see `docs/light.md` (available light, imperfect exposure, natural falloff)

Face refs are for identity only. Do **not** inherit lighting from character face photos.

## Anti-AI realism module (always append)

After the lighting block, append this fixed module (from `docs/light.md` §6). Goal: **deliberately imperfect**, not "higher quality":

```text
[REALISM — reduce AI look]

natural available light, soft uneven lighting, subtle directional shadows,
natural light falloff, slightly imperfect exposure, natural dynamic range,
subtle highlight clipping, natural skin texture, visible pores and fine details,
slight optical softness, natural depth of field, subtle photographic grain,
minor imperfections, unretouched photographic look, candid photography,
not overly sharp, not overly polished, not airbrushed, no plastic skin,
no beauty filter, no HDR, no studio evenness.
Preserve scene reflections, clutter, and uneven shadows exactly as the reference.
Do not brighten any area for "cover" or "thumbnail" appeal.
```

## Template

Assemble one continuous `description` string for GenerateImage:

```text
[CHARACTER IDENTITY — highest priority]

Two recurring virtual East Asian male characters in a romantic couple.

LEFT person is Teo (受): {teo identity_prompt from character-registry}
RIGHT person is Kai (攻): {kai identity_prompt from character-registry}

Use the attached face reference images to preserve exact facial identity.
Teo must keep browline glasses and buzz cut. Kai must keep spiky hair and muscular build.

[SCENE — from scene_blueprint]

{environment.location}, {environment.time}.

[COMPOSITION — preserve reference]

Preserve the exact composition from the scene reference image.
{composition.framing}, {composition.camera_angle}.
Teo on the left, Kai on the right.
{aspect_ratio} vertical frame.

[POSE — inherit from scene]

{pose details for subject_1 → Teo}
{pose details for subject_2 → Kai}
{interaction.type}, {interaction.emotional_tone}.

[LIGHTING — match scene reference exactly]

Copy lighting from the scene reference: {environment.lighting}, {visual_style.lighting}.
Same light direction, color temperature, contrast, shadow density, and EXPOSURE.
Do not brighten the image. Do not lift shadows. Do not add fill light, beauty lighting, rim glow, HDR, or studio evenness.
Keep the original's darker areas dark. Over-bright, glowing, or overly clean light looks AI-generated — forbidden.
If the reference is dim, indoor, overcast, or mixed, keep that exact brightness. Never "improve" it.

[VISUAL STYLE]

{visual_style from scene}. Realistic skin texture. Natural documentary photography, not cinematic glow.
Natural intimate couple moment. Photorealistic, same grain and contrast as the scene reference.
Keep background clutter, surface reflections, and uneven shadow patches — do not sanitize the scene.

[REALISM — reduce AI look]

natural available light, soft uneven lighting, slightly imperfect exposure,
natural skin texture, subtle photographic grain, unretouched photographic look,
not overly sharp, not overly polished, not airbrushed. See docs/light.md.

[XIAOHONGSHU / CONTENT]

Vertical 3:4 portrait suitable for Xiaohongshu cover.
Attractive composition, clear faces, natural emotional tone.
Tasteful romantic BL couple content, not explicit.

[CONSTRAINTS]

Character identity overrides original people in scene reference.
Preserve: composition, body positions, interaction, camera angle, lighting, brightness, color grade.
Do not: swap Teo/Kai, change faces, merge faces, extra limbs, missing people.
Do not: overexpose, add glow, or make the scene look brighter than the reference.
No text, no watermark, no logo.
```

## Single character variant

Replace couple block with one character + "single person portrait, same pose, environment, and lighting/exposure as reference." Keep the lighting lock block.

## Wallpaper variant (`9:16`)

Add: "Leave negative space for mobile UI. Avoid placing faces in bottom third."

## Output

Save prompt to `outputs/drafts/prompt_<task_id>.txt` and pass full text to GenerateImage `description`.
