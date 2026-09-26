---
name: wallpaper-demo
description: >-
  Photorealistic iPhone lock-screen showcase from an existing still. The phone
  is a product shot; the screen wallpaper is the reference image. Brand lines
  汉克壁纸 and MR.HUNK WALLPAPER are omitted unless the user supplies them.
  Use when the user asks for 壁纸演示图, 锁屏展示, 锁屏效果图, 手机锁屏壁纸展示,
  lock screen mockup, or wallpaper demo. The cutout wallpaper skill is removed.
---

# Wallpaper Demo — 手机锁屏展示图

把一张已有成图做成 **iPhone 锁屏产品展示图**：浅灰棚拍、深色 iPhone 15 Pro、屏幕里是原图、iOS 锁屏界面叠在上面。

**不要等待。** 不走换装确认。一次 `GenerateImage`。

| 给了什么 | 手机下方 |
|----------|----------|
| 没给品牌 | **不写任何字**。不要出现 `汉克壁纸`，不要出现 `MR.HUNK WALLPAPER`，不要出现 `4K高清壁纸` |
| 给了中文品牌 | 左侧写用户给的中文，原文 |
| 给了英文品牌 | 中间写用户给的英文，原文 |
| 给了角标（或说要 4K 角标） | 右侧黑色小牌，白字。没给文案时用 `4K高清壁纸` |

只写用户给过的那几项。缺的位置留空，**禁止用示例品牌补上**。

---

## Route in / out

**In:** 指着一张成图，要 壁纸演示图 / 锁屏展示 / 锁屏效果图 / 手机锁屏壁纸展示 / lock screen mockup / wallpaper demo。

**Out:**

- 换脸 → `virtual-couple`
- Tagame 静帧 / 视频词 → `tagame-anime`

---

## Hard rules

1. `reference_image_paths` 只放用户给的那张壁纸原图。屏幕壁纸必须是这张图的再现：脸、发型、胡须、衣服或裸露、姿势、场景、光线都跟原图走。不要加原图没有的帽子或衣服。
2. 手机、背景、锁屏图标是写实产品摄影。屏幕里的画保持原图风格（动漫仍是动漫）。
3. 画幅 `3:4`。时间与小组件放在画面上沿，脸完整露在时间下方，不要被 `9:41` 挡住。
4. 品牌默认不写。见上表。
5. 落盘：`outputs/approved/<源文件名>_lockscreen_demo.png`。

锁屏数字用下面的默认值。用户改了时间、天气或城市，只改他们点名的那几项。

---

## Generate

先读原图，用画面里真实的人物和场景替换提示词里的壁纸描述，再调用 `GenerateImage`。

默认提示词（无品牌。用户给了品牌才把文末那一段加回去）：

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
