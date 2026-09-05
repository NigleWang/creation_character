---
name: cover-collage
description: >-
  Deterministic Pillow collage for Xiaohongshu cover / 首页拼接图 (1080x1440).
  Default is a clean collage with no overlay title, subtitle, scrim, or N图
  badge. Two-turn: analyze source stills, post 3 layout schemes + note copy
  and STOP; after the user picks one, run scripts/make_cover.py and deliver
  a single cover PNG. Use when the user says 拼接, 封面图, 封面拼图, 九宫格, 拼图,
  cover collage, or wants a homepage cover from several approved stills.
  Never call GenerateImage — pixels must stay the source frames.
---

# Cover Collage — 小红书首页拼接

封面拼图是**确定性图像合成**，不是模型生成。全程 `scripts/make_cover.py`（Pillow）算像素。

**禁止**调用 `GenerateImage`。走生图会把人物重画，和系列图对不上。

源技术：`docs/joint_imgs.md`。笔记正文走 `xiaohongshu-caption` 公式。

**默认封面是纯拼图：** 不叠主标题、副标题、渐变压暗、右上角「N图」。文字层只在用户明确说「加字 / 加角标 / 叠字」时才画。

| Turn | When | Do | Forbidden |
|------|------|-----|-----------|
| **1** | User gave 2+ stills, no scheme pick yet | Read frames → **3 numbered layouts + 笔记文案** → STOP | `GenerateImage`、跑拼接脚本、默认往封面上写字 |
| **2** | User replies `1` / `2` / `3` | Write JSON（title/subtitle/badge 默认空）→ `make_cover.py` → 交一张封面 | 再出另外两版（除非用户要） |

Skip Turn 1 only if the first message already picks a layout, e.g. `用主图+三小图`.

---

## Route in / out

**In:** 拼接 / 封面图 / 封面拼图 / 九宫格 / 拼图 / 首页封面 / 多图拼一张；或指着 `outputs/approved/series/<id>/` 要封面。

**Out:**

- 换脸新场景 → `virtual-couple`
- 已有成图换姿态 → `pose-series`（一组图里**每张单独出**，不要拼）
- 只要笔记文案、不要封面 → `xiaohongshu-caption`
- Tagame 出静帧 / 视频词 → `tagame-anime`（本 skill 只拼**已经存在的**静帧）

---

## Hard rules

1. Canvas **1080×1440**（3:4），`GUTTER = 6px`，底色纯白。
2. 等比填充裁切（`fill_crop`），禁止直接 resize 拉变形。
3. 人像 `crop_bias` **0.28–0.4**（脸在上部）。禁止默认 0.5 居中裁。
4. 用户没要求加字时：**禁止**叠标题、副标题、底部渐变、右上角「N图」。
5. 只有用户明确要加字时才画文字层；基线 = **所属那块图的底边**，不是画布底边。只压暗底部做白字可读，**禁止提亮**人物。
6. 加字时强调色从画面主体取高饱和色，不要写死黄（缺省才用 `255,214,51`）。
7. 落盘必须在系列文件夹：`outputs/approved/series/<task_id>/cover_<layout>.png`。`.gitignore` 忽略 `outputs/approved/*`，只放行 `series/**/*.png`。
8. 笔记标题 ≤20 字。若用户要求封面叠字：封面钩子 ≤10 字，且 **≠ 笔记标题**。

---

## Turn 1 — 三套方案 + 笔记文案（不出图）

1. 收齐有序路径（用户 @ 的图，或系列目录里 `01_*.png`…）。角标 `{N}图` **不要默认画上**；N 只用于笔记里说明系列张数。
2. 读 1–3 张（建议主图 + 一张中景 + 末张）。辨认 cast：仅 Kai / 仅 Teo / 双人。
3. 选主图：脸在画面上三分之二、情绪最清楚的那张。
4. 写 `outputs/drafts/cover_plan_<task_id>.json`（`user_confirmed: false`；各方案 `title`/`subtitle`/`badge` 留空）。
5. 按张数组三套方案：**布局 + 用图顺序 + 笔记文案**。不要在方案里写封面叠字，除非用户已经说要加字。
6. 按回复模板贴出。**END。不要跑脚本。**

### 三套布局（按张数）

| # | `layout` | 何时强 | 用图 |
|---|----------|--------|------|
| 1 | `grid_2x2` | 「这是一组」、节奏平均 | **必须 4 张**。不足 4 张时改成 `hero_3`（1+2）并在方案里说明 |
| 2 | `hero_3` | 单一焦点、点击率通常更高 | 主图 + 底栏最多 3 张（共 3–4） |
| 3 | `hero_side` | 杂志感、竖屏信息密 | 左主图 + 右侧叠 2–3 张 |

默认裁切：`grid_2x2` 全 0.4；`hero_3` / `hero_side` 主图 0.28、辅图 0.32。某张脸仍偏低就在方案里写更大/更小的 bias。

### 笔记文案（封面默认不叠字）

默认 JSON：`title` `subtitle` `badge` 都为空。封面 = 纯拼图。

笔记复制块仍要写（发小红书用），公式见 `xiaohongshu-caption`：

| | 封面（默认） | 笔记复制块 |
|--|-------------|------------|
| 叠字 | **无** | 标题 ≤20 字 |
| 角标 | **无** | — |
| 正文 | 不要写在封面上 | 30–80 字：小场景 + 细节 + 一点情绪 |
| 标签 | 不要写在封面上 | 6–10 个，`#TeoKai` `#TeoKaiDaily` 必带 |

人名 **Teo / Kai**。不要虚拟、AI、换脸。三套笔记标题不要撞题。

**仅当用户说「加字 / 加角标 / 叠字」时：** 封面钩子 ≤10 字、可加副标题、角标 `{N}图`（N = 系列总张数）；封面钩子 ≠ 笔记标题；JSON 才填 `title`/`subtitle`/`badge`/`accent`。

### Turn 1 回复模板

```text
✅ 素材已读（原图像素拼接，不会重画人物；默认不叠字、不加角标）

【素材】{N} 张 · {仅Kai / 仅Teo / 双人} · {场景一句} · 主图建议：第 {k} 张（{原因}）

请选封面方案（回复 1 / 2 / 3，可换主图）：

1️⃣ 四宫格 · 这是一组
📐 {2×2 / 张数不够时的替代说明}
🖼 顺序：左上{文件} · 右上… · 左下… · 右下…
✂️ bias：{0.4 / …}

2️⃣ 主图+三小图 · 点击率更高
📐 上主图 + 底{2或3}格
🖼 主图：{文件}；底栏：…
✂️ bias：主 0.28 / 辅 0.32

3️⃣ 左主右辅 · 杂志感
📐 左主图 + 右叠{2或3}
🖼 主图：{文件}；右侧从上到下：…
✂️ bias：主 0.28 / 辅 0.32

【笔记 · 方案1】
```

紧接着 **三个** `text` fence（方案 1/2/3 各一块），格式与 `xiaohongshu-caption` 相同：标题空行正文空行标签。

结尾：

```text
⏸️ 请回复方案编号后我再拼接封面（例如：2）。要叠字再说「加字」或「加 8图 角标」。
```

---

## Turn 2 — 拼一张

1. 解析编号 + 用户改的主图/顺序。默认 **不要** 填 title/subtitle/badge。
2. 写 `outputs/drafts/cover_<task_id>.json`，`"user_confirmed": true`。
3. 探测依赖：`python3 -c "from PIL import Image"`；失败则 `pip3 install Pillow`。默认纯拼图不需要中文字体；加字时脚本会找 wqy-microhei / PingFang / Hiragino。
4. 从仓库根目录：

```bash
python3 scripts/make_cover.py --config outputs/drafts/cover_<task_id>.json
```

5. `Read` 成品图做目视 QC（见下）。失败则改 `crop_bias` / 换主图后重跑脚本，**不要** GenerateImage。
6. 回复：成品图 + 一句 QC + **选用的那条**笔记复制块 + 文件路径。不要把另外两套文案再贴一遍。

### JSON（脚本可读字段 + 计划元数据）

脚本只读：`frames` `layout` `title` `subtitle` `badge` `accent` `crop_bias` `out`。默认三字字段留空，脚本就不画文字层。

```json
{
  "task_id": "20260830_kai_plumber_series",
  "user_confirmed": true,
  "scheme": 2,
  "frames": [
    "outputs/approved/series/20260830_kai_plumber_series/xiaohongshu_20260830_kai_plumber.png",
    "outputs/approved/series/20260830_kai_plumber_series/01_crouch_repair.png",
    "outputs/approved/series/20260830_kai_plumber_series/02_sit_break.png",
    "outputs/approved/series/20260830_kai_plumber_series/03_wire_check.png"
  ],
  "layout": "hero_3",
  "title": "",
  "subtitle": "",
  "badge": "",
  "crop_bias": [0.28, 0.32, 0.32, 0.32],
  "out": "outputs/approved/series/20260830_kai_plumber_series/cover_hero_3.png",
  "note": {
    "title": "水管修好之前他不打算走",
    "body": "…",
    "tags": ["#TeoKai", "#TeoKaiDaily"]
  }
}
```

`out` 文件名：`cover_grid_2x2.png` / `cover_hero_3.png` / `cover_hero_side.png`。若系列还没有文件夹，先 `mkdir` 再写。

加字时才填 `accent`；纯拼图不要写 accent。

---

## QC（拼图，不是生图）

| 项 | 通过 |
|----|------|
| 尺寸 | 1080×1440 |
| 身份 | 与源帧同一张脸，无重绘感 |
| 变形 | 人体比例正常（fill_crop，非拉伸） |
| 脸 | 没被裁掉头 |
| 叠字 | **默认无**标题、副标题、渐变、右上角 N图 |
| 曝光 | 未提亮；白缝 6px 清楚 |

用户要求加字时额外查：文字叠在所属图底边；B 版没盖住底栏；角标 N = 系列总张数。

`fail` → 调 bias / 换主图后重跑脚本。

---

## 脚本参数

| 参数 | 说明 |
|------|------|
| `frames` | 有序路径，数量决定格子 |
| `layout` | `grid_2x2` / `hero_3` / `hero_side` |
| `title` / `subtitle` / `badge` | 默认空。有值才叠字 / 角标 |
| `accent` | 仅加字时需要，`[R,G,B]` |
| `crop_bias` | 每格一个 0–1，人像默认见上 |
| `out` | 系列文件夹内 png |

---

## Routing

- 用户要封面但只给了一张图 → 请他补系列帧，或去 `pose-series` 先出组图
- 选完方案后又要改裁切/主图 → 改 JSON 重跑脚本，不重新出三套
- 要给已拼好的封面加字 → 填 title/subtitle/badge 后重跑，不重新出三套
- 只要文案 → `xiaohongshu-caption`，本 skill 停在文案、不拼图
