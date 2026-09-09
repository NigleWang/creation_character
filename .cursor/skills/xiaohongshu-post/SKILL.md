---
name: xiaohongshu-post
description: >-
  Formats final Xiaohongshu (小红书) images — 3:4 aspect, cover-friendly
  composition, delivery layout. Caption/hashtags belong to xiaohongshu-caption
  (Teo/Kai). Tag mix: half self-built (#TeoKai #TeoKaiDaily) + half discovery
  pool. Use for 小红书 image delivery specs.
---

# Xiaohongshu Post Skill

## Image specs

| Field | Value |
|-------|-------|
| Aspect ratio | 3:4 (primary) |
| Min feel | High-res, cover-worthy, **same brightness as the scene/source still** |
| Style | Natural photograph, lifestyle / BL couple — not cinematic glow, not over-polished |
| Avoid | Watermarks, text overlays, explicit content, over-bright / HDR / beauty lighting, sanitized "clean" backgrounds |

## Pre-publish QC (mandatory)

Before delivery, `quality-control` must pass the anti-AI gate:

- Exposure not brighter than scene/source
- Scene grime preserved (reflections, clutter, uneven shadows)
- No plastic skin / HDR / studio evenness
- **pose-series:** face, hairstyle, outfit locked across all frames; run gate per frame + cross-frame check

See `docs/light.md` for prompt vocabulary.

## Caption

Do **not** write copy here. After QC, run `xiaohongshu-caption`（**Teo** / **Kai**）。标签按下面策略组好再交给 caption。

**pose-series:** one caption for the whole set.

## 标签策略：自建词 + 大池子各一半

总标签 **6–10** 个。**自建词和大池子大约各一半**（8 个 = 4+4）。保留 `#TeoKai` `#TeoKaiDaily`，同时按画面加。不必写 AI/虚拟，但 **别只用自建标签**。

### 自建词（账号沉淀，约一半）

每条必带：`#TeoKai` `#TeoKaiDaily`

再补满一半：`#双人设` `#固定角色`

### 大池子（按画面选，约一半）

从画面里挑，优先这组：

`#氛围感男生` `#男生拍照` `#健身` `#人夫感` `#日常碎片`

| 画面 | 用 |
|------|----|
| 男生单人 / 氛围照 | `#氛围感男生` `#男生拍照` |
| 生活片段、碎片感 | `#日常碎片` |
| 居家、成熟、照顾感 | `#人夫感` |
| 健身、运动、肌肉、工装出力 | `#健身` |

对不上画面的不要硬加（办公室坐着不要乱打 `#健身`）。还差条数时，从 caption 的内容类型 / 氛围池补，仍算大池子。

### 禁止

`#AI` `#虚拟` `#虚拟情侣` `#BL` — 正文也不写这些。

## Cover tips (prompt additions)

When user asks for **拼接封面 / 九宫格 / 多图拼一张** → `cover-collage` (Pillow), not GenerateImage.

When user asks for 封面 / cover on a **single generated still**:

- Faces in upper two-thirds
- Clear emotional beat (eye contact, smile, embrace)
- Do **not** brighten or add contrast/glow to make it "cover-like" — keep original lighting

## Delivery format

Reply structure:

1. **成品图** — generated image
2. **QC 评分** — brief scores
3. **建议标题 + 正文 + 标签** — via `xiaohongshu-caption`，copy-paste ready
4. **文件路径** — 单图 `outputs/approved/xiaohongshu_<task_id>.png`；组图 `outputs/approved/series/<task_id>/`
