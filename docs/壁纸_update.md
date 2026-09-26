对，这张图和上一张不一样。**这张最适合的不是“整图重新生成”，而是「主体分离 → 背景重构 → 构图合成 → 对齐适配」**。

因为原图本身的人物已经很好，尤其是：

* 西装男的脸、发型、体型
* 看书的姿势
* 双手和书
* 地铁座椅的坐姿

这些都应该尽量 **100% 保留**。如果直接 img2img，很容易把人物重新画一遍，导致脸、手、衣服发生变化。

我建议你的 Workflow 改成下面这样：

```text
原始图片
   │
   ▼
① Subject Extraction
   │
   ├── 人物
   ├── 书
   └── 可选：公文包
   │
   ▼
② Background Reconstruction
   │
   └── 地铁 → 简化、虚化、设计化背景
   │
   ▼
③ Composition / Alignment
   │
   ├── 调人物大小
   ├── 调人物位置
   ├── 调底部/顶部留白
   └── 光影统一
   │
   ▼
④ Wallpaper Adaptation
   │
   ├── iPhone
   ├── iPad
   └── Desktop
   │
   ▼
⑤ Vision QA
```

这里最关键的是：**人物和背景分开生成。**

---

# 1. 第一步：把人物真正“抠出来”

对于这张图，我甚至不建议让 LLM 直接生成一个“人物参考图”。

最好是：

> **原图 → segmentation / mask → RGBA transparent subject**

也就是得到：

```text
       原图
        ↓
┌────────────────┐
│                │
│    👨‍💼        │
│   📖           │
│               │
│               │
└────────────────┘

        ↓

透明 PNG

        👨‍💼
       📖
```

### 抠图 Prompt

如果你的图像模型支持 mask / background removal，可以用：

```text
Extract the complete main subject from the reference image.

Preserve the subject exactly as shown.

The subject includes:
- the entire seated man
- his head and hair
- face
- navy blue business suit
- white shirt
- dark tie
- both arms and hands
- the open book he is holding
- his legs
- black dress shoes

Preserve the original:
- facial features
- hairstyle
- body proportions
- clothing
- pose
- hand positions
- book position
- perspective

Do not redraw or redesign the subject.

Do not change the face.
Do not change the hairstyle.
Do not change the clothing.
Do not change the pose.
Do not change the body proportions.

Remove the entire background.

Remove:
- subway interior
- seats
- poles
- windows
- floor
- advertisements
- signs
- environmental objects

Output the subject on a completely transparent background.

The extracted subject should retain clean edges and natural hair details.
```

### 一个重要细节

我会把：

> **人物 + 书**

视为一个整体 Subject。

而：

> 公文包

我会做成第二个 Layer。

也就是：

```text
Layer 1
人物 + 书

Layer 2
公文包

Layer 3
背景
```

这样后面你可以自由决定：

```text
人物 + 书
       ↓
放在画面中间

公文包
       ↓
放左下角
```

---

# 2. 第二步：不要“生成一个新背景”，而是做 Background Reconstruction

这一步是你这个 Workflow 最有价值的地方。

原图：

> 真实地铁

但是壁纸不需要这么多信息。

你真正想保留的是：

> **“通勤 / 地铁 / 都市白领”这个语义**

而不是：

> 每一根扶手、每一个广告牌、每一扇窗户。

所以背景应该从：

```text
真实地铁
```

变成：

```text
简化后的都市地铁空间
```

---

## Background Prompt

把**抠出来的人物作为参考，但要求背景生成模型不要重新生成人物**：

```text
Create a minimalist editorial background for a premium vertical wallpaper.

The visual concept is:
"quiet morning commute on a modern subway".

Use the original image only as environmental reference.

DO NOT generate any person.
DO NOT generate any human figure.
DO NOT generate hands.
DO NOT generate clothing.
DO NOT generate a book.
DO NOT generate a bag.

The background should contain only the subway environment.

Simplify the original subway interior into a clean, aesthetically designed environment.

Preserve the visual language of:
- modern subway carriage
- muted red seats
- metallic poles
- large dark windows
- soft neutral interior panels
- subtle reflections
- realistic subway architecture

However, remove unnecessary visual clutter:
- advertisements
- signs
- text
- logos
- passengers
- excessive details
- distracting objects

Create strong visual hierarchy.

The area behind the future subject should be relatively simple and slightly darker,
so the subject can clearly separate from the background.

Use subtle depth of field:
foreground and distant subway elements slightly blurred,
while maintaining enough architectural detail to establish the subway environment.

Color palette:
warm gray
muted navy
dark red
soft beige
subtle metallic tones

Lighting:
soft morning light entering through the subway windows,
gentle directional light,
subtle ambient reflections.

Style:
premium editorial illustration,
cinematic,
clean,
minimalist,
high-end wallpaper design.

No text.
No people.
No logos.
No UI.

Vertical wallpaper composition.
Leave clean negative space around the central subject area.
```

---

# 3. 这里还有一个更重要的技巧：背景应该主动“让位”

你的最终画面不是：

> 一个很漂亮的地铁背景 + 一个人

而应该是：

> **一个人是视觉第一层，地铁是第二层。**

所以我建议你的 Background Agent 有一个固定规则：

```text
Background Complexity
        ↓
subject area      low
outer area        medium
far background    medium-high
```

也就是人物背后不要太复杂。

例如：

```text
┌────────────────────────┐
│                        │
│       简单背景          │
│                        │
│        👨‍💼             │
│       📖               │
│                        │
│  复杂一点       简单    │
└────────────────────────┘
```

这样壁纸会比“完整复刻地铁”高级很多。

---

# 4. 第三步才是你说的「对齐」

这一步我建议**不要交给生成模型决定**。

如果你自己做 Agent，我甚至会把它定义成一个 deterministic tool：

```text
compose_wallpaper(
    subject,
    background,
    canvas,
    subject_scale,
    subject_x,
    subject_y
)
```

例如 iPhone：

```yaml
canvas:
  width: 1290
  height: 2796

subject:
  scale: 0.82
  x: 0.53
  y: 0.61

safe_area:
  top: 0.24
  bottom: 0.08
```

这样人物位置是**可控的**。

---

# 5. 对这张图，我会怎么排

我不会把人物放得特别大。

原图人物本身占画面非常高，如果直接变成手机壁纸，会出现：

```text
┌───────────────┐
│       👤      │
│      👤👤     │
│     👤👤👤    │
│     👤👤👤    │
│      👤       │
│      👤       │
│      👤       │
│               │
└───────────────┘
```

锁屏时间一放上去就会非常挤。

我更推荐：

```text
┌─────────────────┐
│                 │
│    Subway      │
│                 │
│                 │
│       👤        │
│      👤👤       │
│     👤📖👤      │
│      👤👤       │
│     👤  👤      │
│                 │
│   🚩            │
└─────────────────┘
```

即：

**上面留白 + 人物下沉 + 地铁环境作为氛围。**

---

# 6. 合成后的 Image-to-Image Prompt

把：

> 人物透明层 + 背景

交给最终生成模型做一次轻度融合。

Prompt：

```text
Combine the provided foreground subject and background into a single premium wallpaper.

IMPORTANT:
The foreground subject is already finalized.

Preserve the foreground subject exactly.

Do NOT regenerate the person's face.
Do NOT change the hairstyle.
Do NOT change the body proportions.
Do NOT change the suit.
Do NOT change the hands.
Do NOT change the book.
Do NOT change the pose.

Only integrate the subject naturally into the environment.

COMPOSITION:

Vertical smartphone wallpaper.

Place the subject slightly below the vertical center.

Scale the subject so that the entire head, torso, arms, book, legs and shoes remain visible.

Leave approximately 25% clean visual space above the subject.

The subject should be the primary visual focus.

The subway background should remain secondary.

BACKGROUND:

Simplified modern subway carriage.
Muted red seats.
Metallic poles.
Dark windows.
Soft morning light.

Reduce background detail behind the subject.

Use subtle depth of field to separate the subject from the environment.

LIGHTING:

Match the lighting direction between subject and background.

Add subtle ambient light from the subway environment onto the suit.

Add a very soft contact shadow around the seat and lower body.

Do not change the subject itself.

STYLE:

Premium editorial wallpaper.
Cinematic anime illustration.
Sophisticated.
Minimalist.
High detail.
Clean composition.

NO:
text
logos
watermarks
UI
phone frame
clock
widgets
additional people
additional characters
```

---

# 7. 然后再做「手机壁纸适配」

这里我建议你**不要重新生成整张图**。

而是：

```text
Master Wallpaper
        ↓
   Resize / Crop
        ↓
    Outpaint
        ↓
     Phone
```

比如 Master：

```text
4:5
```

然后：

```text
4:5
 ↓
9:19.5
```

上下扩展背景。

人物尽量不要重新生成。

Prompt：

```text
Convert the existing artwork into a 9:19.5 smartphone wallpaper.

IMPORTANT:
Preserve the existing subject exactly.

Do not regenerate the person.

Do not modify:
- face
- hair
- suit
- hands
- book
- pose
- body proportions

Extend the subway environment naturally above and below the existing artwork.

Move the complete composition slightly downward if necessary.

Create approximately 25–30% clean negative space in the upper portion.

The upper area should contain only simplified subway background.

Do not place important visual information near the top.

This area is reserved for smartphone lock-screen time and widgets.

Maintain the same:
- lighting
- color palette
- perspective
- illustration style
- visual atmosphere

No text.
No UI.
No clock.
No device frame.
```

---

# 8. 最终我会把你的 Agent 做成这个结构

这其实比我上一条给你的 Workflow 更适合你这个项目：

```text
                  ┌──────────────┐
                  │  Original    │
                  │    Image     │
                  └──────┬───────┘
                         │
             ┌───────────┴───────────┐
             ↓                       ↓
      ┌──────────────┐       ┌──────────────┐
      │   Subject    │       │  Background  │
      │  Extraction  │       │ Reconstruction│
      └──────┬───────┘       └──────┬───────┘
             │                       │
             │                       │
             └───────────┬───────────┘
                         ↓
                  ┌──────────────┐
                  │   Composer   │
                  │              │
                  │ scale        │
                  │ position     │
                  │ alignment    │
                  │ lighting     │
                  └──────┬───────┘
                         ↓
                  Master Wallpaper
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
            Phone       iPad      Desktop
              │          │          │
              └──────────┼──────────┘
                         ↓
                    Vision QA
                         │
                    ┌────┴────┐
                    ↓         ↓
                  PASS      FAIL
                    │         │
                    ↓         └──→ regenerate
                  Export
```

## 最关键的设计原则

你的这个场景，我建议牢牢记住四句话：

**① 人物是 Asset，不是 Prompt。**
人物尽量通过抠图/参考图锁住，不要每一轮重新生成。

**② 背景是可生成的 Context。**
地铁、京都、海边、咖啡厅这些环境都可以重新生成。

**③ 构图是参数，不应该完全交给 LLM。**
`scale / x / y / safe_area / aspect_ratio` 最好由 Composer 控制。

**④ 最终生成模型只负责“融合”，不要负责“重新创作人物”。**

这样你这个东西就不再是简单的：

> **AI 生壁纸**

而更像一个真正可批量运行的：

> **Image → Subject Asset → Environment → Composition → Multi-device Wallpaper**

这套架构也特别适合你后面做成 Cursor Skill：**用户丢一张图进去，Skill 自动判断主体、抠主体、简化背景、构图、输出 3 个设备版本。**
