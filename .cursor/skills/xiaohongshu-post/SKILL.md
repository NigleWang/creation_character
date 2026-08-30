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
| Min feel | High-res, cover-worthy |
| Style | Cinematic, warm, lifestyle / BL couple |
| Avoid | Watermarks, text overlays, explicit content |

## Caption

Do **not** write copy here. After QC, run `xiaohongshu-caption` (**Teo** / **Kai**, tags `#TeoKai` `#TeoKaiDaily`).

**pose-series:** one caption for the whole set.

## Cover tips (prompt additions)

When user asks for 封面 / cover:

- Faces in upper two-thirds
- Strong color contrast
- Clear emotional beat (eye contact, smile, embrace)

## Delivery format

Reply structure:

1. **成品图** — generated image
2. **QC 评分** — brief scores
3. **建议标题 + 正文 + 标签** — via `xiaohongshu-caption`，copy-paste ready
4. **文件路径** — 单图 `outputs/approved/xiaohongshu_<task_id>.png`；组图 `outputs/approved/series/<task_id>/`
