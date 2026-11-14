---
name: virtual-couple
description: >-
  Xiaohongshu photoreal swap pipeline. Default cast is Teo (受, left) and
  Kai (攻, right). If the user @小川, @大海, characters/小川, characters/大海,
  or says 换成这两个形象, use that cast instead: 小川 left, 大海 right, same
  two-turn protocol. Turn 1 posts numbered style options; Turn 2 generates
  after the reply. Use when the user uploads a scene photo, @mentions Teo,
  Kai, 小川, 大海, virtual-couple, 换脸, or 小红书. Do not use for Tagame.
---

# Virtual Couple Studio

**Route out:** Existing `outputs/approved/` still + 系列/换姿态/其他 pose → use `pose-series`, not this skill.

**Route out:** Text-only scene (no photo) → use `text-scene`, not this skill.

**Route out:** @Tagame / `characters/Tagame` / 动漫画风肌肉上司 → use `tagame-anime`, not this skill.

**Route out:** 已有多张成图 + 拼接/封面/九宫格 → use `cover-collage`, not this skill.

## Cast（先定人，再问衣服）

| 用户点了 | 用谁 | 参考图 |
|----------|------|--------|
| Teo / Kai，没点小川或大海 | 左 Teo，右 Kai | `characters/teo/references/face_01.jpeg`，`characters/kai/references/face_01.jpeg` |
| 小川 / 大海 / `characters/小川` / `characters/大海` / 换成这两个形象 | 左 **小川**，右 **大海** | `characters/小川/小川.png`，`characters/大海/大海.png` |

两对不要出现在同一张图。两对都点了就停下来问。

小川 / 大海的参考图是**设定表**，不是场景。GenerateImage 的 `reference_image_paths` 里可以带上它们，提示词里写明：只取脸、头发、胡须、身材；不要灰底、分格、Front/45°/Side 标签、色卡、印刷文字。大海的表还锁结实体型。小川的表只有头肩，不要把他画成大海那么壮。

双人场景只点了一个名字：Turn 1 写明默认左小川、右大海。用户回「只换小川」或「只换大海」时，只出那一个人。

装饰物的「角色默认」：Teo = 眉框眼镜；Kai、小川、大海 = 无眼镜。  
「角色默认服装」只在用户这么说时用：小川 = 深灰圆领 T；大海 = 橄榄绿工装衬衫、黑工装裤、棕色工装靴。没说就跟场景衣服。

## ⚠️ TWO-TURN PROTOCOL (read first)

| Turn | When | Do | Forbidden |
|------|------|-----|-----------|
| **1** | User uploads scene, no style choices yet | Analyze + **post numbered text options** + STOP | GenerateImage |
| **2** | User replies with choices | Write manifest → GenerateImage → QC | — |

Skip Turn 1 only if user's first message includes e.g. `全部保持原场景` or `角色默认，上衣藏青`.

**Mobile/cloud:** AskQuestion does NOT work. Always post text options in chat.

---

## Turn 1 — Ask (mandatory unless choices pre-specified)

After analyzing scene, reply with this exact structure:

```text
✅ 场景已分析（构图/动作/环境将保持不变）

换脸前请确认（回复数字或文字）：

【{角色名}】（单人只列被点名的人；双人两块都列。Teo/Kai 或 小川/大海，不要混）
1️⃣ 装饰物：1保持原场景({value}) 2角色默认 3墨镜 4耳机 5无装饰
2️⃣ 上衣颜色：1保持({value}) 2白 3藏青 4浅蓝 5黑
3️⃣ 上衣图案：1保持 2纯色 3条纹 4格子
4️⃣ 下装颜色：1保持({value}) 2黑 3灰 4藏青

快捷：「全部保持原场景」

⏸️ 请回复后我再生成图片。
```

**Then END this turn. Do not call GenerateImage.**

Character defaults: Teo → browline glasses. Kai、小川、大海 → no glasses.

---

## Turn 2 — Generate (after user reply)

1. Parse user reply → write `outputs/drafts/customization_<task_id>.json` with `"user_confirmed": true`
2. Load the active cast from `character-registry`（Teo/Kai，或 小川/大海）
3. Build prompt (include customization choices)
4. Call `GenerateImage` via CallDynamicTool:

```json
namespace: "cursor"
toolName: "GenerateImage"
arguments: {
  "description": "<prompt>",
  "filename": "xiaohongshu_<task_id>.png",
  "aspect_ratio": "3:4",
  "reference_image_paths": ["<scene>", "<character refs>"]
}
```

5. QC → save **single** to `outputs/approved/xiaohongshu_<task_id>.png` → run `xiaohongshu-caption` if user wants 文案. pose-series sets use `outputs/approved/series/<task_id>/` then **must** run `xiaohongshu-caption`.
6. 按下面「Cloud 客户端显示」嵌图。`outputs/` 路径只作归档说明，不拿来当预览图。

**Pre-publish:** QC must pass the anti-AI gate in `quality-control` (exposure, scene grime, no polish) before any file lands in `outputs/approved/`.

---

## Characters

| Name | Role | Side | Reference |
|------|------|------|-----------|
| Teo | 受 | left | `characters/teo/references/face_01.jpeg` |
| Kai | 攻 | right | `characters/kai/references/face_01.jpeg` |
| 小川 | 写实，默认左 | left | `characters/小川/小川.png` |
| 大海 | 写实，默认右 | right | `characters/大海/大海.png` |

一次只用一对。小川/大海不是受攻。

## Rules

```
Character = IDENTITY (face, body, hair)
Scene = COMPOSITION + POSE + ENVIRONMENT + LIGHTING/EXPOSURE + SCENE GRIME
Customization = accessories/clothing (user confirms, may differ from scene)
LEFT = Teo | RIGHT = Kai — never swap
LEFT = 小川 | RIGHT = 大海 — never swap, and never mix with Teo/Kai
Character sheets are not the scene. Do not reproduce their gray studio.
Lighting must match the scene photo. Do not brighten. Over-bright = AI look.
Preserve reflections, clutter, uneven shadows — do not sanitize the scene.
```

## Cloud 客户端显示

手机端 / 远程 Cloud 不会自动贴出 `GenerateImage` 卡片。最终回复里这张图单独一行 Markdown，只用一个路径。不要只写「路径在 xxx」，不要用 HTML `<img>`，不要再嵌一条备用路径。

不要 embed `outputs/`（含 `/workspace/outputs/approved/…`）或 `/home/ubuntu/.cursor/projects/…/assets/…`。

1. 归档到 `outputs/approved/xiaohongshu_<task_id>.png`。系列目录只跟踪真 PNG：磁盘上是 JPEG 时用 Pillow 转成 PNG，禁止 `cp` 改后缀。
2. 再复制到 `/workspace/artifacts/`（本地是仓库根 `artifacts/`，不提交）。扩展名跟二进制走：文件头 `FF D8` 用 `.jpg`，`89 50 4E 47` 用 `.png`。
3. 回复嵌工具已经写入的 `/opt/cursor/artifacts/assets/` 路径（通常是 `.jpg`）。该目录不存在时，改嵌第 2 步的绝对路径。

```markdown
![成图](/opt/cursor/artifacts/assets/xiaohongshu_<task_id>.jpg)
```

Before delivery: run quality-control pre-publish gate (exposure + AI polish + grime).
Prompt realism module: docs/light.md §6 via prompt-builder.

## Sub-skills (Turn 2 detail)

- `character-registry`, `scene-analyzer`, `scene-customizer`, `character-composer`, `prompt-builder`, `quality-control`, `xiaohongshu-caption`, `xiaohongshu-post`

See also: `AGENTS.md` at project root.
