---
name: virtual-couple
description: >-
  Xiaohongshu virtual couple content pipeline. Generates 3:4 portrait images of
  Tom (受) and James (攻) from a user-uploaded scene reference. Use when the user
  @mentions Tom, James, virtual-couple, uploads a scene photo, or asks for
  小红书/情侣/角色/换脸/场景图 content in creation_character.
---

# Virtual Couple Studio — Main Workflow

Orchestrates the full pipeline: **Character → Scene Analysis → Compose → Generate → QC → Deliver**.

## When to run

User provides (any combination):
- Scene reference image (upload in chat or path under `scenes/`)
- `@Tom` / `@James` / both / `@virtual-couple`
- Optional: content type (`couple_daily`, `single`, `wallpaper`, `xiaohongshu_post`)

**Always read this skill first**, then load sub-skills only as needed.

## Mobile / Cursor remote usage

Works on Cursor mobile: user uploads scene image in chat, then sends:

```text
@virtual-couple @Tom @James
情侣日常，保持场景构图
```

Or single character:

```text
@virtual-couple @Tom
单人日常，参考这张场景
```

Agent must execute the full pipeline in one session — do not stop after analysis.

## Pipeline checklist

Copy and track:

```
- [ ] 1. Parse user intent (characters, content type, scene path)
- [ ] 2. Load character bibles → read character-registry skill
- [ ] 3. Analyze scene → read scene-analyzer skill, write scene_blueprint.json
- [ ] 4. Compose binding → read character-composer skill
- [ ] 5. Build prompt → read prompt-builder skill
- [ ] 6. Generate image → CallDynamicTool cursor/GenerateImage
- [ ] 7. Quality control → read quality-control skill
- [ ] 8. Save to outputs/ + return Xiaohongshu-ready asset
```

## Step 1 — Parse input

Determine:

| Field | Default | Notes |
|-------|---------|-------|
| `characters` | `[tom, james]` if couple scene with 2 people | Single `@Tom` → only Tom |
| `content_type` | `xiaohongshu_post` | 3:4 vertical |
| `aspect_ratio` | `3:4` | Xiaohongshu standard |
| `scene_reference` | User upload or latest in `scenes/` | Save uploads to `scenes/` |

Write task manifest to `outputs/drafts/task_<YYYYMMDD_HHMM>.json`:

```json
{
  "task_id": "20260829_001",
  "characters": ["tom", "james"],
  "content_type": "xiaohongshu_post",
  "scene_reference": "scenes/scene_001.jpg",
  "generation_config": {
    "aspect_ratio": "3:4",
    "style": "cinematic_realistic",
    "num_images": 1
  },
  "constraints": {
    "preserve_character_identity": true,
    "preserve_scene_composition": true,
    "preserve_scene_pose": true
  }
}
```

## Step 2–5 — Sub-skills

Read in order (paths relative to project root):

1. [.cursor/skills/character-registry/SKILL.md](.cursor/skills/character-registry/SKILL.md)
2. [.cursor/skills/scene-analyzer/SKILL.md](.cursor/skills/scene-analyzer/SKILL.md)
3. [.cursor/skills/character-composer/SKILL.md](.cursor/skills/character-composer/SKILL.md)
4. [.cursor/skills/prompt-builder/SKILL.md](.cursor/skills/prompt-builder/SKILL.md)

## Step 6 — Image generation (required)

Use **Cursor built-in GenerateImage** via `CallDynamicTool`:

```json
namespace: "cursor"
toolName: "GenerateImage"
arguments: {
  "description": "<full prompt from prompt-builder>",
  "filename": "xiaohongshu_<task_id>.png",
  "aspect_ratio": "3:4",
  "reference_image_paths": [
    "<scene_reference_path>",
    "characters/tom/references/face_01.jpeg",
    "characters/james/references/face_01.jpeg"
  ]
}
```

**Reference image order matters:**
1. Scene reference (composition/pose)
2. Tom face reference (if in scene)
3. James face reference (if in scene)

For single-character tasks, only include that character's reference.

Only include character refs that are in the scene. Always include scene ref when user provided one.

## Step 7 — Quality control

Read [.cursor/skills/quality-control/SKILL.md](.cursor/skills/quality-control/SKILL.md).

If QC fails → regenerate once with tightened prompt (emphasize failed checks). Max 2 attempts.

## Step 8 — Deliver

On pass:
- Move/copy final image to `outputs/approved/`
- Reply with:
  - Image (tool output displays automatically)
  - Brief QC score summary
  - Suggested Xiaohongshu caption (1–2 sentences, 受/攻 dynamic tone)
  - Hashtag suggestions: `#情侣日常 #虚拟男友 #BL #氛围感`

On fail after retries:
- Save to `outputs/rejected/` with QC notes

## Character quick reference

| Name | Role | Side default | Reference |
|------|------|--------------|-----------|
| Tom | 受 | left | `characters/tom/references/face_01.jpeg` |
| James | 攻 | right | `characters/james/references/face_01.jpeg` |

## Content type routing

| User says | content_type | aspect_ratio |
|-----------|--------------|--------------|
| 壁纸 / wallpaper | wallpaper | 9:16 |
| 单人 / @Tom only / @James only | single_daily | 3:4 |
| 情侣 / couple / default | couple_daily or xiaohongshu_post | 3:4 |
| 小红书 | xiaohongshu_post | 3:4 |

For wallpaper skill extras, also read [.cursor/skills/xiaohongshu-post/SKILL.md](.cursor/skills/xiaohongshu-post/SKILL.md).

## Critical rules

```
Character controls IDENTITY.
Scene controls COMPOSITION and ACTION.
Neither overrides the other.

LEFT → Tom (受)
RIGHT → James (攻)
```

Never describe or replicate identities of people in the scene reference — extract structure only.
