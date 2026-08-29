---
name: xiaohongshu-post
description: >-
  Formats final images and captions for Xiaohongshu (小红书) posting — 3:4
  aspect, hashtags, cover-friendly composition. Use for 小红书 content delivery.
---

# Xiaohongshu Post Skill

## Image specs

| Field | Value |
|-------|-------|
| Aspect ratio | 3:4 (primary) |
| Min feel | High-res, cover-worthy |
| Style | Cinematic, warm, lifestyle / BL couple |
| Avoid | Watermarks, text overlays, explicit content |

## Caption template

After QC pass, generate for user:

```text
【标题】{short emotional hook, ≤20 chars}

{1-2 sentences scene description in casual 小红书 tone}

#情侣日常 #虚拟情侣 #BL #氛围感 #恋爱日常 #{scene_tag}
```

**pose-series:** One caption for the set. Title may include `办公室日常` / `1/n`. Same hashtags; add scene tag like `#办公室`.

## Scene tag examples

`#咖啡馆` `#雨天` `#居家` `#旅行` `#海边` `#圣诞`

## Cover tips (prompt additions)

When user asks for 封面 / cover:

- Faces in upper two-thirds
- Strong color contrast
- Clear emotional beat (eye contact, smile, embrace)

## Delivery format

Reply structure:

1. **成品图** — generated image
2. **QC 评分** — brief scores
3. **建议标题 + 正文 + 标签** — copy-paste ready
4. **文件路径** — `outputs/approved/xiaohongshu_<task_id>.png`
