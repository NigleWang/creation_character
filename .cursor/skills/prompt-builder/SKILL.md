---
name: prompt-builder
description: >-
  Builds the final GenerateImage prompt from character bibles, scene blueprint,
  and content type. Use before calling Cursor GenerateImage in creation_character.
---

# Prompt Builder

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
| `character_default` | Tom → browline glasses; James → no glasses |
| specific value | Use user's color/item/pattern explicitly |

Add block to prompt:

```text
[STYLE CUSTOMIZATION — may differ from scene reference]

Tom accessories: {resolved}
Tom top: {color} {pattern} {type}
Tom bottom: {color} {pattern}

James accessories: {resolved}
James top: ...
James bottom: ...

Pose, composition, environment unchanged. Only these style details differ from scene where specified.
```

## Template

Assemble one continuous `description` string for GenerateImage:

```text
[CHARACTER IDENTITY — highest priority]

Two recurring virtual East Asian male characters in a romantic couple.

LEFT person is Tom (受): {tom identity_prompt from character-registry}
RIGHT person is James (攻): {james identity_prompt from character-registry}

Use the attached face reference images to preserve exact facial identity.
Tom must keep browline glasses and buzz cut. James must keep spiky hair and muscular build.

[SCENE — from scene_blueprint]

{environment.location}, {environment.time}. {environment.lighting}.

[COMPOSITION — preserve reference]

Preserve the exact composition from the scene reference image.
{composition.framing}, {composition.camera_angle}.
Tom on the left, James on the right.
{aspect_ratio} vertical frame.

[POSE — inherit from scene]

{pose details for subject_1 → Tom}
{pose details for subject_2 → James}
{interaction.type}, {interaction.emotional_tone}.

[VISUAL STYLE]

{visual_style from scene}. Realistic skin texture. Cinematic film photography.
Natural intimate couple moment. High detail, photorealistic.

[XIAOHONGSHU / CONTENT]

Vertical 3:4 portrait suitable for Xiaohongshu cover.
Attractive composition, clear faces, warm emotional tone.
Tasteful romantic BL couple content, not explicit.

[CONSTRAINTS]

Character identity overrides original people in scene reference.
Preserve: composition, body positions, interaction, camera angle, lighting.
Do not: swap Tom/James, change faces, merge faces, extra limbs, missing people.
No text, no watermark, no logo.
```

## Single character variant

Replace couple block with one character + "single person portrait, same pose and environment as reference."

## Wallpaper variant (`9:16`)

Add: "Leave negative space for mobile UI. Avoid placing faces in bottom third."

## Output

Save prompt to `outputs/drafts/prompt_<task_id>.txt` and pass full text to GenerateImage `description`.
