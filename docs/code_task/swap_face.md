这个方向**非常适合做成一套“Character-driven Content Pipeline（角色驱动内容生产流水线）”**。

你的核心目标其实不是“写几个生成图片的 Prompt”，而是搭建一个：

> **两个固定虚拟角色 → 输入任意 Scene Reference → 自动理解场景 → 保持角色一致性 → 生成符合小红书内容类型的图片**

我建议你不要把它设计成一个单一的 Image Generation Skill，而是设计成一个 **Content Production Agent + 多个 Skills**。

---

# 一、先定义整体架构

我建议你的 Cursor 项目最终长这样：

```text
Xiaohongshu Virtual Couple Studio
│
├── Character System
│   ├── Character A Bible
│   ├── Character B Bible
│   ├── Relationship Bible
│   └── Character Consistency Rules
│
├── Scene System
│   ├── Scene Analyzer
│   ├── Composition Extractor
│   ├── Pose Extractor
│   └── Style Extractor
│
├── Generation System
│   ├── Character Composer
│   ├── Prompt Builder
│   ├── Image Generator
│   └── Quality Controller
│
├── Content System
│   ├── Wallpaper Skill
│   ├── Couple Daily Skill
│   ├── Single Daily Skill
│   └── Xiaohongshu Post Skill
│
└── Workflow Orchestrator
```

最终你在 Cursor 里面的使用方式应该非常简单：

```text
@virtual-couple

角色：
- A
- B

内容类型：
- 情侣日常

Scene：
[上传参考图片]

要求：
- 保持Scene的构图
- 保持人物动作
- 替换成角色A和B
- 小红书竖屏
```

然后整个 Pipeline 自动执行。

---

# 二、最重要的核心思想：把“角色”和“场景”解耦

这是整个系统最关键的设计。

不要直接这样：

```text
Character Prompt
+
Scene Image
↓
Image Generation
```

因为这样非常容易出现：

* 角色脸变了
* 发型变了
* 衣服不符合设定
* Scene 动作丢失
* 两个人的位置关系改变
* AI 自动换姿势
* 参考图质感消失

应该拆成：

```text
                 Character Bible
                       │
                       ▼
               Character Identity
                       │
                       │
Scene Image ──► Scene Understanding
                       │
                       ▼
                 Scene Blueprint
                       │
                       ▼
              Character + Scene Fusion
                       │
                       ▼
                 Generation Prompt
                       │
                       ▼
                   Final Image
```

也就是说：

> **Character Bible 决定“谁”**
>
> **Scene Reference 决定“在哪里、做什么、怎么构图”**
>
> **Content Skill 决定“最后做成什么内容”**

---

# 三、建议设计 6 个核心 Skills

---

# Skill 1：Character Registry

这是你的角色数据库。

目录：

```text
characters/
├── character_A/
│   ├── bible.md
│   ├── appearance.json
│   ├── personality.md
│   ├── reference/
│   │   ├── face_01.png
│   │   ├── face_02.png
│   │   └── fullbody.png
│
└── character_B/
    ├── bible.md
    ├── appearance.json
    ├── personality.md
    └── reference/
```

---

## Character Bible 不要只写 Prompt

建议结构化。

### character_A.yaml

```yaml
id: character_A

identity:
  gender: male
  age_appearance: 25

face:
  shape: oval
  eyes: narrow
  nose: straight
  skin: fair

hair:
  color: black
  style: medium_length
  특징: slightly messy

body:
  height_ratio: tall
  build: slim

personality:
  keywords:
    - calm
    - reserved
    - gentle

visual_signature:
  - slightly lowered gaze
  - subtle smile
  - elegant posture

negative_identity:
  - do not change face shape
  - do not change hairstyle drastically
  - do not change body type
```

Character B 同样。

---

## 再加一个 Relationship Bible

这个非常重要。

```yaml
relationship:

characters:
  - A
  - B

dynamic:
  type: romantic couple

character_A_role:
  keywords:
    - calm
    - protective
    - introverted

character_B_role:
  keywords:
    - warm
    - expressive
    - playful

interaction_patterns:
  - walking together
  - looking at each other
  - sharing food
  - sitting closely
  - quiet domestic moments
  - subtle physical contact

emotion_rules:
  - natural
  - cinematic
  - intimate but restrained
```

这样以后生成情侣内容的时候，Agent 不需要每次重新理解两个人的关系。

---

# 四、Skill 2：Scene Analyzer

这是你整个系统的核心 Skill。

你的输入可能是：

![Image](https://images.openai.com/static-rsc-4/uu7EbL6lYWCw7dbWOhwocvdwFHMhxK0BDTnEWFO1DGivGTTNlf0M5NHOA1JuxwrkWtpt4YEJeX9H3SWuhE7cVi5iZ2Sjc5uT1baTpGXDnzL8HgaT9wf3_IwBueFBPnC3LqM7HL1J_xm3Gj9N8dwHF9Al_1pJcp5DG5t5rGEAlZ8093-qkDnNsoI_EHYoq-t5?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/aZfV50wqVKAvCnbjRlVUZ4ScT6tlx-xKidbkZFXQLctbOCvijFtM0nIzPsbKK0aob3eiSqb2UH__v-YUI2NgXh-iq8VDcNbBtMnveeQsFr1B6hZLHJ-Yc2CfNs8-SQwTHifURELeTiE64Wy0tFHYAxX_ZoMNFAwF9aYSfLnwIAEmuwJeLj9yPjYi4vCgNejb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/f0yJpsvoUH5vlWwy4e2cc-vFGtV0ZaBJB2AVSBa8vJD6jg-jEEiS9t06FbaQyOpcpKWmeMi36JSn-NxK0RbjztFLnAm8-UAVCCRZWY09ZlD7lutUNdHuKoq8x7wYwr_6q-QjDqih2wfVZhAWR0u6vmT0-Lu3uP9fyxMu1VnFbYgBBc3qTRprxQZnMo-yjReX?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/WJ8cGHbno3xlwNi12ZMeo9f2Sjqt1tA_8uVSlcrOoMh_zUnXg2tio1uRZUP8WVpG7GWy3Ns5QIKJNSvhsEza21ecQNKDEhJJx8Qmj-sgSR_YhyDk_p_seKK7-D66WuQjXl5Pw8UgXJXnJSqZZCNW4sn_zdGSbO6nDzKyiBhCbGN79P0qckBxRDedfEgd0oKW?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/8u-fkKYopQFNR9x2AIOyvDvpqAW8T2InbRMkkb-UvVXg1VFqPrMAOPn9ldNMEsvfw21_i4LYsZtb28-zftT9I3Nu8j1m602qkhNM84f2fDFBpP3CeVtUBCaQ68d89q3yx81wKqanJY5M3jIz4bBczr7rDzmnw0EA7pEAyZURPiQYQemrAaoMEPbleHvT0pEB?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/eFE7CqUnhAf7p0ujNtIV2KMZGxQvItZFNlhnqA7EiRiL8WpsN-tg3pdoZM3KzWpXFov73EBe2DxxsGLPaRTiUcJSCsUxERmg_GygifY-9EmzQmXjJJkK33vrdiCNB-9z3_7drkesgQ1rz2-e-JaCDv8Wd04Pqmioo7lVG47PWJBR9M-PDmo2PouEc_b1euz7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/47CrzEbNHaaBqblpQMHa67MOIv3sm66Tu_gPb-RZO1z-FQxpfzeQiF3FmL0EuFwIgSLje4yYW9uI3p97WytSf5U5Sk6evLYV4B31Fj8bNInk9NZkV7iFe7-RLeoo8Y1m-XGmfVLR5YlfsAYa5_QZtWLcGybkttfcZBXEZOfn0zdWJo4VRKc5VNeHJuV-Vejm?purpose=fullsize)

假设用户上传：

```text
Scene Reference Image
```

Scene Analyzer 不应该直接生成图片。

它首先输出一个：

# Scene Blueprint

例如：

```yaml
scene:

environment:
  location: cafe
  time: afternoon
  lighting: warm sunlight

composition:
  framing: medium shot
  camera_angle: eye level
  aspect_ratio: 3:4

subjects:
  count: 2

positions:

  subject_1:
    position: left
    body_direction: facing right
    posture: sitting

  subject_2:
    position: right
    body_direction: facing left
    posture: sitting

interaction:
  type: eye_contact
  emotional_tone: intimate

pose:
  subject_1:
    left_hand: holding coffee
    gaze: looking at subject_2

  subject_2:
    posture: leaning forward
    gaze: looking at subject_1

visual_style:
  realism: high
  lighting: cinematic
  color_tone: warm
  texture: film photography
```

---

## Scene Analyzer 的 Prompt

你的 Skill 应该要求：

```text
Analyze the reference image.

Your task is NOT to identify the original people.

Extract only:

1. Environment
2. Composition
3. Camera angle
4. Framing
5. Number of people
6. Position of each person
7. Body posture
8. Interaction
9. Hand position
10. Head direction
11. Eye direction
12. Lighting
13. Color palette
14. Visual texture
15. Emotional atmosphere

Return structured JSON.

Preserve the original composition and action logic.
Do not describe the identity of the original people.
```

这样可以实现：

> **Scene 的人是谁不重要，只提取 Scene 的“视觉结构”。**

---

# 五、Skill 3：Character + Scene Composer

这是把两个系统融合。

输入：

```text
Character A
+
Character B
+
Scene Blueprint
```

输出：

```text
Generation Blueprint
```

例如：

```yaml
subjects:

  left_person:
    character: A

    identity:
      use_character_bible: true

    pose:
      inherit_from_scene_subject_1: true

    position:
      left

  right_person:
    character: B

    identity:
      use_character_bible: true

    pose:
      inherit_from_scene_subject_2: true

interaction:
  inherit_scene_interaction: true

environment:
  inherit_scene: true

composition:
  preserve_scene: true
```

这里最关键的一条规则：

```text
Character controls IDENTITY.

Scene controls COMPOSITION and ACTION.

Neither should override the other.
```

也就是：

| 模块              | 决定什么 |
| --------------- | ---- |
| Character Bible | 脸    |
| Character Bible | 身材   |
| Character Bible | 固有发型 |
| Character Bible | 人物气质 |
| Scene           | 动作   |
| Scene           | 构图   |
| Scene           | 镜头   |
| Scene           | 环境   |
| Scene           | 光影   |
| Scene           | 色调   |

---

# 六、Skill 4：Content Type Router

你的最终内容不能全部用同一个 Prompt。

至少应该有三个 Content Skills。

---

## ① Wallpaper Skill

目标：

```text
手机壁纸
电脑壁纸
锁屏壁纸
```

输入：

```yaml
content_type: wallpaper
```

Skill 自动增加：

```yaml
requirements:

aspect_ratio:
  mobile: 9:16

composition:
  leave_negative_space: true

subject_position:
  avoid_center_ui_area: true

visual_priority:
  - aesthetic
  - clean composition
  - high resolution
```

Prompt：

```text
Create a vertical wallpaper composition.

Maintain clear negative space.

Avoid placing important facial details in
areas likely to be covered by mobile UI.

High aesthetic value.
Cinematic photography.
Clean visual hierarchy.
```

---

## ② Couple Daily Skill

这是你最重要的内容来源。

内容类型：

```text
一起吃饭
下班回家
咖啡馆
旅行
雨天
做饭
散步
看电影
超市
海边
生日
圣诞节
睡前聊天
```

Skill：

```yaml
content_type: couple_daily

relationship_priority:
  - interaction
  - chemistry
  - emotion

visual_requirements:
  - natural interaction
  - subtle intimacy
  - believable body language
```

---

## ③ Single Daily Skill

分别生成：

```text
Character A 日常
Character B 日常
```

例如：

```text
早晨起床
上班
健身
咖啡馆
看书
旅行
雨天
夜晚街头
```

这个非常适合小红书的人设运营。

因为你的账号不能只有：

```text
情侣合照
情侣合照
情侣合照
```

应该是：

```text
A的日常
B的日常
情侣日常
壁纸
情侣故事
```

这样用户会逐渐：

> **把他们当成两个“真实存在的虚拟人物”。**

---

# 七、Skill 5：Prompt Builder

建议不要人工维护一个超级 Prompt。

应该：

```text
Character Prompt
+
Scene Blueprint
+
Content Skill
+
Style Constraints
↓
Prompt Builder
```

自动生成。

例如：

```text
[CHARACTER IDENTITY]

Two recurring virtual male characters.

Character A:
{character_A_bible}

Character B:
{character_B_bible}

[SCENE]

A warm afternoon cafe.

[COMPOSITION]

Preserve the reference composition.

Character A sits on the left.
Character B sits on the right.

Medium shot.
Eye-level camera.

[POSE]

Character A holds a coffee cup.

Character B slightly leans forward.

Maintain natural eye contact.

[VISUAL STYLE]

Warm cinematic lighting.
Film photography texture.
Realistic skin texture.

[CONSTRAINTS]

Character identity has higher priority than
the original people in the reference image.

Preserve:

- composition
- body position
- interaction
- camera angle
- lighting logic

Do not change:

- Character A facial identity
- Character B facial identity
```

---

# 八、Skill 6：Quality Controller

生成完不要直接发布。

做一个 AI QC。

输入：

```text
Generated Image
+
Character Reference
+
Scene Reference
```

检查：

### 1️⃣ Character Consistency

```text
A 是不是 A？
B 是不是 B？
```

---

### 2️⃣ Scene Consistency

```text
构图是否保持？

人物位置是否正确？

动作是否接近？

环境是否一致？
```

---

### 3️⃣ Couple Consistency

```text
两个人是否正确？

有没有：

A/B角色交换？
人物多出来？
人物消失？
脸融合？
```

---

### 4️⃣ Social Media Quality

```text
是否适合小红书？

构图是否有吸引力？

人物是否明显？

是否适合封面？
```

输出：

```json
{
  "score": 8.7,

  "character_consistency": 9,
  "scene_consistency": 8,
  "composition": 9,
  "social_quality": 9,

  "issues": [
    "Character B hairstyle slightly inconsistent"
  ],

  "decision": "accept"
}
```

---

# 九、整个 Cursor Skill Workflow

我建议最终设计成：

```text
                USER INPUT
                     │
                     ▼
             Content Router
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
      Wallpaper   Couple      Single
                     │
                     ▼
                Load Characters
                     │
                     ▼
                Scene Analyzer
                     │
                     ▼
                Scene Blueprint
                     │
                     ▼
           Character Scene Composer
                     │
                     ▼
               Prompt Builder
                     │
                     ▼
               Image Generation
                     │
                     ▼
               Quality Control
                     │
              ┌──────┴──────┐
              │             │
           PASS           FAIL
              │             │
              ▼             ▼
           Output        Regenerate
```

---

# 十、我建议你的 Cursor 项目目录

可以直接这样初始化：

```text
virtual-couple-agent/

├── README.md

├── .cursor/
│   └── rules/
│       ├── character-system.mdc
│       ├── scene-analysis.mdc
│       └── generation-rules.mdc

├── skills/

│   ├── character-registry/
│   │   └── SKILL.md
│   │
│   ├── scene-analyzer/
│   │   └── SKILL.md
│   │
│   ├── character-composer/
│   │   └── SKILL.md
│   │
│   ├── prompt-builder/
│   │   └── SKILL.md
│   │
│   ├── wallpaper/
│   │   └── SKILL.md
│   │
│   ├── couple-daily/
│   │   └── SKILL.md
│   │
│   ├── single-daily/
│   │   └── SKILL.md
│   │
│   └── quality-control/
│       └── SKILL.md

├── characters/

│   ├── character_A/
│   │   ├── character.yaml
│   │   ├── bible.md
│   │   └── references/
│   │
│   └── character_B/
│       ├── character.yaml
│       ├── bible.md
│       └── references/

├── relationship/
│   └── relationship.yaml

├── templates/

│   ├── wallpaper.yaml
│   ├── couple_daily.yaml
│   └── single_daily.yaml

├── outputs/

│   ├── drafts/
│   ├── approved/
│   └── rejected/

└── workflows/

    ├── generate_wallpaper.md
    ├── generate_couple.md
    └── generate_single.md
```

---

# 十一、真正适合你的 MVP：不要一开始做 Agent

这是我特别建议你的地方。

你本身已经做了很多 Agent，你很容易犯一个问题：

> **为了 Agent 化，把一个确定性的内容生产流程做得过于复杂。**

第一版建议做成：

```text
Workflow > Agent
```

因为这个任务其实是一个比较标准的 Pipeline。

---

## V1

你手动输入：

```text
角色：A + B
内容类型：情侣日常
参考图：scene.jpg
```

自动执行：

```text
1. Load Character
2. Analyze Scene
3. Build Prompt
4. Generate Image
5. QC
```

---

## V2

增加：

```text
Content Planner
```

用户只输入：

```text
帮我生成今天的小红书内容
```

系统自动：

```text
今天适合：
情侣咖啡馆日常

↓
寻找 Scene

↓
生成 4 张图片

↓
选择最佳图片

↓
生成标题
```

---

## V3

最终变成：

```text
Xiaohongshu Virtual IP Agent
```

自动：

```text
Content Planning
      ↓
Scene Selection
      ↓
Image Generation
      ↓
Image QC
      ↓
Cover Selection
      ↓
Title Generation
      ↓
Caption Generation
      ↓
Content Calendar
```

这时候你做的就不是：

> AI 图片生成工具

而是：

> **Virtual Couple Content Factory**

---

# 十二、你现在最应该先固定的“接口协议”

我建议所有 Skill 之间统一传递一个 JSON：

```json
{
  "task_id": "20260829_001",

  "characters": [
    "character_A",
    "character_B"
  ],

  "content_type": "couple_daily",

  "scene_reference": "scene_001.jpg",

  "scene_blueprint": {},

  "generation_config": {
    "aspect_ratio": "3:4",
    "style": "cinematic_realistic",
    "num_images": 4
  },

  "constraints": {
    "preserve_character_identity": true,
    "preserve_scene_composition": true,
    "preserve_scene_pose": true
  }
}
```

所有 Skill：

```text
Input JSON
↓
Process
↓
Output JSON
```

这样以后你无论：

* Cursor
* Claude Code
* OpenAI Codex
* 自己写 Python
* ComfyUI
* API

都可以复用。

---

# 十三、我认为最值得你优先解决的技术难点

你的难点不是 Prompt。

而是这三个：

## ① Character Identity Consistency

```text
每次生成都是同一个人
```

---

## ② Scene Pose Preservation

```text
Scene里面怎么站

生成后基本保持
```

---

## ③ Two-character Binding

```text
A永远是A

B永远是B
```

尤其双人生成非常容易：

```text
❌ A的脸跑到B身上
❌ 两个人融合
❌ 人物位置交换
❌ 多一只手
❌ 少一个人
```

所以你的 Workflow 必须明确：

```text
LEFT PERSON → Character A
RIGHT PERSON → Character B
```

而不是：

```text
Generate Character A and B
```

---

# 我的最终建议

你这个项目可以定义成：

> **Reference-driven Virtual Character Content Generation System**

第一阶段不要追求“全自动 Agent”。

先做一个稳定的：

```text
Scene Reference
      +
Character Bible
      +
Content Type
      ↓
Scene Analysis
      ↓
Character Binding
      ↓
Prompt Composition
      ↓
Image Generation
      ↓
Visual QC
```

等这个 Pipeline 稳定之后，再在最上面增加：

```text
Content Planner Agent
```

形成：

```text
          Virtual IP Agent
                 │
          Content Planning
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
  Couple Daily         Single Daily
       │                   │
       └─────────┬─────────┘
                 ▼
          Scene-driven Pipeline
                 ▼
            Image Factory
                 ▼
          Xiaohongshu Assets
```

**下一步我建议直接进入工程设计阶段：我可以继续帮你把这套系统具体拆成 Cursor 可执行的 `SKILL.md` 文件，包括 `Character Registry`、`Scene Analyzer`、`Character Composer`、`Prompt Builder` 四个核心 Skill 的完整 Prompt、输入输出 Schema 和目录结构。**

---

# 十四、Style Differentiation Gate（换脸前差异化询问）

## 核心需求

生成图与 Scene 参考图的关系：

| 维度 | 是否必须与 Scene 一致 |
|------|----------------------|
| 构图、镜头、人物位置 | ✅ 必须一致 |
| 动作、姿势、互动 | ✅ 必须一致 |
| 环境、背景、光影 | ✅ 必须一致 |
| 角色脸部身份 | ✅ 必须一致（Character Bible） |
| **装饰物**（耳机、墨镜、眼镜、帽子等） | ❌ **可不同，需询问用户** |
| **衣服颜色** | ❌ **可不同，需询问用户** |
| **图案**（条纹、格子、印花等） | ❌ **可不同，需询问用户** |
| **材质/款式细节** | ❌ **可不同，需询问用户** |

> **换脸（GenerateImage）之前，必须先询问用户可换选项，确认后再生成。**

## 更新后的 Pipeline

```text
Scene Reference
      ↓
Scene Analysis（提取构图 + customizable_elements）
      ↓
★ Scene Customizer — AskQuestion 询问用户 ★
      ↓（用户确认后）
Character Binding
      ↓
Prompt Composition（合并 customization_manifest）
      ↓
Image Generation
      ↓
Visual QC
```

## 询问项（每角色）

1. **装饰物**：保持原场景 / 角色默认（Tom→眉框眼镜）/ 墨镜 / 耳机 / 无装饰
2. **上衣颜色**：保持原场景 / 白 / 黑 / 藏青 / 浅蓝 / 其他
3. **上衣图案**：保持原场景 / 纯色 / 条纹 / 格子
4. **下装颜色**：保持原场景 / 黑 / 灰 / 藏青 / 其他
5. **下装图案**：保持原场景 / 纯色 / 其他

用户快捷指令：

- `全部保持原场景` → 跳过逐项询问，全部 `keep_scene`
- `Tom 戴耳机，衣服 navy` → 解析后直接写 manifest

## 实现位置

- Skill: `.cursor/skills/scene-customizer/SKILL.md`
- Manifest 模板: `templates/customization_manifest.example.json`
- 主编排: `virtual-couple` Step 4 强制暂停

## 设计原则

```text
Scene 决定「怎么站、在哪、做什么」
Character 决定「是谁」
Customization 决定「穿什么、戴什么」—— 可与 Scene 不同，但必须用户确认
```
