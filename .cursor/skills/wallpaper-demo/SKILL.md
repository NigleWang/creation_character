---
name: wallpaper-demo
description: >-
  Device wallpaper showcases from an existing still. iPhone is a lock-screen
  product shot of the still as-is. Computer and iPad first expand that portrait
  still into a 16:9 or 4:3 wallpaper, then a product shot of a MacBook or iPad
  whose screen shows that wallpaper. Brand lines 汉克壁纸 and MR.HUNK WALLPAPER
  are omitted unless the user supplies them. Use when the user asks for
  壁纸演示图, 锁屏展示, 锁屏效果图, 手机锁屏壁纸展示, 电脑壁纸, 电脑演示,
  iPad壁纸, iPad演示, lock screen mockup, or wallpaper demo. The cutout
  wallpaper skill is removed.
---

# Wallpaper Demo — 设备壁纸展示

指着一张已有成图，做成设备展示图。**不要等待。** 不走换装确认。

| 用户要 | 做什么 |
|--------|--------|
| 手机 / 锁屏 / 没点设备 | 原图直接做 iPhone 锁屏。一次 `GenerateImage`，`3:4` |
| 电脑 | 先扩成 `16:9` 壁纸，再做 MacBook 展示图 |
| iPad | 先扩成 `4:3` 壁纸，再做 iPad 展示图 |
| 电脑和 iPad | 上面两套都做 |

竖图（9:16 或 3:4）不能裁切或拉伸去填横屏。电脑和 iPad 必须先扩背景，再拿扩好的图做屏幕。

| 给了什么 | 设备外 |
|----------|--------|
| 没给品牌 | **不写任何字**。不要出现 `汉克壁纸`，不要出现 `MR.HUNK WALLPAPER`，不要出现 `4K高清壁纸` |
| 给了中文品牌 | 左侧写用户给的中文，原文 |
| 给了英文品牌 | 中间写用户给的英文，原文 |
| 给了角标（或说要 4K 角标） | 右侧黑色小牌，白字。没给文案时用 `4K高清壁纸` |

只写用户给过的那几项。缺的位置留空，**禁止用示例品牌补上**。

---

## Route in / out

**In:** 指着一张成图，要 壁纸演示图 / 锁屏展示 / 锁屏效果图 / 手机锁屏壁纸展示 / 电脑壁纸 / 电脑演示 / iPad壁纸 / iPad演示 / lock screen mockup / wallpaper demo。

**Out:**

- 换脸 → `virtual-couple`
- Tagame 静帧 / 视频词 → `tagame-anime`

---

## Shared rules

1. 先读原图。提示词里的人物、衣服或裸露、姿势、场景，按这张图写。不要加原图没有的帽子或衣服。
2. 设备、棚拍背景、系统界面是写实产品摄影。屏幕里的画保持原图风格（动漫仍是动漫）。不要把动漫改成照片，也不要加亮。
3. 品牌默认不写。见上表。三端都适用：字写在设备外面的浅灰底上。
4. 落盘到 `outputs/approved/`，文件名用源文件名：

| 产物 | 文件 |
|------|------|
| iPhone 展示 | `<源文件名>_lockscreen_demo.png` |
| 电脑壁纸 | `<源文件名>_desktop_wallpaper.png` |
| 电脑展示 | `<源文件名>_desktop_demo.png` |
| iPad 壁纸 | `<源文件名>_ipad_wallpaper.png` |
| iPad 展示 | `<源文件名>_ipad_demo.png` |

---

## iPhone

`reference_image_paths` 只放用户给的那张原图。画幅 `3:4`。时间与小组件放在画面上沿，脸完整露在时间下方，不要被 `9:41` 挡住。

锁屏数字用下面的默认值。用户改了时间、天气或城市，只改他们点名的那几项。

```text
A high-resolution, photorealistic render of a centered, dark-colored iPhone 15 Pro with Dynamic Island against a clean, neutral light-grey studio background. Soft even studio light, subtle contact shadow, no clutter. The phone screen is active and displays a precise, fully detailed iOS lock screen. The wallpaper filling the screen is an exact reproduction of the reference image: [read the still and describe the actual person, pose, clothing or lack of it, and environment. Do not invent a cap or outfit].

The iOS lock screen interface is overlaid perfectly:
- Dynamic Island at the top center.
- Top status bar: left text exactly "Mon 10 🗽 NYC 12:41 AM"; right side cellular, Wi-Fi, and battery icons.
- Large bold white time "9:41" in the upper third, clear of the face. The face stays fully visible below the time.
- Widgets under the time: left "72°, Partly Cloudy, H:88° L:64°"; center circular "67 (50 78)"; right circular "8:29 PM".
- Bottom left camera icon, bottom right flashlight icon, home indicator bar at the bottom center.

No text, logo, or badge anywhere outside the phone. The area below the phone is empty light grey.
```

用户给了品牌时，删掉最后一句，改成只包含他们给的项：

```text
Below the phone, on the light-grey background, only these branding elements, nothing else:
- far left, black Chinese text: [用户给的中文，例如 汉克壁纸]
- center, black uppercase Latin text: [用户给的英文，例如 MR.HUNK WALLPAPER]
- far right, a small black rectangular badge with white text: [用户给的角标，或 4K高清壁纸]
```

没给的那一行不要写进提示词。

---

## Computer and iPad — expand, then demo

顺序固定。先出壁纸，读过壁纸，再用那张壁纸做展示图的唯一参考。展示图不要再用竖图原件，否则屏幕会回到 9:16。

### 1. 电脑壁纸 `16:9`

`reference_image_paths` = 竖图原件。

人物放在画面中右，比例和姿势跟原图一致，脸和身体不要裁掉。**左侧**用同一场景无缝补齐：同样的光线、颜色、纹理。左侧留出能放桌面图标的空位。不要新加人物。

```text
A high-resolution 16:9 horizontal image in the same style as the reference (if the reference is anime, stay anime; do not make it photorealistic). Perfectly preserve the person from the reference: [face, hair, beard, clothing or lack of it, pose, and the objects they are holding]. Same exposure. Place them in the center-right of the wide frame, fully visible, not cropped. Seamlessly extend the existing environment to the LEFT to fill the canvas: [the actual background — wall, room, forest, water — in the same lighting and color]. The left side is a clean continuation with open space for desktop icons. Do not add clothes, a cap, glasses, or any new person. Do not brighten the image.
```

落盘 `<源文件名>_desktop_wallpaper.png`。

### 2. iPad 壁纸 `4:3`

`reference_image_paths` = 竖图原件。

人物居中。上下左右都用同一场景补齐，光线不变。可以多露出一点原图裁掉的身体边缘，不要重画一张新姿势。

```text
A high-resolution 4:3 image in the same style as the reference (if the reference is anime, stay anime; do not make it photorealistic). Perfectly preserve the person from the reference: [face, hair, beard, clothing or lack of it, pose, and the objects they are holding]. Same exposure. They are centered in the 4:3 frame. Extend the existing environment seamlessly in all directions: [the actual background]. A little more of the body or setting may show at the edges. The person remains the central focus. Do not add clothes, a cap, glasses, or any new person. Do not brighten the image.
```

落盘 `<源文件名>_ipad_wallpaper.png`。

### 3. 电脑展示图 `16:9`

先读电脑壁纸。`reference_image_paths` 只放这张 `16:9` 壁纸。

浅灰棚拍、打开的深色 MacBook Pro、屏幕是这张壁纸。菜单栏只用英文，避免乱码。文件夹不要字。脸不要被图标挡住。

```text
A high-resolution photorealistic product photograph of a centered space-black MacBook Pro, open and facing the camera, on a clean neutral light-grey studio background. Soft even studio light, subtle contact shadow, no clutter, no people. The laptop screen shows a macOS desktop. The wallpaper filling the screen is an exact reproduction of the reference image: [describe the 16:9 wallpaper]. The person sits on the right side of the screen. The menu bar uses only these exact English words, left to right: a small Apple logo, then Finder, File, Edit, View, Go, Window, Help. Three plain yellow folder icons stacked on the far left over the empty background, with no text labels, not covering the face. A slim dock of colorful app icons along the bottom, no text. The words MacBook Pro may appear in small grey letters on the bottom bezel. No other text, logo, or badge anywhere outside the laptop. The light-grey area around the laptop is empty. No Chinese characters anywhere.
```

落盘 `<源文件名>_desktop_demo.png`。

### 4. iPad 展示图 `4:3`

先读 iPad 壁纸。`reference_image_paths` 只放这张 `4:3` 壁纸。

浅灰棚拍、横屏银色 iPad Pro。时间放在左侧背景上，脸保持完整。

```text
A high-resolution photorealistic product photograph of a centered silver iPad Pro in landscape orientation, thin black bezel, on a clean neutral light-grey studio background. Soft even studio light, subtle contact shadow, no clutter, no people. The screen displays an iPadOS lock screen. The wallpaper filling the screen is an exact reproduction of the reference image: [describe the 4:3 wallpaper]. Large white time "9:41" on the left third of the screen over the background, with smaller white date "Monday, September 10" above it. The face stays fully visible and is not covered by the time. No widgets over the face. No text, logo, or badge anywhere outside the iPad. The light-grey area around the iPad is empty.
```

落盘 `<源文件名>_ipad_demo.png`。

电脑或 iPad 给了品牌时，删掉「设备外空白」那句，改成和 iPhone 相同的品牌句，把 `phone` 换成 `laptop` 或 `iPad`。没给的那一行不要写。

---

## 显示到客户端（远程 Cloud）

远程 Cloud 不会把 `GenerateImage` 的工具卡片贴进对话。每张已落盘的 PNG，在最终回复里用**绝对路径**再嵌一行，客户端才会显示。一张图一行，不要只写路径文字。

```markdown
![电脑壁纸](/absolute/path/to/<源文件名>_desktop_wallpaper.png)
```

同时把同一份文件复制到仓库 `artifacts/` 下（同名），供 Cloud artifacts 接口拉取。`artifacts/` 不提交。
