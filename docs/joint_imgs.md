下面是这次封面拼图的完整技术方案，按你写 skill 需要的粒度整理。

**已落地：** `.cursor/skills/cover-collage/SKILL.md` + `scripts/make_cover.py`（`grid_2x2` / `hero_3` / `hero_side`）。两轮：先出 3 套方案+文案，确认后再拼一张。**默认不叠字、不加右上角 N图**；用户明确说「加字 / 加角标」才画文字层。

## 核心定位

封面拼图是**确定性图像合成**，不是模型生成。全程用 Pillow 计算像素，不调 `GenerateImage`。这一点应该作为 skill 的第一条路由规则：用户说「拼接 / 封面图 / 九宫格 / 拼图」时走脚本，不要走生图，否则人物会被重画、和系列图对不上。

依赖只有两项，环境里都需要先探测：Pillow（`pip3 install Pillow`，本机原本没有）和中文字体（`fc-list :lang=zh` 找到 `/usr/share/fonts/truetype/wqy/wqy-microhei.ttc`）。

## 画布与栅格

画布固定 1080×1440，即小红书封面的 3:4。格子间距 `GUTTER = 6px`，底色纯白，白缝在深色水面上形成清晰分隔。

两种布局，都由「格子矩形列表」驱动，加新布局只要加一组矩形：

```python
# A 四宫格：cell = ((W-G)//2, (H-G)//2)，四个原点
# B 主图+三小图：hero = (W, H-strip_h-G)，strip 三格 = ((W-2G)//3, 400)
```

A 版适合表达「这是一组」，B 版单一焦点更强、点击率通常更高。同一批素材两版都出，让用户挑，成本极低。

## 等比填充裁切（关键函数）

源图是 3:4，格子可能是任意比例（B 版小图接近 1:1），所以不能直接 resize，否则人物会被拉变形。做法是按 `max(tw/sw, th/sh)` 放大到刚好覆盖格子，再裁掉多余部分：

```27:36:/workspace/scripts/make_cover.py
def fill_crop(img, size, bias=0.4):
    """Scale and crop so img exactly covers size; bias<0.5 keeps more of the top."""
    tw, th = size
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = int((nh - th) * bias)
    return img.crop((left, top, left + tw, top + th))
```

`bias` 是这里最重要的参数：纵向裁切位置，0.5 是居中，小于 0.5 保留更多上半部分。人像必须用 0.28–0.4，因为脸在画面上部，居中裁会把头切掉或把脸推到标题层底下。B 版主图用 0.28，小图用 0.32，A 版用 0.4。写 skill 时应该把它作为显式参数暴露，而不是写死。

## 文字层

三个部分共用一个 `decorate()`，靠 `bottom` 参数决定挂在哪条基线上，这是 B 版布局的关键。

**渐变压暗**：单独建一张 RGBA 图，逐行画线，alpha 按 `(i/h) ** 1.7` 递增到 215，底色 `(8, 20, 26)`。指数大于 1 让过渡更集中在底部，上方几乎无损。这一层是为了让白字在明亮水面上可读，同时**不提亮人物**——直接给整图加亮度会破坏系列的曝光一致性。

**伪粗体**：文泉驿没有 Bold 字重，所以在半径 `weight` 的圆形偏移内重复绘制同一段文字。`weight=3` 视觉上接近 Bold，再大会糊。

**主标题 + 副标题**：主标题 96px 白色伪粗体，副标题 46px 淡黄，前面加一根 9px 宽的黄色竖条。所有纵向位置从 `bottom` 反推（`sub_y = bottom - margin - sub_h - 10`），换标题长度不用手工调坐标。

**角标**：右上角圆角矩形 + 「8图」，用 `textbbox` 居中。这是转化设计，不是装饰——它明示还有更多内容，引导点进正文。

配色（黄 `(255, 214, 51)`）取自画面里桨板的颜色。skill 里应该写成「从主体物取一个高饱和色作为强调色」，而不是固定黄色。

## 这次踩到的两个坑

**标题压住了下排图**。B 版第一次把 scrim 固定在画布底部、高度 560，结果三张小图几乎全被盖住。解法是给 `decorate()` 加 `bottom` 参数，把整个文字层锚定到主图底边而不是画布底边。写 skill 时这条要写成硬规则：文字层的基线必须是「它所属的那块图的底边」。

**裁切没考虑人脸位置**。默认居中裁的第一版，A 版下排两张脸差点进入渐变区。加 `bias` 之后解决。

## 落盘路径的约束

仓库 `.gitignore` 忽略 `outputs/approved/*`，只对 `outputs/approved/series/**/*.png` 开了白名单。所以封面必须存进系列文件夹（`cover_a_grid.png`、`cover_b_hero.png`），放在 `outputs/approved/` 根目录会被忽略、推不上去。skill 里要写死这个路径规则，并说明原因，避免以后又踩。

## 建议的 skill 参数面

如果要抽成可复用的 skill，我会把这些暴露成配置，其余全部内置：

| 参数 | 说明 |
|------|------|
| `frames` | 有序图片路径，数量决定可用布局 |
| `layout` | `grid_2x2` / `hero_3` / 后续扩展 |
| `title` / `subtitle` / `badge` | 文案，标题建议 ≤10 字 |
| `accent` | 强调色，从画面主体取 |
| `crop_bias` | 每块图的纵向裁切偏移，人像默认 0.32 |
| `out_dir` | 固定为系列文件夹 |

另外两条流程规则值得写进 skill：布局要同时出 A、B 两版让用户挑；封面标题和 `xiaohongshu-caption` 的正文标题应该是**两套文案**——封面标题追求短和钩子，正文标题可以更完整，两者重复会浪费一次曝光。

需要的话我可以直接把这套写成 `.cursor/skills/cover-collage/SKILL.md`，并把 `make_cover.py` 改成读参数的通用脚本。