---
name: tagame-anime
description: >-
  Tagame anime pipeline: if the user has no scene still, generate one
  Japanese-anime image from the Tagame face reference to match the dialogue
  scene. Then either (a) post 5 diverse Japanese dialogue options, or (b) use
  user-supplied Japanese/English lines. Long scripts split into multiple 10s
  i2v clips. After the video prompt, run douyin-caption (账号：猛男日语教学).
  Use when the user mentions Tagame, @Tagame, characters/Tagame, docs/anime.md,
  动漫画风, 办公室肌肉上司, CuteGuysArt, or asks for Tagame 场景图 / 图生视频 / 10秒视频.
  Never photoreal; never Teo/Kai couple pipeline. Default art is Japanese anime.
  CuteGuysArt only when the user names that style.
---

# Tagame Anime — Bible Still → 台词选项 → 10s i2v

固定角色 **Tagame**（办公室肌肉上司）。默认画风是 **高品质日系动漫**。用户点名 **CuteGuysArt** 时，改用该风格出图和锁视频画风。两种都禁止写实。

先按 Character Bible 补全场景。静帧通过后：

- **没给台词** → **先读成图/场景卡**，再给 **5 组不同风格**日语台词，等用户选一组，再写 10s 图生视频提示词。
- **用户已给日语或英语台词** → **跳过 C1**，用用户原文（英译日、日转假名）。**一句/三句塞进一条 10s**；**较长则按长度拆成多条独立 10s**（每段用自己的参考图生成，看起来像同一场景的连续瞬间）。身份、服装、场景、机位锁定；每段必须完成一个跟台词对应的主动作，参考图只是起始姿态。第 2 段起上传上一段最后一帧，不要每段回到原静帧，也不要推镜头。

**没有用户参考图 / 成图时：** 不要干等场景卡。用 Tagame 脸图 `characters/Tagame/references/face_01.jpeg` **直接出一张**符合 **台词场景** 的动漫静帧（没台词才用办公室默认）。禁止向用户再要一张真人场景照。

不要默认套「邀请 → 身体热度 → 占有」。

公式与台词库：[formula.md](formula.md)。发布文案（抖音 / 猛男日语教学）：`douyin-caption`。

本 skill **不要**走 `virtual-couple` / `text-scene` / `pose-series` / `gemini-video`（那些是 Teo/Kai 写实线）。

**场站巡逻职业线**（大野健一 / `characters/Tagame-patrol` / `docs/patorl-tagame.md`）走 `tagame-patrol`。那边的场景和台词锁职业故事；写出的 10 秒视频词仍用本 skill 的 C2 / C2-S，不要换成办公室脸图。

| Mode | Input | Do | Forbidden |
|------|--------|-----|-----------|
| **A 场景卡** | 只 @Tagame / 要新场景，**没台词、没说出图** | 填场景卡 → STOP | GenerateImage |
| **B 出图** | `生成` / 出图，或 **无用户图且已有台词** | GenerateImage **一张**（脸图=Tagame 参考图；场景跟台词走） | 写实、向用户再要场景照 |
| **C1 台词** | 已有 Tagame 成图，**且用户没贴台词** | **先读图** → 贴 **5 组**不同风格台词 → STOP | GenerateImage、i2v 复制块、没读图就编台词 |
| **C2 视频词** | 用户回复编号 / 选定短台词 | 写 **一条** 10s i2v 复制块 → 跑 `douyin-caption` | GenerateImage |
| **C2-S 长台词** | 用户贴的日语或英语 **超过一条 10s**（约 >3 句） | 转假名；拆成 **N 条独立 10s**；**同一套 BASE** + 每段自己的 ACTION PLAN / 时间轴 / 台词 / 收势 | GenerateImage、写成「一段 40s 的第 N 截」、换景、走出画面、猛推镜头 |

**无用户参考图 + 已给台词：** 跳过 A 的 STOP，本回合按台词场景出静帧，再进 C2 / C2-S。  
**无用户参考图 + 用户说生成/出图（没台词）：** 跳过 A 的 STOP，办公室默认出静帧，再进 C1。  
只 @Tagame、没台词、没说出图：仍走 A。  
已有成图 + 只要视频词、**没贴台词**：跳过 A/B，**仍要跑 C1**。  
已有成图 + 用户已给日语/英语台词或选了编号：跳过 C1，只跑 C2（短）或 C2-S（长）。

---

## Art style lock（任何 Tagame 步骤）

先判定本轮画风，再写静帧和 i2v。没点名就用默认，不要把 CuteGuysArt 套进普通 Tagame。

| 用户怎么说 | `art_style` | 用哪一块 |
|------------|-------------|----------|
| 没提画风，或只说动漫 / 日系 | `japanese_anime` | 默认日系块 |
| **CuteGuysArt**、Cute Guys Art、风格 CuteGuysArt、限定 CuteGuysArt | `cuteguysart` | `.cursor/skills/cuteguysart/SKILL.md` 的静帧段。说明：`docs/tagame_style.md` |

两种画风共用这些锁：

- 匹配 `characters/Tagame/references/face_01.jpeg`：深棕短刺发、棕色胡茬、方颌、约 40 岁、极度肌肉
- **禁止：** photorealistic、真人摄影、3D CGI、美颜写实、HDR 真人光
- **禁止：** 清俊少年、削瘦、换脸、混入 Teo/Kai
- 服装按场景走（衬衫留在身上）。CuteGuysArt **不要**照搬风格参考里的白背心、牛仔短裤、彩虹袜、网球场，除非用户自己要那个场景

### 默认：`japanese_anime`

```text
High-quality Japanese anime / modern digital illustration. Clean linework, refined cel-shaded lighting, bara muscular aesthetic. NOT photorealistic. NOT live-action. NOT 3D CGI. NOT a real photograph. Match the attached anime character reference.
```

### 点名才用：`cuteguysart`

先读 `.cursor/skills/cuteguysart/SKILL.md`，把其中的静帧段原样贴进 `[ART STYLE]`。人仍是 Tagame。参考图在 `docs/STYLE/`，只借粗线卡通、暖肤和明亮生活场景的画法，不借网球场、背心、彩虹袜、温泉和截图界面。

i2v 用该 skill 的 `ART STYLE LOCK`：锁粗手绘轮廓线、赛璐璐加柔和皮肤、中等有神的眼睛、自然大型肌肉和明亮高饱和。不要写成大眼睛光泽倒三角，也不要写回默认日系细线暗调。

---

## Load

1. `characters/Tagame/bible.md`
2. `characters/Tagame/character.yaml`
3. Face ref: `characters/Tagame/references/face_01.jpeg`（fallback `characters/Tagame/Tagame.jpeg`）
4. Formula: [formula.md](formula.md)

Identity prompt（**出静帧**用。图生视频不要靠这段点名，用上传图 + CHARACTER LOCK）：

```text
Tagame: mature East Asian man ~40, square jaw, dark-brown short slightly wavy spiked hair swept up, neat brown stubble/beard, thick angled brows, confident half-smile, extremely muscular (broad shoulders, full chest, thick arms, narrow waist). High-quality Japanese anime / digital illustration, clean linework, not photorealistic. Match the attached character reference exactly.
```

CuteGuysArt 出图时，不要再写 `High-quality Japanese anime`。身份句用 `cuteguysart` skill 里的 Tagame 句：同一张脸，改成中等有神的眼睛和温暖自信的笑。发色、胡茬、方颌仍锁脸图。不要写成美少年或过大的二次元眼睛。

---

## Turn A — 场景卡（仅「只点名、还不出图」）

**无用户参考图且（已给台词 或 已说生成/出图）→ 跳过本回合，直接 Turn B。**

只 @Tagame / 要新场景、还没台词、也没说出图时：用 Bible 填缺口。用户原文覆盖默认值。**不能**削肌肉、换脸、改成写实。画风只有用户点名 CuteGuysArt 才离开默认日系。

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
✅ Tagame 场景已按人设补全（画风：{默认日系动漫 / CuteGuysArt}）

【谁】仅 Tagame，对镜头里的「你」
【画风】{默认日系动漫 / CuteGuysArt}
【时间地点】{...}
【构图】3:4 {中近景}，仰拍
【第一帧】{插腰/摸胸口前的静止姿态，要抓人}
【服装】{白衬衫±汗湿±解开扣 / 西裤 / 外套}
【光】{冷色办公室光，不要过亮}
【情绪强度】温柔 / 标准 / 强势 / 调戏  → 当前：{...}
【台词】{用户已给日/英台词 → 出图后按长度拆 10s 段，不再给 5 组选项 / 未给 → 出图后先读成图，再给 5 组不同风格日语台词}

改法直接说，例如：不要湿衬衫、改成更衣室、强度改温柔、镜头再低。
快捷：「生成」

⏸️ 请确认后再出图。
```

**本回合结束。禁止 GenerateImage。禁止写视频提示词。禁止贴定稿三句台词。**

---

## Turn B — 一张动漫静帧

**无用户参考图 = 正常情况。** 不要向用户再要场景照。身份只锁 Tagame 脸图。

1. 合并场景（见下「台词 → 场景」）。JSON `"user_confirmed": true`
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

`reference_image_paths` **必须有** Tagame 脸图（fallback `characters/Tagame/Tagame.jpeg`）。  
用户 **没给** 构图参考 → 列表里 **只有** 这张脸图，场景全靠 prompt。  
用户 **给了** 构图参考 → 构图图放列表最前，并写明：只借构图/机位，人物必须是动漫 Tagame，不要参考图里的真人脸。

4. QC → 通过则复制到 `outputs/approved/tagame_<task_id>.png`
5. **用户已贴日语/英语台词 → 跳过 C1，同一回合进 C2 或 C2-S**（静帧当第 1 段参考图）。没台词则进 C1（用户说只要图除外）

### 台词 → 场景（无用户图时必填，不要一律走廊湿衬衫）

先读用户台词（日/英），再填 place / outfit / pose。脸、体型、胡茬仍锁参考图。

| 台词里出现 | 地点 | 服装/姿态 |
|------------|------|-----------|
| 暗記 / 本 / 問題 / 学校 / 宿題 / 人生 / 延ばす | 办公室工位或走廊，可有文件夹/书 | 西装+白衬衫+领带（贴近脸图）；插腰或撑桌，说教眼神 |
| 残業 / こんなじかん / のこって | 深夜办公室走廊 | 可湿衬衫解开扣，插腰拦人 |
| うんどう / さめない / 更衣室 | 健身房更衣室 | 汗湿白衬衫，刚练完 |
| ぬれ / 雨 | 楼下门口或雨中 | 湿衬衫 |
| せまい / 车 | 车内 | 西装，座位上对镜头 |
| ホテル / しずかに | 酒店走廊 | 西装，压低声音的姿态 |
| 看不出 | 办公室走廊 | 脸图那套西装；仰拍插腰 |

用户明文指定的地点/服装 **覆盖** 上表。

### 静帧 prompt

```text
[ART STYLE — highest priority]
{粘贴本轮画风块：默认日系，或用户点名后的 CuteGuysArt 整段}

[CHARACTER IDENTITY]
Only one person: Tagame. {identity prompt}
Use the attached face reference. Keep the beard, dark-brown short spiked hair, square jaw, and extreme musculature. Do not slim him. Do not make a pretty-boy. Do not add other people.

[SCENE]
{place from 台词→场景 table, or user override}, {time}.
{environment and 1–2 props that match the lines}. Cool office-toned background unless the lines need locker / rain / car / hotel.

[COMPOSITION]
Vertical 3:4. {framing}. LOW-ANGLE shot looking up at him. Face in the upper two-thirds. First-frame hook: {pose}. He looks at the camera as if speaking to the viewer.

[POSE]
{filled first-frame pose}. Powerful, inviting, not a fashion catalog stance.

[CLOTHING]
{filled}. Shirt stays on. Tasteful tension (open collar / optional sweat-damp fabric). No nudity.

[LIGHTING]
{默认日系：} {lighting}. Match a real indoor brightness — do not over-brighten into cheap AI glow. Keep contrast.
{CuteGuysArt：} Bright cheerful light, warm skin, high saturation. The place stays the requested scene and stays a drawn lifestyle setting. Do not repaint it as a photograph, and do not replace it with the tennis court, rainbow socks, or hot spring from docs/STYLE.

[CONSTRAINTS]
One adult man, correct anatomy, no extra limbs. No text, watermark, logo, or subtitles on the image. No Teo, no Kai, no photoreal skin pores. CuteGuysArt stills must literally include the words CuteGuysArt style.
```

### QC（Tagame）

| Check | Fail if |
|-------|---------|
| Style | 看起来像照片/真人。点了 CuteGuysArt 却画成细腻日系，或没点名却画成 CuteGuysArt。CuteGuysArt 成图照搬了网球场、白背心、彩虹袜 |
| Face | 不像参考：没胡茬、发色错、脸嫩 |
| Body | 被画瘦、肩窄 |
| Frame | 不是 3:4、第一帧没有压迫感/抓人 |
| Cast | 多了人、混入 Teo/Kai |
| Scale | 裸体或过露 |

`accept` → 批准路径。`regenerate` 最多 1 次（收紧画风/身份）。`reject` → `outputs/rejected/`。

---

## Turn C1 — 先读图，再给 5 组不同风格台词

只出选项，**不要** GenerateImage，**不要**写 i2v 复制块。

**禁止跳过读图。** 没读成图 / 场景卡就写台词 = 失败。台词必须像这个人、在这个地方会说的话，不能套万能调情三段。

1. **先读原始图片设定**（成图 + 场景卡 JSON + Bible）。看清：地点、时间、姿态、服装、是否汗湿、光线、镜头、强度、他在对谁说话
2. **先写【读图】摘要**（见模板），证明读过这张图，再写台词
3. 按 [formula.md](formula.md) 出 **正好 5 组**，5 个 **不同弧 + 不同风格**。从目录里挑最贴本场景的，再混入不同情绪（责问 / 命令 / 温柔 / 调戏 / 教学 / 经典邀请等），**不要 5 组同一种味道**
4. 每组三句都要吃进本图事实：走廊加班就说留到这么晚；更衣室就说刚练完；雨景才说湿；车里才说挤。禁止更衣室说酒店、雨景说加班、干衬衫硬说汗湿
5. **禁止** 5 组都是「邀请 → 身体热度 → 占有」，也禁止只改几个假名、弧名却一样
6. 至少 1 组标「好教」（语法点清楚，方便抖音号「猛男日语教学」）
7. 保存 `outputs/drafts/tagame_lines_<task_id>.json`，`"user_confirmed": false`
8. 按模板回复，然后 **STOP**

### 回复模板

```text
✅ 台词选项（先读成图，再按本角+本场景写；选一组后我再写 10 秒图生视频提示词）

【读图】
地点：{办公室走廊 / 更衣室 / 车里 / …}
时间：{深夜加班 / 刚练完 / …}
姿态：{插腰 / 撑墙 / …} · 镜头：{仰拍中近景}
服装：{白衬衫±汗湿±解开扣 / 西裤}
光 / 强度：{冷色室内 · 标准/温柔/强势/调戏}
本图能说：{一句：他现在为什么开口，例如「抓到你还没走」}

【谁】仅 Tagame，对镜头（お前）——办公室肌肉上司，成熟、低沉、直接

1️⃣ 【{弧名}】{本图里这种风格为什么成立} {好教则标 ·好教}
1 {kana} ｜ {中文}  （{语法钩}）
2 {kana} ｜ {中文}
3 {kana} ｜ {中文}

2️⃣ 【{弧名}】…   ← 与①风格不同
3️⃣ 【{弧名}】…   ← 再换一种
4️⃣ 【{弧名}】…
5️⃣ 【{弧名}】…   ← 必须 5 组，5 种风格

回复编号即可，例如：`2` 或 `用第3组，强度再强一点`。
也可以自己贴日语或英语台词（短的一条 10s；长的按长度拆成多条 10s，画面接着演）。

⏸️ 请选择后再生成图生视频提示词。
```

**本回合结束。禁止输出英文 i2v 块。没写【读图】就贴 5 组 = 不合格。**

---

## Turn C2 — 10s 图生视频提示词

用户选定编号（或贴了**短**台词）之后才进入。只写提示词，**不要** GenerateImage。目标：Gemini / 通用 i2v，**9:16** 竖屏 10 秒。

**用户贴了日语或英语台词：** 先走下面的「台词处理」。能塞进 **一条** 10s（约 3 句、总拍数 ≤ 42）→ 本回合 C2。**更长 → Turn C2-S**（多条 10s，画面连贯）。

1. 把选定弧写入 JSON，`"user_confirmed": true`；三条台词进 `dialogue`，并写入 `action_plan`
2. 第一条台词 **2.0s** 开口。先按下面的动作方案写 **一个主动作**（开始、发展、收势），不要把 10 秒写成只有呼吸、眨眼和口型。参考图是起始状态，不是整段冻住的姿态
3. 台词 **假名**；中文（及英语原文）放在聊天标题里给用户烧字幕。模型里 **只说日语，禁止即兴加句**
4. 保存：
   - `outputs/drafts/tagame_video_<task_id>.json`
   - `outputs/drafts/tagame_video_<task_id>.txt`（仅复制块）
5. 按下面模板回复。复制块用一个 `text` fence，里面不要写中文说明
6. **同一回合**再跑 `.cursor/skills/douyin-caption/SKILL.md`（账号：猛男日语教学）。用户说只要视频词、先不要发布文案时除外

### 用户给的日语 / 英语台词（C2 与 C2-S 共用）

1. **先读成图**（地点、姿态、服装、汗湿、光），台词意思不能和画面打架；不能改的只改口吻贴近 Tagame（お前、成熟上司），不改用户剧情
2. **日语**（汉字或假名）→ i2v 里写成 **ひらがな/カタカナ**，无汉字
3. **英语** → 先译成 **自然口语日语**（Tagame 会说的话），再转假名。聊天里保留：英语原文 ｜ 假名 ｜ 中文。**禁止**让模型说英语
4. 按句号 / 逗号 / 换行拆成「一口气」：每句 **6–16 拍（mora）**；太长就在从句切开，不要把一个单词切开
5. **容量：** 每条 10s = 前 2s 呼吸 + **最多 3 句**口播（2.0 / 4.5 / 7.0）。总拍数大约 **30–42**。第 4 句起必须下一条视频
6. 2 句也能成一条（2.0 / 5.5，主动作落在后一句，8.5s 起停在收势）。1 句且很短：仍一条 10s，后半段把主动作做完并停住，不要硬凑废话

### 回复模板

```text
✅ Tagame 10秒图生视频提示词（身份/服装/场景锁定，机位不动，姿态按台词表演）

【用法】打开 Gemini（或你的 i2v）→ 上传这张成图 → 粘贴下面英文块 → 时长 10s / **9:16** 竖屏

【谁】仅 Tagame，对镜头（お前）
【情绪弧】{用户选的弧名}（不是默认邀请→占有，除非选了那一组）
【主动作】{A0x · 一句：必须发生，并在结尾停住}
【辅助】{低头/抬眼/目光/表情里的一个}
【收势】{最后约 1.5 秒停在什么姿态}
【台词】第一条 @2.0s
Tagame：「{kana}」  {中文}
Tagame：「{kana}」  {中文}
Tagame：「{kana}」  {中文}

【字幕】模型里不要烧字；发布时叠日文+中文。

【复制到模型】
```

（此处一个 `text` 代码块 = 英文提示词）

然后接 `douyin-caption` 的发布复制块。

结尾：`改法直接说，例如：换第4组台词、主动作改成抬眼注视、不要伸手、强度改温柔。`

### i2v 复制块结构（C2 与 C2-S 共用）

设计说明：动作模块按 `docs/update_img2video.md`。独立片段、禁止 `Clip N of M`、禁止每段推镜头，仍按 `docs/modify_prompt.md`。**优先级：身份与场景锁定 > 指定主动作必须发生 > 机位锁定 > 台词。** 参考图是起始状态，不是整段冻住的姿态。

每段复制块按这 10 层写，**删掉重复的 ANIME / 不要 fade / 不要 cut**。单段 C2 用 BASE + ACTION PLAN + ACTION TIMELINE + DIALOGUE + END STATE。长台词 C2-S 用同一套 BASE，每段只改 CLIP STATE / ACTION PLAN / ACTION TIMELINE / DIALOGUE / END STATE。

**禁止：** `Clip 1 of 4 in one continuous take`（模型会当成要生成 40 秒再截一段）。  
**禁止：** 每段都写 `slow push-in toward chest`（四段会越推越近、构图漂掉）。  
**禁止：** 把人物名字当主锚点。锚点是 **上传的参考图**。

#### BASE（人物/画风/场景/镜头语言，各段相同）

```text
ANIME IMAGE-TO-VIDEO.
Create a 10-second vertical video from the uploaded reference image.

FORMAT:
Duration: 10 seconds. Aspect ratio: 9:16.
Single continuous shot. No cuts. No transitions. No fade. No new location. No costume change. No nudity.

REFERENCE IMAGE PRIORITY:
The uploaded image is the definitive reference for the character's identity, visual design, anime art style, clothing, environment, lighting, and initial pose.

Preserve the exact character identity: face, hairstyle, beard, muscular build, body proportions, clothing design, and overall visual appearance.
Preserve the original environment, architecture, lighting, color palette, and camera angle.

IMPORTANT DISTINCTION:
The reference image defines the initial visual state, not a frozen pose that must be maintained throughout the video.
The character is allowed to move naturally from the initial pose to perform the explicitly specified actions.
Temporary changes in hand position, arm position, head angle, gaze direction, facial expression, shoulder orientation, and upper-body posture are allowed when required by the action.
All movements must remain anatomically coherent and consistent with the original character design.

Do not redesign the character.
Do not alter his identity, body proportions, clothing design, or the surrounding environment.

ART STYLE LOCK:
{默认日系：} Preserve the exact high-quality Japanese anime / digital illustration style of the reference image.
{CuteGuysArt：} Preserve the exact CuteGuysArt rendering of the reference image: modern cartoon illustration, bold clean hand-drawn contour lines, cel shading mixed with soft painterly skin, warm skin with soft highlights, medium expressive eyes, bright saturated color, powerful natural muscle including thick thighs. Do not redraw him with oversized anime eyes, thin manga linework, or the default refined Japanese office illustration.
Do not convert him into photorealistic live action. Do not make him look like a real person.

CHARACTER LOCK:
The adult muscular anime man shown in the reference image. Fictional adult only, not based on any living person.
Preserve: face identity, dark-brown short spiked hair, brown beard, extreme muscular build, body proportions, clothing, sweat/damp clothing condition.
Do not slim him. Do not make him younger. Do not make him a pretty-boy. Do not change body proportions.
He speaks directly to the viewer. Voice: low, mature Japanese male, natural conversational delivery.

SCENE LOCK:
The scene remains exactly the same as the reference image. Same architecture, background, lighting, time of day, atmosphere, color palette.
Do not introduce or remove people. Do not add new objects. Do not change the location.

CAMERA CONTINUITY:
Maintain a single continuous shot with no cuts or transitions.
Keep the original camera angle, lens perspective, composition, and background layout.
The camera remains locked in place.
No orbiting, panning, tilting, reframing, push-in, or dramatic zooming.
The character may perform meaningful upper-body movements while remaining in approximately the same position in the frame.
Allow the character's hands and arms to move naturally within the visible frame when required by the specified action.
If the reference is chest-up or tighter, keep every gesture inside that crop. Do not invent a full body or limbs the image does not show.
The character's body may change pose temporarily, but his identity, body proportions, and visual design must remain consistent with the reference image.
Prioritize character performance over camera movement.

MOTION PRIORITY:
The goal is to create an engaging animated character performance, not a minimally animated still image.
Preserve the character's identity and the original scene, but allow clear, intentional, emotionally motivated movements.
The character must perform the specified primary action.
Do not replace the primary action with breathing, blinking, lip movement, or other negligible micro-movements.

ACTION HIERARCHY:
1. PRIMARY ACTION: One clear, readable character action that changes the visual state and communicates the meaning of the dialogue.
2. SECONDARY ACTION: A complementary head movement, gaze shift, facial expression, or upper-body movement that supports the primary action.
3. CONTINUOUS MICRO-MOTION: Natural breathing, blinking, subtle eye movement, and small facial changes throughout the shot.

MOVEMENT DESIGN:
Every major dialogue beat should produce a visible change in the character's expression, gaze, posture, or hand position.
Use deliberate, smooth, anatomically coherent movements.
Actions should develop progressively rather than occurring randomly.
Allow moderate head movement, shoulder rotation, small upper-body posture changes, and natural arm gestures.
When explicitly specified, allow the character to raise one hand, extend one arm toward the viewer, or make a clear beckoning gesture.
The character may briefly shift his gaze away from the viewer and then return to direct eye contact.
Avoid repetitive idle animation.
Do not keep the character in exactly the same pose for the entire video.
Do not introduce unrelated gestures or excessive movement.
Avoid abrupt pose changes, exaggerated body deformation, extra fingers, distorted hands, or inconsistent anatomy.
Do not walk out of frame, turn fully away, change clothes, change location, or leave his place in the scene.
The character must complete the specified action and settle into the intended final pose.
```

#### 动作方案（写复制块之前先定，不要每条都伸手）

读成图再选动作。每条视频 **一个主动作 + 一个辅助动作**。主动作必须改变画面，并且有开始、发展、收势。呼吸、眨眼、口型全程都有，但不能代替主动作。

先看构图：脸部特写或手不在画里 → 只用 A01 / A04 / A08。手和前臂在画里 → 才可以用 A02 / A03 / A05 / A07。不要要求模型长出原图没有的身体。

| 编号 | 主动作 | 辅助 | 适用 | 难度 |
|------|--------|------|------|------|
| A01 | 低头，再抬眼看观众 | 轻皱眉 | 冷、压、责问 | 低 |
| A02 | 向观众伸出一只手，掌心向上 | 头微侧 | 邀请、关心 | 中 |
| A03 | 轻轻招手，示意靠近 | 眼神变柔 | 亲密 | 中 |
| A04 | 肩膀慢转，回头看观众 | 短暂停 | 警觉 | 中 |
| A05 | 抬手整理衣领 | 低头后再抬眼 | 自信 | 中 |
| A06 | 双臂交叉，再微微低头 | 眉和目光变化 | 克制、冷 | 中 |
| A07 | 手伸向画面前方后停住 | 目光跟着手动 | 强互动 | 中高 |
| A08 | 先看远处，再回看观众 | 轻皱眉 | 悬念、关心 | 低到中 |

优先 A01、A02、A03、A08。同一结构可以换台词和时机，不要每条都是伸手邀请。手容易变形时，把 A02/A03/A07 降成 A01 或 A08。

禁止写成主动作：走开、背对观众转走、换衣服、摸胸、抓握、靠近到贴身。这些会漂脸、漂衣服，也容易被模型拒。

情绪跟台词走，不要套死「发现 → 关心 → 伸手」。责问用 A01，教学用抬眼或整理衣领，关怀邀请才用 A02/A03。

#### ACTION PLAN + ACTION TIMELINE + DIALOGUE + END STATE（单段 C2）

`{room}` = 成图里的环境音，如 `quiet office corridor, distant HVAC`。

三句默认窗口是 2.0 / 4.5 / 7.0，主动作放在意思最重的那一句（常常是最后一句），约 8.5s 进入收势。两句用 2.0 / 5.5，收势从 8.5s 起。窗口可以按句长挪，但第一条仍在 **2.0s**，而且每一句都要有看得见的变化。0–2s 不是只呼吸：做一个注意力变化（看向镜头或转开再回来）。

```text
ACTION PLAN:
PRIMARY ACTION:
{one sentence: the A0x action, readable, stays inside the frame}
SECONDARY ACTION:
{one sentence: head, gaze, or expression}
EMOTIONAL PROGRESSION:
{beat} → {beat} → {beat}
FINAL POSE:
{the pose held for the last 1.5 seconds}

ACTION TIMELINE:
0.0-2.0s — ATTENTION
Begin from the exact reference pose.
{visible gaze or head change}. Natural breathing continues.
Do not remain on breathing and blinking alone.
The first spoken line has not started.

2.0-4.5s — {BEAT}
Dialogue:
"{kana line 1}"
{visible change in expression, gaze, or posture. This may start the secondary action.}

4.5-7.0s — {BEAT}
Dialogue:
"{kana line 2}"
{a different visible change. Do not repeat the previous beat.}

7.0-8.5s — {BEAT}
Dialogue:
"{kana line 3}"
{the primary action develops and becomes clearly readable.}

8.5-10.0s — HOLD
The character maintains FINAL POSE.
He keeps the specified eye contact and shows the last emotional change.
Natural breathing and one small blink are allowed.
The pose remains stable without freezing completely.
No new action begins during the final hold.
Mouth closes after the final word.

DIALOGUE CONTINUITY:
Speak ONLY the provided lines. Do not improvise. Do not add narration. Do not repeat extra lines.
Japanese speech only. Hiragana/katakana only (no kanji). Lip-sync the quotes.
No English. No Chinese. No on-screen text, subtitles, captions, logos, or watermarks.

DIALOGUE:
"{kana line 1}"
"{kana line 2}"
"{kana line 3}"

AUDIO:
No background music. Room tone: {room}. Natural breathing. Subtle shirt fabric. No extra footsteps unless the reference pose already implies a step.

END STATE:
The final 1.5 seconds hold FINAL POSE: a meaningful, stable pose, not a return to a motionless still and not a cinematic ending.
Same camera, lighting, identity, clothing design, and place in the frame.
Natural breathing and one blink. No fade, no freeze-frame, no camera reset, no new gesture.

FINAL CONSTRAINTS:
Anime only. Preserve identity, clothing design, location, lighting, body proportions, and the locked camera.
Perform the specified primary action and settle into FINAL POSE.
No photorealism. No new dialogue.
```

台词规则、弧目录：见 [formula.md](formula.md)。示例：见 [examples.md](examples.md)。

---

## Turn C2-S — 长台词：N 条独立 10s（看起来像连续瞬间）

用户给的日语/英语 **超过一条 10s 容量** 时走这里。只写提示词，**不要** GenerateImage。

工作流是 **图→独立 10s→截最后一帧当下一张图**，不是「生成一条 40s 再切片」：

```text
静帧 → Video1 10s
         ↓ 截最后一帧
图2   → Video2 10s
         ↓
图3   → Video3 10s
```

每段都是 **独立生成**，但必须看起来像 **同一场景的连续瞬间**。BASE 各段相同；每段换自己的 CLIP STATE、ACTION PLAN、台词和收势。下一段从上一段的收势接着演，不要演回原静帧。

### 拆段

1. 按上面「用户给的日语 / 英语台词」转假名、切成一口气
2. **每 3 句 = 1 条 10s**。余 1–2 句单独最后一条
3. 先贴 **【分镜表】**，再贴 **N 个完整复制块**（每块 = BASE + 该段 CLIP STATE + ACTION PLAN + ACTION TIMELINE + DIALOGUE + END STATE）
4. 保存 `outputs/drafts/tagame_video_<task_id>.json`（`clips`）和 `_01.txt` … `_0N.txt`
5. `douyin-caption` **整条系列写一次**（第 1 段 3 句当教学钩）

### 连贯（硬性）

| 项 | 规则 |
|----|------|
| 第 1 段上传 | **原静帧** = 身份、场景和起始姿态 |
| 第 2 段起上传 | **上一段最后一帧** = 新的起始状态（不要再上传原静帧） |
| 文字 vs 图 | 身份、服装设计、场景、光、机位以当前图为准。姿态从该图出发，按本段主动作变化 |
| 身份/服装/场景/光 | 锁在 **当前上传图**，不换景、不换装、不增人 |
| 姿态 | 每段一个主动作，停在该段收势。禁止走开、背对转走、摸胸、抓握 |
| 镜头 | **机位锁定在当前参考图**。禁止推近、拉远、环绕、重新发现走廊。人物仍在画面里差不多同一位置 |
| 开口 | 每段第一句仍 **2.0s**。0–2s 从 **当前图** 做注意力变化，不要回到更早的静帧 |
| 段尾 | 最后约 1.5 秒停在 **本段收势**（有意义的稳定姿态）。不要 fade、不要定格、不要演回开头。这一帧就是下一段的起始图 |
| 台词 | 每段只说 **本段句子**。禁止即兴、禁止把上一段再念一遍、禁止旁白 |

### 回复模板

```text
✅ Tagame 长台词 → {N} 条独立 10秒（同一场景的连续瞬间，动漫画风）

【用法】
1. 第1段：上传原成图 → 粘贴复制块 1 → 10s / 9:16
2. 第2段起：截上一段 **最后一帧** 当新图 → 粘贴对应块
不要每段都重新上传原静帧。不要理解成一条长视频的切片。

【读图】{地点 · 服装 · 姿态一句话}

【分镜表】
第1/{N}  参考图：原静帧  → 主动作：{A0x}  → 收势：{停住的姿态，可截}
  2.0s 「{kana}」  {中文}
  4.5s 「{kana}」  {中文}
  7.0s 「{kana}」  {中文}
第2/{N}  参考图：第1段收势  → 主动作：{另一 A0x，不要重复上一段}  → 收势：{…}
  …
第{N}/{N}  参考图：上一段收势  → 主动作：{…}  → 收势：停住，不要电影结尾

【字幕】模型里不要烧字；发布时叠日文+中文。

【复制到模型 · 第 1/{N} 段】
```

（一个 `text` fence = 完整英文块）然后第 2…N 段各一块。

然后接 `douyin-caption`。

结尾：`改法直接说，例如：某句改温柔、两段并一段、这一段不要伸手。`

### 每段只改这些（BASE 原样粘上）

**CLIP STATE · 第 1 段**

```text
CLIP STATE:
This clip is generated independently from the uploaded reference image (the original still).
It is one segment in a multi-clip sequence. Do not treat this as a slice of a longer video.
Begin from this exact pose, then perform only this clip's specified primary action.
Do not invent a new outfit, lighting, location, or character design.
```

**CLIP STATE · 第 2 段起**

```text
CLIP STATE:
This clip is generated independently from the uploaded reference image.
The uploaded image is the last frame of the previous independently generated clip — it is now the initial state.
Begin from this exact pose, camera, clothing, and lighting, then perform this clip's specified primary action.
Do not rewind to an earlier still. Do not reset the scene. Do not restart the conversation.
Do not change outfit, lighting, or background.
```

**SERIES CONTINUITY（每段都加，不要写 Clip i of n 长镜头）**

```text
SERIES CONTINUITY:
Each 10-second clip is generated independently from its own reference image, but all clips must look like consecutive moments of ONE continuous scene.
Maintain: same character, face, hairstyle, beard, body proportions, clothing, clothing condition, sweat/dampness, environment, lighting, visual style, camera language.
Pose may change during the clip according to this clip's action plan. Do not reset the scene at the beginning of the clip.
```

**ACTION PLAN / ACTION TIMELINE** 与单段 C2 同一结构，但每段换自己的主动作和收势。第 2 段起第一句仍 2.0s；0–2s 写 `Begin from the exact pose in the uploaded image`，不要写回原静帧。不要把上一段的主动作再做一遍。

**DIALOGUE CONTINUITY（每段都加）**

```text
DIALOGUE CONTINUITY:
The lines are part of one continuous conversation across separately generated clips.
Speak ONLY the lines listed in this clip. Do not improvise. Do not add narration. Do not repeat lines from previous clips.
Natural pauses are allowed. The last phrase should end naturally, leaving a short breathing pause.
```

**END STATE · 非最后一段**

```text
END STATE:
The final 1.5 seconds hold this clip's FINAL POSE — a meaningful, stable pose, not a return to the opening still and not a cinematic ending.
Same camera, lighting, identity, and clothing design.
Natural breathing and one blink. Mouth closes after the last word.
No fade, freeze-frame, or camera reset. No new action begins during the hold.
The final frame must be easy to use as the reference image of the next 10-second clip.
```

**END STATE · 最后一段**：同上，但最后一句改成 `Do not create a cinematic ending. A short living hold on FINAL POSE is enough.`（仍不要 fade / 定格）。

**DIALOGUE** 只列 **本段** 假名，不要写成 `Tagame says:`（以图里的人为准）。

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
  "aspect_ratio": "9:16",
  "art_style": "japanese_anime",
  "arc": "overtime_blame",
  "first_line_at_sec": 2.0,
  "action_plan": {
    "primary_id": "A01",
    "primary": "lower the head, then raise the eyes to the viewer",
    "secondary": "a slight frown on the second line",
    "emotion": "notice → blame → look here",
    "final_pose": "eyes locked on the viewer, head slightly raised"
  },
  "dialogue": [
    { "who": "tagame", "kana": "こんなじかんまで、のこってたのか", "zh": "都这时候了，你还留着？", "at_sec": 2.0 },
    { "who": "tagame", "kana": "おまえのせいだ、かえれなくなる", "zh": "都是你的错，我回不去了", "at_sec": 4.5 },
    { "who": "tagame", "kana": "ほら、こっちをみろ", "zh": "喂，看这边", "at_sec": 7.0 }
  ]
}
```

`task_id`：`{YYYYMMDD}_{scene}`；视频加 `_v`。多段加 `_v1` `_v2`。不要再写死 `"formula": ["invite", "body_heat", "possession"]`。

多段长台词（C2-S）在同一 JSON 里用 `clips`：

```json
{
  "task_id": "20260918_office_corridor_v",
  "source_image": "outputs/approved/tagame_20260918_office_corridor.png",
  "series": true,
  "clip_count": 2,
  "aspect_ratio": "9:16",
  "art_style": "japanese_anime",
  "continuity": "independent_clips_last_frame_as_next_ref",
  "prompt_layers": ["base", "clip_state", "action_plan", "timeline", "dialogue", "end_state"],
  "clips": [
    {
      "clip": 1,
      "source": "original_still",
      "action_plan": { "primary_id": "A01", "final_pose": "eyes on the viewer" },
      "end_pose": "held final pose of this clip, ready to crop as next ref",
      "dialogue": [
        { "kana": "…", "zh": "…", "en": null, "at_sec": 2.0 }
      ]
    },
    {
      "clip": 2,
      "source": "last_frame_of_clip_1",
      "start_pose": "matches clip 1 end_pose",
      "end_pose": "short hold on face and chest",
      "dialogue": [
        { "kana": "…", "zh": "…", "en": "original English if any", "at_sec": 2.0 }
      ]
    }
  ]
}
```

---

## 路由

| 用户说了 | 走 |
|----------|-----|
| @Tagame / 田龟式肌肉上司 / docs/anime.md | **本 skill**。无用户图 + 已给台词 → **直接 B 出图** 再 C2/C2-S。画风默认日系 |
| 大野健一 / Tagame-patrol / docs/patorl-tagame.md / 场站巡逻 | **`tagame-patrol`**。视频词仍回本 skill C2 / C2-S |
| 限定风格 CuteGuysArt / 风格 CuteGuysArt | **本 skill**，`art_style: cuteguysart`。静帧和 i2v 都用 CuteGuysArt 块。人、胡茬、深棕短发、衣服不脱仍锁 Tagame |
| 无成图、无台词、只点名 | 本 skill **A**（场景卡 STOP） |
| 已有 Tagame 成图 + 图生视频 | 本 skill **C1**（先选项） |
| 已选台词编号 / 已贴 **短** 日语或英语（≤3 句） | 本 skill **C2** + `douyin-caption` |
| 已贴 **较长** 日语或英语台词 | 本 skill **C2-S**（N 条独立 10s，最后一帧当下一段参考图）+ `douyin-caption` |
| 抖音文案 / 猛男日语教学 / 抖音标题标签 | `douyin-caption`（台词须已选定） |
| @Teo / @Kai / 换脸照片 | `virtual-couple` 或 `text-scene`，**不要**本 skill |
| Teo/Kai 成图 + 图生视频 | `gemini-video`（写实） |
