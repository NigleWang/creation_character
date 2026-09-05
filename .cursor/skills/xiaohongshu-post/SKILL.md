---
name: xiaohongshu-post
description: >-
  Formats final Xiaohongshu (小红书) images — 3:4 aspect, cover-friendly
  composition, delivery layout. Caption/hashtags belong to xiaohongshu-caption
  (Teo/Kai). Use for 小红书 image delivery specs.
---

# Xiaohongshu Post Skill

## Image specs

| Field | Value |
|-------|-------|
| Aspect ratio | 3:4 (primary) |
| Min feel | High-res, cover-worthy, **same brightness as the scene/source still** |
| Style | Natural photograph, lifestyle / BL couple — not cinematic glow |
| Avoid | Watermarks, text overlays, explicit content, over-bright / HDR / beauty lighting |

## Caption

Do **not** write copy here. After QC, run `xiaohongshu-caption` (**Teo** / **Kai**, tags `#TeoKai` `#TeoKaiDaily`).

**pose-series:** one caption for the whole set.

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
