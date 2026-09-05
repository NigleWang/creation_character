# cover-collage examples

## Turn 1 口吻（节选）

素材：`outputs/approved/series/20260830_kai_plumber_series/` 4 张，仅 Kai，维修间。

```text
✅ 素材已读（原图像素拼接，不会重画人物；默认不叠字、不加角标）

【素材】4 张 · 仅Kai · 维修间水管 · 主图建议：源成图（看镜头、脸最清楚）

请选封面方案（回复 1 / 2 / 3）：

1️⃣ 四宫格 · 这是一组
2️⃣ 主图+三小图 · 点击率更高
3️⃣ 左主右辅 · 杂志感
```

笔记文案照常给三套；不要往封面上写钩子或「4图」。用户说「加字」才叠。

## Turn 2 JSON（默认）

`title` / `subtitle` / `badge` 留空：

```json
{
  "layout": "hero_3",
  "title": "",
  "subtitle": "",
  "badge": "",
  "out": "outputs/approved/series/20260830_kai_plumber_series/cover_hero_3.png"
}
```

```bash
python3 scripts/make_cover.py --config outputs/drafts/cover_20260830_kai_plumber_series.json
```
