---
name: wallpaper
description: >-
  Wallpaper pipeline that locks the person as a cutout asset, reconstructs a
  simplified background, composites scale and position with a script, then
  lightly fuses lighting and adapts the master to iPhone, iPad, and desktop.
  Use when the user says 壁纸, wallpaper, /wallpaper, iPhone壁纸, iPad壁纸,
  桌面壁纸, or asks for a phone/tablet/desktop wallpaper set. Do not use for
  Tagame anime dialogue, Xiaohongshu 3:4 posts, or pose series.
---

# Wallpaper

人物是原图像素，背景可以重做，构图是参数。人物用蒙版抠出后只贴上去，不再重画。

提示词：`prompts.md`。构图：`scripts/make_wallpaper.py compose`。

## Route

**In:** 上传了一张照片，并说 壁纸 / wallpaper / /wallpaper / iPhone壁纸 / iPad壁纸 / 桌面壁纸。

**Out:**

- @Tagame / 动漫画风、要台词或 10 秒视频 → `tagame-anime`
- 小红书 3:4、换脸、换姿态、拼接封面 → 对应的 Teo/Kai skill
- 没有照片 → 停下，只要一张照片

点了 `@Teo` 或 `@Kai` 时，只在抠主体那一步追加 `face_01.jpeg`。没点名就不要套这两张脸。画面是动漫就保持动漫，是照片就保持照片。

不要走 `scene-customizer`。不要等用户确认。不要把原图整张 img2img 成壁纸。

## Hard rules

1. **人物是原图像素。** 用蒙版从原图抠出。禁止用 GenerateImage 重画人物。背景和三端都贴这张蒙版。
2. **背景单独生成。** 保留原图的环境语义（通勤地铁、京都、海边、咖啡厅），删掉广告、字、logo、路人、杂物。人物将来所在的区域更简单，四周可以稍丰富。
3. **构图是参数。** `scale` / `x` / `y` / `safe_top` / `safe_bottom` 写进 spec，由 `compose` 执行。不要让生图模型决定人物大小和位置。
4. **融合只接光。** 接触阴影、环境色可以加。人物像素的身份不能改。
5. 手里的东西跟人物同一层。座上的包、脚边的物件若要留下，单独做 Layer 2；否则删掉。
6. 每张生图最多重试 **1** 次。主体或融合仍失败就停，放进 `outputs/rejected/wallpaper/<task_id>/`。某一端失败不影响已经通过的其他端。
7. 人物身上的曝光跟原图。不要提亮、HDR、磨皮。见 `docs/light.md`。
8. 成品不能有字、logo、机框、时钟、小组件、第二个人。
9. `GenerateImage` 只有 `1:1` `4:3` `3:4` `16:9` `9:16`。Master 用 `3:4`（方案里的 4:5）。iPhone 用 `9:16`（方案里的 9:19.5）。

## Pipeline

```
照片
 → 读图。若是设备截图，先 crop
 → 写 spec.json（此步不生图）
 → 抠主体（+ 可选的分离物件）
 → 单独生成简化背景
 → compose（不生图，这张就是 Master）
 → 读图 QA
 → 同一张蒙版贴到 iPhone / iPad / Desktop
 → 交付
```

目录：`outputs/drafts/wallpaper_<task_id>/`。通过后复制到 `outputs/approved/wallpaper/<task_id>/`。

### 1. 读图，必要时裁机框

有手机外框、锁屏时钟、小组件时：

```bash
python3 scripts/make_wallpaper.py crop \
  --src <upload> --box left,top,right,bottom \
  --out outputs/drafts/wallpaper_<task_id>/source.png
```

没有机框就用原图，记为 `source`。

### 2. 写 spec

`outputs/drafts/wallpaper_<task_id>/spec.json`。此步不要调用 GenerateImage。

```json
{
  "medium": "photo",
  "subject_parts": ["entire seated person", "open book in the hands"],
  "detached": [],
  "remove": ["subway interior", "ads", "signs", "other passengers"],
  "environment": {
    "concept": "quiet morning commute on a modern subway",
    "keep": ["modern carriage", "muted red seats", "dark windows", "soft panels"],
    "palette": "warm gray, muted navy, dark red, soft beige",
    "lighting": "soft morning light from the windows, same exposure as the person"
  },
  "key": "247,247,245",
  "compose": {
    "scale": 0.82,
    "x": 0.50,
    "y": 0.61,
    "safe_top": 0.24,
    "safe_bottom": 0.08
  }
}
```

`medium` 只填 `photo` 或 `anime`。`concept` / `keep` / `palette` / `lighting` 从这张原图来，不要套地铁例句。

构图起点用上面的 `compose`。全身、坐下时不要再把人放大；半身可以保持 0.82。人朝一侧看时，把 `x` 往反方向挪一点，给视线留空。数字先写进 spec，再交给脚本。

衣服接近 `247,247,245` 时，把 `key` 改成 `0,177,64`，抠图提示词用同一颜色。

`detached` 只放和身体分开、且要留在壁纸里的物件。空数组就不要做 Layer 2。

### 3. 抠主体

不要调用 GenerateImage。用 u2net 从 `source` 出一张带 alpha 的蒙版，存成 `subject.png`。像素必须是原图，不是重画。

模型在 `~/.u2net/u2net.onnx`。输入缩到 320，再把蒙版放回原图尺寸。alpha 低于 36 的残影去掉。西装和鞋这类主体颜色，alpha 已经起来的就设成不透明。和身体分开的包若是半透明残影，从蒙版里去掉，不要留鬼影。

Read `subject.png` 叠在中性灰底上。脸、头发、手、书、两条腿、两只鞋都要在，边缘不能吃进大块车厢。失败就收紧阈值再出一次蒙版，仍然不要生图。

### 4. 简化背景

`aspect_ratio`: `3:4`。`reference_image_paths`: `[source]`。提示词用 Background。

不要把脸图或主体图传给这一步。画面里不能有人、手、衣服、书、包。

存成 `background.png`。Read：没有人，没有字；主体将来所在的中下部更干净，远处可以保留环境。失败只重做这一张一次。

### 5. 构图

不要在这一步调用 GenerateImage。

```bash
python3 scripts/make_wallpaper.py compose \
  --subject outputs/drafts/wallpaper_<task_id>/subject.png \
  --background outputs/drafts/wallpaper_<task_id>/background.png \
  --out outputs/drafts/wallpaper_<task_id>/composite.png \
  --scale 0.82 --x 0.50 --y 0.61 \
  --safe-top 0.24 --safe-bottom 0.08
```

有 Layer 2 时追加 `--prop .../prop.png --prop-scale 0.18 --prop-x 0.18 --prop-y 0.88`。数字以 spec 为准。

脚本从边缘去掉 key，按中心点粘贴，不放大主体。人会闯入留白时，脚本会把人缩小并下移。stdout 里的 `scale=` 就是实际占比。

### 6. 成图

`compose` 的输出就是 `master.png`。不要再调用 GenerateImage 做融合，融合会把人物重画掉。

Read 成图。人物必须还能对上原图的脸、手、书和鞋子。座位上可以没有接触阴影。半透明包、大块绿边、缺一条腿，都算失败：改蒙版后再 `compose` 一次。仍失败则停止。

### 7. 三端

不要生图。把背景板向上或向两侧延伸，再用同一张 `subject.png` 各 `compose` 一次。延伸处用边缘条带叠化，不要镜像整张图。

| 文件 | 画幅 | 留白 |
|------|------|------|
| `iphone.png` | `9:16` | 头顶以上约 25–30% 只有车厢，留给锁屏时间 |
| `ipad.png` | `4:3` | 向两侧补车厢，人完整 |
| `desktop.png` | `16:9` | 向两侧补车厢，人在中下部 |

手机顶上没有留白，或人被放大超过蒙版原像素，就只改这一张的 `compose` 参数再贴一次。

### 8. 交付

把 `master.png`、`iphone.png`、`ipad.png`、`desktop.png`、`spec.json` 放进 `outputs/approved/wallpaper/<task_id>/`。

回复这四张路径。说明人物来自抠图，位置来自 `compose` 的 scale / x / y，三端是在 Master 上扩展的环境。
