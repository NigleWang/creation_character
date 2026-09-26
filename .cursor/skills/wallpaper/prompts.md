# Wallpaper prompts

Fill every `{slot}` from `spec.json`. Do not leave a slot in the prompt.

Match the reference medium in every prompt: a Japanese anime illustration stays Japanese anime with crisp linework and cel shading. A photograph stays photoreal. Do not convert one into the other.

The subject is an asset. Background, fusion, and device prompts must not redesign the person.

## Subject — aspect_ratio `3:4`

References: source, plus a face ref only when the user named Teo or Kai.

`{key}` is `247,247,245`, or `0,177,64` when the clothes are close to that gray.

```text
Extract the complete main subject from the reference image.

Preserve the subject exactly as shown.

The subject includes:
{subject_parts}

Preserve the original:
- facial features
- hairstyle
- body proportions
- clothing
- pose
- hand positions
- held-object positions
- perspective

Do not redraw or redesign the subject.

Do not change the face.
Do not change the hairstyle.
Do not change the clothing.
Do not change the pose.
Do not change the body proportions.

Remove the entire background.

Remove:
{remove}

Frame the subject large, with only a thin margin of flat color around the body.

Output the subject on a perfectly flat rgb({key}) field, edge to edge.
That field must touch all four edges.
No gradient, no vignette, no texture, no floor, no contact shadow on the field.
The field is a removable key color, not a scene.

The extracted subject should retain clean edges and natural hair details.
Keep the light on the person and the original exposure. Do not brighten.

Match the reference medium. If the reference is a Japanese anime illustration, stay Japanese anime with crisp linework and cel shading. If it is a photograph, stay photoreal. Do not convert one into the other.

No text, logo, watermark, device frame, clock, widgets, or UI.
Do not duplicate the person. Do not mirror the image.
```

## Prop — aspect_ratio `1:1`

Only when `detached` is non-empty. Reference: source. One object, same key color.

```text
Extract only this object from the reference image: {detached_item}.

Preserve its shape, color, and material exactly. Do not redraw it as a different object.

Do not include any person, hands, clothing, or the rest of the scene.

Output the object on a perfectly flat rgb({key}) field, edge to edge.
No shadow, no floor, no text.
```

## Background — aspect_ratio `3:4`

Reference: source only. Do not pass the subject cutout or a face ref.

```text
Create a minimalist editorial background for a premium vertical wallpaper.

The visual concept is:
"{concept}"

Use the original image only as environmental reference.

DO NOT generate any person.
DO NOT generate any human figure.
DO NOT generate hands.
DO NOT generate clothing.
DO NOT generate a book.
DO NOT generate a bag.

The background should contain only the environment.

Simplify the original setting into a clean, aesthetically designed environment.

Preserve the visual language of:
{keep}

Remove unnecessary visual clutter:
{remove}
- excessive details
- distracting objects

Create strong visual hierarchy.

Background complexity:
- the central and lower area where a person will be placed: low detail, slightly darker
- the outer area: medium detail
- the far background: medium-high detail, still simplified

Use subtle depth of field:
foreground and distant elements slightly blurred,
while keeping enough architectural or spatial detail to establish the place.

Color palette:
{palette}

Lighting:
{lighting}
Gentle directional light, subtle ambient reflections.
Do not blow out the exposure.

Style:
premium editorial, cinematic, clean, minimalist, high-end wallpaper.
Same medium as the reference. Do not convert a photograph into anime, or anime into a photograph.

No text.
No people.
No logos.
No UI.

Vertical wallpaper composition.
Leave clean negative space in the central subject area.
```

## Fusion — aspect_ratio `3:4`

References, in order: `composite.png`, `subject.png`. Do not pass the original photo.

```text
Combine the provided foreground subject and background into a single premium wallpaper.

IMPORTANT:
The foreground subject is already finalized.
The composite already has the correct scale and position. Keep that placement.

Preserve the foreground subject exactly.

Do NOT regenerate the person's face.
Do NOT change the hairstyle.
Do NOT change the body proportions.
Do NOT change the clothing.
Do NOT change the hands.
Do NOT change objects held in the hands.
Do NOT change the pose.
Do NOT move or rescale the subject.

Only integrate the subject naturally into the environment.

COMPOSITION:

Vertical wallpaper.
The subject sits slightly below the vertical center.
The entire head, torso, arms, held objects, and any visible legs stay inside the frame.
Leave approximately 25% clean visual space above the subject.
The subject is the primary visual focus.
The environment stays secondary.

BACKGROUND:

{concept}
Reduce detail directly behind the subject.
Use subtle depth of field to separate the subject from the environment.

LIGHTING:

Match the lighting direction between subject and background.
Add subtle ambient light from the environment onto the subject.
Add a very soft contact shadow under the body.
Do not change the subject itself.
Do not brighten the person. Keep the original exposure.

STYLE:

Premium editorial wallpaper.
Cinematic, sophisticated, minimalist, high detail, clean composition.
Same medium as the references.

NO:
text
logos
watermarks
UI
phone frame
clock
widgets
additional people
```

## Adapt

Reference: `master.png` only.

| File | `{device}` | `{extend}` | `{space}` |
|------|------------|------------|-----------|
| iPhone | a 9:16 smartphone wallpaper | Extend the environment naturally above and below the existing artwork. | Create approximately 25–30% clean negative space in the upper portion. The upper area is only simplified environment, reserved for lock-screen time and widgets. Do not place the head or other important detail there. |
| iPad | a 4:3 tablet wallpaper | Extend the environment naturally to the left and right, and above or below if needed. | Keep the full subject visible, slightly below center. |
| Desktop | a 16:9 desktop wallpaper | Extend the environment naturally to the left and right. | Keep the full subject visible in the lower-middle. The top band is only simplified environment. |

```text
Convert the existing artwork into {device}.

IMPORTANT:
Preserve the existing subject exactly.

Do not regenerate the person.

Do not modify:
- face
- hair
- clothing
- hands
- objects held in the hands
- pose
- body proportions
- the subject's identity

{extend}

Move the complete composition slightly downward if needed so the subject stays fully visible.

{space}

Maintain the same:
- lighting
- color palette
- perspective
- medium and illustration or photographic style
- visual atmosphere

The environment stays secondary to the subject.
Do not brighten the person.

No text.
No UI.
No clock.
No device frame.
No additional people.
```

## Regeneration line

Append only the line for the check that failed.

Subject:

- `The field behind the subject is not one flat key color. Fill every background pixel with rgb({key}), edge to edge.`
- `The face does not match the reference. Copy the reference face exactly.`
- `The hands are malformed. Restore the reference hands and pose.`
- `The clothing, hair, or body was redesigned. Copy the reference subject exactly.`
- `The image is brighter than the reference. Restore the original exposure on the person.`

Background:

- `A person, hand, or held object appeared. Remove every human figure.`
- `The background still contains text, logos, or clutter. Remove them.`
- `The area behind the future subject is too detailed. Simplify that region.`

Fusion:

- `The face, hair, clothing, hands, or pose changed. Restore the subject from the second reference exactly.`
- `The subject was moved or rescaled. Keep the placement in the composite.`
- `The image is brighter than the subject reference. Restore the original exposure.`

Adapt:

- `The person was regenerated. Keep the master image's subject exactly and only extend the environment.`
- `The upper area is crowded. Leave clean simplified environment above the subject.`
