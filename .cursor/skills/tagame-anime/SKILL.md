---
name: tagame-anime
description: >-
  Tagame anime pipeline: if the user has no scene still, generate one
  Japanese-anime image from the Tagame face reference to match the dialogue
  scene. Then either (a) post 5 diverse Japanese dialogue options, or (b) use
  user-supplied Japanese/English lines. Long scripts split into multiple 10s
  i2v clips. After the video prompt, run douyin-caption (账号：猛男日语教学).
  Use when the user mentions Tagame, @Tagame, characters/Tagame, docs/anime.md,
  动漫画风, 办公室肌肉上司, or asks for Tagame 场景图 / 图生视频 / 10秒视频.
  Never photoreal; never Teo/Kai couple pipeline.
---

# Tagame Anime — Bible Still → 台词选项 → 10s i2v

固定角色 **Tagame**（办公室肌肉上司）。画风 **永远是高品质日系动漫**，禁止写实。

先按 Character Bible 补全场景。静帧通过后：

- **没给台词** → **先读成图/场景卡**，再给 **5 组不同风格**日语台词，等用户选一组，再写 10s 图生视频提示词。
- **用户已给日语或英语台词** → **跳过 C1**，用用户原文（英译日、日转假名）。**一句/三句塞进一条 10s**；**较长则按长度拆成多条独立 10s**（每段用自己的参考图生成，看起来像同一场景的连续瞬间）。姿态微动、镜头几乎不动；第 2 段起上传上一段最后一帧，不要每段回到原静帧，也不要每段都往前推镜头。

**没有用户参考图 / 成图时：** 不要干等场景卡。用 Tagame 脸图 `characters/Tagame/references/face_01.jpeg` **直接出一张**符合 **台词场景** 的动漫静帧（没台词才用办公室默认）。禁止向用户再要一张真人场景照。

不要默认套「邀请 → 身体热度 → 占有」。

公式与台词库：[formula.md](formula.md)。发布文案（抖音 / 猛男日语教学）：`douyin-caption`。

本 skill **不要**走 `virtual-couple` / `text-scene` / `pose-series` / `gemini-video`（那些是 Teo/Kai 写实线）。

| Mode | Input | Do | Forbidden |
|------|--------|-----|-----------|
| **A 场景卡** | 只 @Tagame / 要新场景，**没台词、没说出图** | 填场景卡 → STOP | GenerateImage |
| **B 出图** | `生成` / 出图，或 **无用户图且已有台词** | GenerateImage **一张**（脸图=Tagame 参考图；场景跟台词走） | 写实、向用户再要场景照 |
| **C1 台词** | 已有 Tagame 成图，**且用户没贴台词** | **先读图** → 贴 **5 组**不同风格台词 → STOP | GenerateImage、i2v 复制块、没读图就编台词 |
| **C2 视频词** | 用户回复编号 / 选定短台词 | 写 **一条** 10s i2v 复制块 → 跑 `douyin-caption` | GenerateImage |
| **C2-S 长台词** | 用户贴的日语或英语 **超过一条 10s**（约 >3 句） | 转假名；拆成 **N 条独立 10s**；**同一套 BASE** + 每段只改 CLIP STATE / 台词 / 片尾 | GenerateImage、写成「一段 40s 的第 N 截」、每段大动作/猛推镜头 |

**无用户参考图 + 已给台词：** 跳过 A 的 STOP，本回合按台词场景出静帧，再进 C2 / C2-S。  
**无用户参考图 + 用户说生成/出图（没台词）：** 跳过 A 的 STOP，办公室默认出静帧，再进 C1。  
只 @Tagame、没台词、没说出图：仍走 A。  
已有成图 + 只要视频词、**没贴台词**：跳过 A/B，**仍要跑 C1**。  
已有成图 + 用户已给日语/英语台词或选了编号：跳过 C1，只跑 C2（短）或 C2-S（长）。

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

Identity prompt（**出静帧**用。图生视频不要靠这段点名，用上传图 + CHARACTER LOCK）：

```text
Tagame: mature East Asian man ~40, square jaw, dark-brown short slightly wavy spiked hair swept up, neat brown stubble/beard, thick angled brows, confident half-smile, extremely muscular (broad shoulders, full chest, thick arms, narrow waist). High-quality Japanese anime / digital illustration, clean linework, not photorealistic. Match the attached character reference exactly.
```

---

## Turn A — 场景卡（仅「只点名、还不出图」）

**无用户参考图且（已给台词 或 已说生成/出图）→ 跳过本回合，直接 Turn B。**

只 @Tagame / 要新场景、还没台词、也没说出图时：用 Bible 填缺口。用户原文覆盖默认值；**不能**改画风、削肌肉、换脸。

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
High-quality Japanese anime / modern digital illustration. Clean linework, refined cel-shaded lighting, bara muscular aesthetic. NOT photorealistic. NOT live-action. NOT 3D CGI. NOT a real photograph. Match the attached anime character reference.

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

1. 把选定弧写入 JSON，`"user_confirmed": true`；三条台词进 `dialogue`
2. 第一条台词 **2.0s** 开口。动作只用 **呼吸 / 眨眼 / 口型 / 极小转头**，姿态锁定上传图。不要写摸胸、走近、甩手、走路（即使用户选了经典 A）
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
6. 2 句也能成一条（2.0 / 5.5）。1 句且很短：仍一条 10s，后半段靠近+停住，不要硬凑废话

### 回复模板

```text
✅ Tagame 10秒图生视频提示词（身份/服装/场景锁定成图，动漫画风，只加动作和声音）

【用法】打开 Gemini（或你的 i2v）→ 上传这张成图 → 粘贴下面英文块 → 时长 10s / **9:16** 竖屏

【谁】仅 Tagame，对镜头（お前）
【情绪弧】{用户选的弧名}（不是默认邀请→占有，除非选了那一组）
【微动】姿态锁定成图；只呼吸/眨眼/口型，不写大动作或猛推镜头
【台词】第一条 @2.0s
Tagame：「{kana}」  {中文}
Tagame：「{kana}」  {中文}
Tagame：「{kana}」  {中文}

【字幕】模型里不要烧字；发布时叠日文+中文。

【复制到模型】
```

（此处一个 `text` 代码块 = 英文提示词）

然后接 `douyin-caption` 的发布复制块。

结尾：`改法直接说，例如：换第4组台词、强度改温柔、不要湿、动作再小一点。`

### i2v 复制块结构（C2 与 C2-S 共用）

设计说明：`docs/modify_prompt.md`。**优先级：图片一致 > 人物 > 场景 > 微动连续 > 镜头连续 > 台词连续。** 不要为了表演写大动作。

每段复制块按这 10 层写，**删掉重复的 ANIME / 不要 fade / 不要 cut**。单段 C2 用 BASE + TIMELINE + DIALOGUE + END STATE（单段收束）。长台词 C2-S 用同一套 BASE，每段只改 CLIP STATE / TIMELINE / DIALOGUE / END STATE。

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
The uploaded image is the PRIMARY VISUAL SOURCE OF TRUTH.
Follow it exactly for: character appearance, face, hair, beard, body proportions, musculature, clothing, clothing position, pose, hand position, facial expression, background, architecture, lighting, shadows, color palette, camera angle, framing.
Do not redesign, reinterpret, beautify, or regenerate these elements.
If any textual instruction conflicts with the reference image, PRIORITIZE THE REFERENCE IMAGE.

ART STYLE LOCK:
Preserve the exact high-quality Japanese anime / digital illustration style of the reference image.
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
Preserve the exact camera angle and initial framing of the reference image.
Camera movement is extremely subtle. Only a very slow micro push-in is allowed.
The character must remain approximately the same size in frame.
Do not zoom out, whip-pan, orbit, tilt dramatically, change height, change lens perspective, reveal a new area, or reframe the character.

MOTION PRIORITY:
Natural micro-motion is more important than large movements.
The character remains mostly in the same pose as the reference image.
Allowed: subtle breathing, chest rise, blinking, tiny facial movement, small eye movement, subtle head movement, very small weight shift, natural mouth movement during speech.
Avoid: large arm movements, walking, turning around, changing posture, touching the face or chest, raising/lowering arms, changing clothes, exaggerated gestures.
```

#### TIMELINE + DIALOGUE + END STATE（单段 C2）

`{room}` = 成图里的环境音，如 `quiet office corridor, distant HVAC`。

```text
TIMELINE:
0.0-2.0s: Very subtle living motion from the exact reference pose. Breathing, blinking, a small preparatory inhale. Do not stare like a frozen image.
2.0-4.5s: FIRST LINE STARTS at 2.0s. Natural mouth and eye movement toward the camera. Maintain the original body pose. No large gesture.
4.5-7.0s: Second line. Only subtle facial and head movement. No lean-in. No step closer.
7.0-9.5s: Third line. Maintain eye contact. Minimal natural movement.
9.5-10.0s: Natural living hold. Mouth closes after the final word. Continue breathing. Do not freeze. Do not create an ending pose.

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
The final 1 second stays visually stable: same body, camera, face, eye direction, lighting. Natural blink/breath. No dramatic gesture, no camera reset, no fade, no freeze-frame.

FINAL CONSTRAINTS:
Anime only. Preserve the reference image, clothing, location, lighting, body proportions, camera language. Minimal natural motion. No photorealism. No new dialogue.
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

每段都是 **独立生成**，但必须看起来像 **同一场景的连续瞬间**。BASE 各段相同；只改 CLIP STATE、本段台词、片尾状态。

### 拆段

1. 按上面「用户给的日语 / 英语台词」转假名、切成一口气
2. **每 3 句 = 1 条 10s**。余 1–2 句单独最后一条
3. 先贴 **【分镜表】**，再贴 **N 个完整复制块**（每块 = BASE + 该段 CLIP STATE + TIMELINE + DIALOGUE + END STATE）
4. 保存 `outputs/drafts/tagame_video_<task_id>.json`（`clips`）和 `_01.txt` … `_0N.txt`
5. `douyin-caption` **整条系列写一次**（第 1 段 3 句当教学钩）

### 连贯（硬性）

| 项 | 规则 |
|----|------|
| 第 1 段上传 | **原静帧** = 视觉真相 |
| 第 2 段起上传 | **上一段视频的最后一帧** = 新的视觉真相（不要再上传原静帧） |
| 文字 vs 图 | 冲突时 **以图为准** |
| 身份/服装/场景/光 | 锁在 **当前上传图**，不换景、不换装、不增人 |
| 姿态 | 几乎保持上传图姿势。禁止走路、转体、摸脸摸胸、大幅举手 |
| 镜头 | **匹配当前参考图的机位和取景**。只允许极慢微推。人物在画面里差不多一样大。禁止每段都往胸口推近、禁止拉远、禁止重新发现走廊 |
| 开口 | 每段第一句仍 **2.0s**。第 2 段起 0–2s 从 **当前图姿势** 活过来，不要回到原静帧 |
| 段尾 | 最后 1 秒是 **还没结束的中间帧**（呼吸、眨眼、嘴刚合上）。不要写成结尾、不要 fade、不要定格。方便截帧当下一张图 |
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
第1/{N}  参考图：原静帧  → 片尾：同一姿势的中间帧（可截）
  2.0s 「{kana}」  {中文}
  4.5s 「{kana}」  {中文}
  7.0s 「{kana}」  {中文}
第2/{N}  参考图：第1段最后一帧  → 片尾：仍是中间帧
  …
第{N}/{N}  参考图：上一段最后一帧  → 片尾：活着停住，仍不要电影结尾

【字幕】模型里不要烧字；发布时叠日文+中文。

【复制到模型 · 第 1/{N} 段】
```

（一个 `text` fence = 完整英文块）然后第 2…N 段各一块。

然后接 `douyin-caption`。

结尾：`改法直接说，例如：某句改温柔、两段并一段、动作再小一点。`

### 每段只改这些（BASE 原样粘上）

**CLIP STATE · 第 1 段**

```text
CLIP STATE:
This clip is generated independently from the uploaded reference image (the original still).
It is one segment in a multi-clip sequence. Do not treat this as a slice of a longer video.
Establish a living, ongoing moment from this exact pose. Do not invent a new pose, outfit, lighting, or background.
```

**CLIP STATE · 第 2 段起**

```text
CLIP STATE:
This clip is generated independently from the uploaded reference image.
The uploaded image is the last frame of the previous independently generated clip — it is now the visual source of truth.
Continue from this exact pose, camera, clothing, and lighting.
Do not rewind to an earlier still. Do not reset the scene. Do not restart the conversation. Do not introduce a new pose, outfit, lighting, or background.
```

**SERIES CONTINUITY（每段都加，不要写 Clip i of n 长镜头）**

```text
SERIES CONTINUITY:
Each 10-second clip is generated independently from its own reference image, but all clips must look like consecutive moments of ONE continuous scene.
Maintain: same character, face, hairstyle, beard, body proportions, clothing, clothing condition, sweat/dampness, environment, lighting, visual style, camera language.
Do not reset the scene at the beginning of the clip.
```

**TIMELINE** 与单段 C2 相同（微动 + 口型）。第 2 段起第一句仍 2.0s；0–2s 写 `from the exact pose in the uploaded image`，不要写回原静帧。

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
The final 1 second must look like a natural intermediate moment in an ongoing scene — not an ending.
Same body position, camera, face, eye direction, lighting.
Mouth closes naturally after the last word. Continue subtle breathing and blinking.
No cinematic ending, fade, freeze-frame, pose change, or camera reset.
The final frame must be easy to use as the reference image of the next 10-second clip.
```

**END STATE · 最后一段**：同上，但最后一句改成 `Do not create a cinematic ending. A short living hold is enough.`（仍不要 fade / 定格）。

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
  "prompt_layers": ["base", "clip_state", "timeline", "dialogue", "end_state"],
  "clips": [
    {
      "clip": 1,
      "source": "original_still",
      "end_pose": "intermediate living hold, same pose, ready to crop as next ref",
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
| @Tagame / 田龟式肌肉上司 / docs/anime.md | **本 skill**。无用户图 + 已给台词 → **直接 B 出图** 再 C2/C2-S |
| 无成图、无台词、只点名 | 本 skill **A**（场景卡 STOP） |
| 已有 Tagame 成图 + 图生视频 | 本 skill **C1**（先选项） |
| 已选台词编号 / 已贴 **短** 日语或英语（≤3 句） | 本 skill **C2** + `douyin-caption` |
| 已贴 **较长** 日语或英语台词 | 本 skill **C2-S**（N 条独立 10s，最后一帧当下一段参考图）+ `douyin-caption` |
| 抖音文案 / 猛男日语教学 / 抖音标题标签 | `douyin-caption`（台词须已选定） |
| @Teo / @Kai / 换脸照片 | `virtual-couple` 或 `text-scene`，**不要**本 skill |
| Teo/Kai 成图 + 图生视频 | `gemini-video`（写实） |
