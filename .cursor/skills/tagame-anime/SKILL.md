---
name: tagame-anime
description: >-
  Tagame anime pipeline: confirm a scene card, generate one Japanese-anime
  still, post 3–5 diverse Japanese dialogue options and wait, then write a 10s
  i2v prompt for the chosen lines. Use when the user mentions Tagame, @Tagame,
  characters/Tagame, docs/anime.md, 动漫画风, 办公室肌肉上司, or asks for Tagame 场景图
  / 图生视频 / 10秒视频. After the video prompt, run douyin-caption (账号：猛男日语教学).
  Never photoreal; never Teo/Kai couple pipeline.
---

# Tagame Anime — Bible Still → 台词选项 → 10s i2v

固定角色 **Tagame**（办公室肌肉上司）。画风 **永远是高品质日系动漫**，禁止写实。

先按 Character Bible 补全场景卡，**等用户确认再出静帧**；静帧通过后 **先给 3–5 组不同情绪的日语台词，等用户选一组**，再写 **10 秒图生视频提示词**。不要默认套「邀请 → 身体热度 → 占有」。

公式与台词库：[formula.md](formula.md)。发布文案（抖音 / 猛男日语教学）：`douyin-caption`。

本 skill **不要**走 `virtual-couple` / `text-scene` / `pose-series` / `gemini-video`（那些是 Teo/Kai 写实线）。

| Mode | Input | Do | Forbidden |
|------|--------|-----|-----------|
| **A 场景卡** | 文字 / @Tagame / 无静帧 | 填场景卡 → STOP | GenerateImage、视频提示词、定稿台词 |
| **B 出图** | 用户回复 `生成` / 修改后确认 | GenerateImage **一张** 动漫静帧 → QC | 写实、换脸、立刻写视频词 |
| **C1 台词** | 已有 Tagame 成图，或 B 刚通过 | 贴 **3–5 组**不同弧的台词 → STOP | GenerateImage、i2v 复制块 |
| **C2 视频词** | 用户回复编号 / 选定台词 | 写 10s i2v 复制块 → 跑 `douyin-caption` | GenerateImage |

用户同一条消息里说「直接生成」且场景够用：仍先贴场景卡，再出图，再进 C1。  
已有成图 + 只要视频词：跳过 A/B，**仍要跑 C1**（除非用户已经指定台词）。  
已有成图 + 用户已给台词或选了编号：跳过 C1，只跑 C2。

---

## Art style lock（任何 Tagame 步骤）

- 高品质日系动漫 / 现代数字插画 / 干净线稿 + 细腻光影
- 匹配 `characters/Tagame/references/face_01.jpeg` 的 bara 肌肉男动漫脸
- **禁止：** photorealistic、真人摄影、3D CGI、美颜写实、HDR 真人光
- **禁止：** 清俊少年、削瘦、换脸、混入 Teo/Kai
- 服装可按场景变，**脸+体型+胡茬+深棕短发**锁定参考图

---

## Load

1. `characters/Tagame/bible.md`
2. `characters/Tagame/character.yaml`
3. Face ref: `characters/Tagame/references/face_01.jpeg`（fallback `characters/Tagame/Tagame.jpeg`）
4. Formula: [formula.md](formula.md)

Identity prompt（出图 + 视频 IDENTITY LOCK 都用）：

```text
Tagame: mature East Asian man ~40, square jaw, dark-brown short slightly wavy spiked hair swept up, neat brown stubble/beard, thick angled brows, confident half-smile, extremely muscular (broad shoulders, full chest, thick arms, narrow waist). High-quality Japanese anime / digital illustration, clean linework, not photorealistic. Match the attached character reference exactly.
```

---

## Turn A — 场景卡（先确认）

无静帧、或用户要新场景时：用 Bible 填缺口。用户原文覆盖默认值；**不能**改画风、削肌肉、换脸。

写 `outputs/drafts/tagame_scene_<task_id>.json`，`"user_confirmed": false`。

### 缺口默认

| Slot | 用户没说时 |
|------|------------|
| Who | 仅 Tagame，对镜头（お前） |
| Place | 办公室走廊 |
| Time | 加班深夜或刚运动完回楼 |
| Light | 商务冷色室内光，正常曝光，不要提亮成封面光 |
| Outfit | 紧身白衬衫解开两颗扣；可选汗湿贴身；黑西裤+黑皮带银扣；外套可脱 |
| Pose / 第一帧 | 仰拍、双手插腰或一手撑腰，直视镜头，第一帧就要抓人 |
| Intensity | 标准（用来筛选台词弧，不锁定「邀请→占有」） |
| Wet shirt | 开（公式母题）；用户说不要湿则关 |
| Camera | 低角度仰拍，3:4 中近景 |

场景池：办公室走廊 / 健身房更衣室 / 车里 / 酒店走廊 / 雨中 / 深夜加班工位。

### 回复模板（必须用，然后 STOP）

```text
✅ Tagame 场景已按人设补全（动漫画风锁定，可改）

【谁】仅 Tagame，对镜头里的「你」
【时间地点】{...}
【构图】3:4 {中近景}，仰拍
【第一帧】{插腰/摸胸口前的静止姿态，要抓人}
【服装】{白衬衫±汗湿±解开扣 / 西裤 / 外套}
【光】{冷色办公室光，不要过亮}
【情绪强度】温柔 / 标准 / 强势 / 调戏  → 当前：{...}
【台词】出图后给 3–5 组不同情绪的日语台词，你选一组再写图生视频提示词（不会默认「邀请→热→占有」）

改法直接说，例如：不要湿衬衫、改成更衣室、强度改温柔、镜头再低。
快捷：「生成」

⏸️ 请确认后再出图。
```

**本回合结束。禁止 GenerateImage。禁止写视频提示词。禁止贴定稿三句台词。**

---

## Turn B — 一张动漫静帧

1. 把用户修改合并进 JSON，`"user_confirmed": true`
2. 保存 `outputs/drafts/prompt_tagame_<task_id>.txt`
3. 调用 GenerateImage **一次**：

```json
namespace: "cursor"
toolName: "GenerateImage"
arguments: {
  "description": "<prompt>",
  "filename": "tagame_<task_id>.png",
  "aspect_ratio": "3:4",
  "reference_image_paths": ["characters/Tagame/references/face_01.jpeg"]
}
```

无场景照片。`reference_image_paths` **只有** Tagame 脸图。若用户给了构图参考，可加在列表最前，并写明：只借构图/机位，人物必须是动漫 Tagame，不要参考图里的真人脸。

4. QC → 通过则复制到 `outputs/approved/tagame_<task_id>.png`
5. **立刻进入 Turn C1**（用户说只要图、先不出视频词时除外）

### 静帧 prompt

```text
[ART STYLE — highest priority]
High-quality Japanese anime / modern digital illustration. Clean linework, refined cel-shaded lighting, bara muscular aesthetic. NOT photorealistic. NOT live-action. NOT 3D CGI. NOT a real photograph. Match the attached anime character reference.

[CHARACTER IDENTITY]
Only one person: Tagame. {identity prompt}
Use the attached face reference. Keep the beard, dark-brown short spiked hair, square jaw, and extreme musculature. Do not slim him. Do not make a pretty-boy. Do not add other people.

[SCENE]
{place}, {time}.
{environment and 1–2 props}. Cool office-toned background unless the user chose another place.

[COMPOSITION]
Vertical 3:4. {framing}. LOW-ANGLE shot looking up at him. Face in the upper two-thirds. First-frame hook: {pose}. He looks at the camera as if speaking to the viewer.

[POSE]
{filled first-frame pose}. Powerful, inviting, not a fashion catalog stance.

[CLOTHING]
{filled}. Shirt stays on. Tasteful tension (open collar / optional sweat-damp fabric). No nudity.

[LIGHTING]
{lighting}. Match a real indoor brightness — do not over-brighten into cheap AI glow. Keep contrast.

[CONSTRAINTS]
Anime still, one adult man, correct anatomy, no extra limbs. No text, watermark, logo, or subtitles on the image. No Teo, no Kai, no photoreal skin pores.
```

### QC（Tagame）

| Check | Fail if |
|-------|---------|
| Style | 看起来像照片/真人 |
| Face | 不像参考：没胡茬、发色错、脸嫩 |
| Body | 被画瘦、肩窄 |
| Frame | 不是 3:4、第一帧没有压迫感/抓人 |
| Cast | 多了人、混入 Teo/Kai |
| Scale | 裸体或过露 |

`accept` → 批准路径。`regenerate` 最多 1 次（收紧画风/身份）。`reject` → `outputs/rejected/`。

---

## Turn C1 — 3～5 组台词选项（先选再写提示词）

只出选项，**不要** GenerateImage，**不要**写 i2v 复制块。

1. 读成图（谁、场景、姿态、服装、是否汗湿）+ 场景卡强度
2. 按 [formula.md](formula.md) 选 **3–5 个不同弧**（加班责问 / 命令靠近 / 温柔允许 / 调戏 / 更衣室 / 雨湿 / 车里 / 酒店 / 教学向 / 经典邀请占有）
3. **禁止** 5 组都是「邀请 → 身体热度 → 占有」，也禁止 5 组只改几个假名、弧名却一样
4. 至少 1 组标「好教」（语法点清楚，方便抖音号「猛男日语教学」）
5. 保存 `outputs/drafts/tagame_lines_<task_id>.json`，`"user_confirmed": false`
6. 按模板回复，然后 **STOP**

### 回复模板

```text
✅ 台词选项（身份/服装/场景锁定成图；选一组后我再写 10 秒图生视频提示词）

【谁】仅 Tagame，对镜头（お前）
【场景】{地点 · 服装一句话}
【强度】{温柔 / 标准 / 强势 / 调戏}

1️⃣ 【{弧名}】{一句话情绪} {好教则标 ·好教}
1 {kana} ｜ {中文}  （{语法钩}）
2 {kana} ｜ {中文}
3 {kana} ｜ {中文}

2️⃣ 【{弧名}】…
3️⃣ 【{弧名}】…
4️⃣ 【{弧名}】…   ← 至少 3 组，最多 5 组
5️⃣ 【{弧名}】…

回复编号即可，例如：`2` 或 `用第3组，强度再强一点`。
也可以自己贴三句（我会转成假名）。

⏸️ 请选择后再生成图生视频提示词。
```

**本回合结束。禁止输出英文 i2v 块。**

---

## Turn C2 — 10s 图生视频提示词

用户选定编号（或贴了台词）之后才进入。只写提示词，**不要** GenerateImage。目标：Gemini / 通用 i2v，竖屏 10 秒。

1. 把选定弧写入 JSON，`"user_confirmed": true`；三条台词进 `dialogue`
2. 第一条台词 **2.0s** 开口；动作匹配 **该弧**，不要强行写成摸胸→热→占有（除非选的就是经典 A）
3. 台词 **假名**；中文放在聊天标题里给用户烧字幕（日+中）
4. 保存：
   - `outputs/drafts/tagame_video_<task_id>.json`
   - `outputs/drafts/tagame_video_<task_id>.txt`（仅复制块）
5. 按下面模板回复。复制块用一个 `text` fence，里面不要写中文说明
6. **同一回合**再跑 `.cursor/skills/douyin-caption/SKILL.md`（账号：猛男日语教学）。用户说只要视频词、先不要发布文案时除外

### 回复模板

```text
✅ Tagame 10秒图生视频提示词（身份/服装/场景锁定成图，动漫画风，只加动作和声音）

【用法】打开 Gemini（或你的 i2v）→ 上传这张成图 → 粘贴下面英文块 → 时长 10s / 竖屏

【谁】仅 Tagame，对镜头（お前）
【情绪弧】{用户选的弧名}（不是默认邀请→占有，除非选了那一组）
【从静止到动作】{匹配该弧的动作，一句}
【台词】第一条 @2.0s
Tagame：「{kana}」  {中文}
Tagame：「{kana}」  {中文}
Tagame：「{kana}」  {中文}

【字幕】模型里不要烧字；发布时叠日文+中文。

【复制到模型】
```

（此处一个 `text` 代码块 = 英文提示词）

然后接 `douyin-caption` 的发布复制块。

结尾：`改法直接说，例如：换第4组台词、强度改温柔、不要湿、镜头再近。`

### i2v 复制块模板

`MOTION` 的 2.0 / 4.5 / 7.0 三段按 **所选弧** 填，不要写死 hand-to-chest → body-heat → possession。

```text
Animate the uploaded image into a 10-second ANIME video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change, no nudity.

ART STYLE LOCK: Keep high-quality Japanese anime / digital illustration look of the still. Do NOT restyle into photorealistic live action. Do NOT turn him into a real person.

FICTION: Original fictional adult anime character only (Tagame, late 30s–early 40s). Not a real person. Not based on any living person. Suggestive but clothed. No explicit nudity.

IDENTITY LOCK: Keep the exact anime face, dark-brown short spiked hair, brown beard, extreme musculature, clothing, sweat/damp state, lighting, and location from the uploaded image. Do not add or remove people. Do not slim him. Do not make him a pretty-boy.

CAST: The muscular anime man is Tagame, a mature office superior speaking directly to the viewer (second person). Voice: low, slightly breathy mature Japanese male.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: tiny living motion from the still — chest breathing, blink, micro weight shift, inhale as if about to speak. Low angle stays. No silent stare without preparing to talk.
2.0-4.5s: FIRST LINE STARTS at 2.0s. {arc beat 1 motion}.
4.5-7.0s: second line. {arc beat 2 motion}. He may move slightly closer to camera.
7.0-9.5s: third line. {arc beat 3 motion}. Hold the gaze.
9.5-10.0s: short end hold on the face/chest. Do not freeze into a mute stare.

CAMERA: {low-angle slow push-in toward chest and face}. Do not whip-pan. Do not cut. First frame already has impact — do not start with a wide empty hallway.

AUDIO: Japanese speech only. Lip-sync the quoted lines. Lines are hiragana/katakana only (no kanji). No English. No Chinese. No on-screen text, subtitles, captions, logos, or watermarks. No background music. Room tone: {office corridor HVAC / rain / car interior}. Foley: {shirt fabric, one footstep, breath}.

DIALOGUE (spoken in Japanese, written in kana; he is talking to YOU):
Tagame says: "{kana line 1}"
Tagame says: "{kana line 2}"
Tagame says: "{kana line 3}"

CONSTRAINTS: Anime, not photoreal. Clothes stay on. First spoken line at 2.0s. After 2s keep dialogue dense. Direct address only (no third-person narrator). Suggestive tension through clothing, not explicit.
```

台词规则、弧目录、强度、拒稿改写：见 [formula.md](formula.md)。示例：见 [examples.md](examples.md)。

---

## JSON

场景卡：

```json
{
  "task_id": "20260905_office_corridor",
  "user_confirmed": false,
  "cast": ["tagame"],
  "art_style": "japanese_anime",
  "scene": {
    "place": "office corridor",
    "time": "late night overtime",
    "lighting": "cool fluorescent, real indoor exposure",
    "framing": "medium-close 3:4 low-angle",
    "pose": "hands on hips, looking at camera",
    "clothes": "tight white shirt two buttons open, optional sweat-damp, black suit pants",
    "wet_shirt": true,
    "intensity": "standard"
  }
}
```

台词选项：

```json
{
  "task_id": "20260905_office_corridor",
  "user_confirmed": false,
  "source_image": "outputs/approved/tagame_20260905_office_corridor.png",
  "options": [
    {
      "id": 1,
      "arc": "overtime_blame",
      "arc_zh": "加班责问",
      "teachable": true,
      "lines": [
        { "kana": "こんなじかんまで、のこってたのか", "zh": "都这时候了，你还留着？" },
        { "kana": "おまえのせいだ、かえれなくなる", "zh": "都是你的错，我回不去了" },
        { "kana": "ほら、こっちをみろ", "zh": "喂，看这边" }
      ]
    }
  ]
}
```

视频词：

```json
{
  "task_id": "20260905_office_corridor_v",
  "source_image": "outputs/approved/tagame_20260905_office_corridor.png",
  "cast": ["tagame"],
  "duration_sec": 10,
  "art_style": "japanese_anime",
  "arc": "overtime_blame",
  "first_line_at_sec": 2.0,
  "dialogue": [
    { "who": "tagame", "kana": "こんなじかんまで、のこってたのか", "zh": "都这时候了，你还留着？", "at_sec": 2.0 },
    { "who": "tagame", "kana": "おまえのせいだ、かえれなくなる", "zh": "都是你的错，我回不去了", "at_sec": 4.5 },
    { "who": "tagame", "kana": "ほら、こっちをみろ", "zh": "喂，看这边", "at_sec": 7.0 }
  ]
}
```

`task_id`：`{YYYYMMDD}_{scene}`；视频加 `_v`。不要再写死 `"formula": ["invite", "body_heat", "possession"]`。

---

## 路由

| 用户说了 | 走 |
|----------|-----|
| @Tagame / 田龟式肌肉上司 / docs/anime.md | **本 skill**（A→B→C1→C2） |
| 已有 Tagame 成图 + 图生视频 | 本 skill **C1**（先选项） |
| 已选台词编号 / 已贴三句 | 本 skill **C2** + `douyin-caption` |
| 抖音文案 / 猛男日语教学 / 抖音标题标签 | `douyin-caption`（台词须已选定） |
| @Teo / @Kai / 换脸照片 | `virtual-couple` 或 `text-scene`，**不要**本 skill |
| Teo/Kai 成图 + 图生视频 | `gemini-video`（写实） |
