---
name: tagame-patrol
description: >-
  Occupation series for 大野健一 (Ohno Kenichi), the night bus-depot dispatcher
  and security patrol. Locks face and uniform to characters/Tagame-patrol and
  keeps every scene and every spoken line on the depot job storyline
  《深夜场站的10秒私语》. Video prompts stay the tagame-anime 10s i2v
  (C2 / C2-S): one primary action per clip, kana, independent clips. Use when the user
  mentions Tagame-patrol, characters/Tagame-patrol, docs/patorl-tagame.md,
  大野健一, Ohno Kenichi, 场站, 巡逻员, 调度员, 深夜巴士, 职业线, or a
  patrol series. Do not use the office Tagame face or office scenes.
---

# Tagame Patrol — 职业故事线 → 静帧 → 台词 → 原样 10s i2v

角色是 **大野健一**，不是办公室肌肉上司。人设、服装、八集目录：[storyline.md](storyline.md)。设定原文：`docs/patorl-tagame.md`。

**视频提示词结构不另写一套。** 台词选定后，打开 `.cursor/skills/tagame-anime/SKILL.md` 的 **Turn C2**（短）或 **Turn C2-S**（长），按那里的 BASE、ACTION PLAN、ACTION TIMELINE、DIALOGUE、END STATE、CLIP STATE 写。第一条仍 **2.0s**。每段一个跟本集台词对应的主动作，参考图只是起始姿态。长台词拆成多条独立 10s，第 2 段起用上一段最后一帧。不要改成办公室流程，也不要改成 `gemini-video`。不要退回「只呼吸眨眼」。

本轨只改两件事：**场景**和**台词**必须是深夜巴士场站的职业故事。

不要走 `virtual-couple` / `text-scene` / `pose-series` / `gemini-video`。不要用 `characters/Tagame/references/face_01.jpeg`。

| Mode | 用户说了 | 做 | 禁止 |
|------|----------|----|------|
| **S1 系列菜单** | 只丢设定 / 要系列 / 没点集数、没说生成 | 贴八集目录 → STOP | GenerateImage、i2v |
| **B 静帧** | 点了集数，或说生成某一职业场景 | 每一集一张静帧 | 办公室、写实、设定表排版 |
| **C1 台词** | 已有该集静帧，用户没锁台词 | 先读图 → 5 组 **职业**台词 → STOP | 办公室台词、i2v |
| **C2 / C2-S** | 选定编号，或「用设定台词」，或自带日/英且能落在本集职业动作上 | 走 `tagame-anime` C2 或 C2-S 的当前动作方案 | 另写一套微动白名单、GenerateImage |

点名集数 = 场景已确认，不要再出服装选项，不要等场景卡。  
「用设定台词」= 用 [storyline.md](storyline.md) 该集例句，跳过 C1。  
用户贴的日/英台词：能放进本集职业动作就用（英译日、日转假名）；情节离开场站职业，就改口到本集动作上，不改成办公室上司。

---

## 身份与参考图

1. 读 [storyline.md](storyline.md)
2. 读 `characters/Tagame-patrol/detail_char.jpeg`（只核对，不上传）
3. 出图参考 **只有** `characters/Tagame-patrol/full_body_char.jpeg`

身份句：

```text
Ohno Kenichi, 32, night bus-depot dispatcher and security patrol. Match the attached full-body reference: East Asian man, square jaw, short dark-brown spiky hair, neat stubble, thick brows, confident half-smile, extremely muscular. Navy leather bomber, tight white shirt, burgundy tie, black belt, black trousers, black oxfords. High-quality Japanese anime / digital illustration. NOT photorealistic. NOT the office superior. NOT the character-sheet layout.
```

画风默认日系动漫，与参考图一致。用户点名 CuteGuysArt 时，只换 `.cursor/skills/cuteguysart/SKILL.md` 的画风段，人、制服、场站、职业台词不变。

衣服留在身上。可敞开夹克、解开一颗扣、松开领带。不要裸体。

---

## S1 — 系列菜单

只点设定、要一系列、没点集数：把 [storyline.md](storyline.md) 八集压成下面的回复，然后 **STOP**。

```text
✅ 大野健一 ·《深夜场站的10秒私语》
职业：深夜巴士场站调度员 / 夜班巡逻员。制服锁定藏青夹克 + 白衬衫 + 酒红领带。

1️⃣ last_train 末班已过 · 关怀 · 候车椅、关掉手电
2️⃣ sweep 手电照到你 · 巡逻 · 夜间停车场
3️⃣ confiscate 抽走烟 · 管束
4️⃣ radio 别进车道 · 调度对讲
5️⃣ summer_heat 夏夜值班 · 松领带
6️⃣ timetable 核对时刻表 · 好教
7️⃣ dawn_coffee 清晨交接 · 递咖啡
8️⃣ escort 送到站外 · 披夹克

回复集数。例如：`生成 1` / `1,3,7 用设定台词` / `先出 2 和 4 的图`。
没写「用设定台词」时，出图后先给 5 组职业台词，再写视频词。
视频词与办公室 Tagame 的 10 秒规则相同。

⏸️ 请点集数后再出图。
```

---

## B — 静帧

每一集一张。`aspect_ratio` `3:4`。参考图只有全身设定。灰底和设定表不要画进去。

```json
namespace: "cursor"
toolName: "GenerateImage"
arguments: {
  "description": "<prompt>",
  "filename": "patrol_<episode_id>.png",
  "aspect_ratio": "3:4",
  "reference_image_paths": ["characters/Tagame-patrol/full_body_char.jpeg"]
}
```

系列目录：`outputs/approved/series/patrol_<YYYYMMDD>/0N_<episode_id>.png`  
只出一集、用户没说系列：`outputs/approved/patrol_<episode_id>.png`

一次点了多集：按集数顺序各出一张。用户没锁台词就先别写 i2v。

### 静帧 prompt

```text
[ART STYLE]
High-quality Japanese anime / modern digital illustration. Clean linework, refined cel-shaded lighting, bara muscular aesthetic. NOT photorealistic. NOT live-action. NOT 3D CGI. Match the attached character reference for face, hair, beard, and uniform only.

[CHARACTER]
Only one person: Ohno Kenichi, 32. {identity sentence}
Do not slim him. Do not use the office-superior face. Do not reproduce the model sheet, labels, extra heads, or the line-art sketches.

[SCENE]
{this episode's depot place and job action from storyline.md}. Night bus depot or dawn shift change. Props only if this episode uses them: flashlight, radio, cigarette and lighter, coffee, timetable.

[COMPOSITION]
Vertical 3:4. Medium-close, slight low angle. Face in the upper two-thirds. He looks at the camera and speaks to the viewer. First frame already shows the job action.

[POSE]
{episode pose}. The signature prop action is already in this still. Shirt stays on.

[CLOTHING]
Navy bomber, tight white shirt, burgundy tie, black trousers, black belt, black shoes. Jacket may be open. Tie may be loosened. No nudity. No costume change.

[LIGHTING]
Night depot: practical lamps, sodium, or flashlight. Dawn episodes: dim blue morning. Real exposure. Do not brighten into glow.

[CONSTRAINTS]
One adult man. No text, watermark, subtitles, or character-sheet graphics. No Teo, no Kai, no office corridor.
```

### QC

| 失败 | 原因 |
|------|------|
| 人 | 不像全身参考：没胡茬、发色错、画瘦、画成办公室那张脸 |
| 景 | 办公室、健身房、酒店、灰底设定表、多头像 |
| 职 | 看不出本集职业动作 |
| 衣 | 制服被换成别的衣服，或衬衫脱掉 |
| 画 | 像照片 |

不过关最多重出 1 次。通过后：用户已锁台词 → 同一回合 C2 / C2-S。否则 C1。

---

## C1 — 5 组职业台词

先读这一集的成图，再写。5 组都是 **这一张图里的场站职业**，风格互相不同：

1. 深夜关怀
2. 管束（车道 / 烟 / 滞留）
3. 反差（仍在值班）
4. 交接或护送
5. 职业口语 · 好教（終電、巡回、無線、遅番 里至少点明一个）

每句都要吃进本图：有手电才说照到你，有对讲才说无线，候车椅才说末班。禁止加班走廊、更衣室、酒店、背书。

保存 `outputs/drafts/patrol_lines_<episode_id>.json`，`"user_confirmed": false`。

```text
✅ 职业台词（大野健一 · {集名} · 先读成图）

【读图】
地点：{场站何处}
职业动作：{巡逻 / 调度 / 交接 / …}
姿态 / 道具：{…}
本图能说：{他为什么现在开口}

【谁】大野健一，对镜头（お前）——场站夜班，外表凶，只对你软

1️⃣ 【关怀】…
1 {kana} ｜ {中文}  （{语法钩}）
2 …
3 …

2️⃣ 【管束】…
3️⃣ 【反差】…
4️⃣ 【交接】…
5️⃣ 【职业口语 · 好教】…

回复编号，或「用设定台词」。
⏸️ 选定后再写 10 秒视频词（规则与 tagame-anime 相同）。
```

**STOP。不要输出英文 i2v 块。**

---

## C2 / C2-S — 视频词（用 tagame-anime 当前模板）

1. 读 `.cursor/skills/tagame-anime/SKILL.md` 的 Turn C2 与 C2-S，按那里写复制块。
2. 约 3 句、总拍数 ≤ 42 → 一条 C2。更长 → C2-S。
3. 假名。模型只说日语。第一条 2.0s。
4. 允许的替换只有这些：
   - 文件名前缀 `patrol_`：`outputs/drafts/patrol_video_<episode_id>.txt`（多段 `_01`…）
   - JSON 增加 `"character": "ohno_kenichi"`、`"episode_id"`、`"job_action"`
   - `AUDIO` 的 room tone 写成成图里的场站声：夜班停车场、远处巴士、无线杂音、清晨交接。不要写成 office corridor
5. 不要改 FORMAT、身份/场景锁、机位锁定、禁 `Clip 1 of N`。主动作按当前 `tagame-anime` 动作库选，不要退回只允许呼吸眨眼。
6. 静帧里已经做完的点烟、挥手电、披夹克不要在视频里再演一遍。主动作是从这张图出发的下一段表演。
7. 同一回合按 `douyin-caption` 的结构写文案。账号写成 **二次元猛男说日语**。正文场景用场站 / 末班 / 巡逻，不要写成加班上司。一集一条。用户说先不要文案则跳过。

系列里每一集是独立成片（自己的静帧、自己的 10 秒）。只有 **同一集台词超长** 才用 C2-S 的「最后一帧接下一截」。不要把第 2 集接到第 1 集的最后一帧上。

---

## 路由

| 用户说了 | 走 |
|----------|-----|
| Tagame-patrol / 大野健一 / `docs/patorl-tagame.md` / 场站巡逻系列 | **本 skill** |
| 只丢设定、没点集 | **S1** STOP |
| `生成 1` / `1,4` | **B**，然后 **C1** |
| `1,3 用设定台词` | **B** 然后 **C2** |
| 已有巡逻成图 + 要视频、没台词 | **C1** |
| 选定台词或短日/英 | `tagame-anime` **C2** + 抖音文案 |
| 较长日/英 | `tagame-anime` **C2-S** |
| @Tagame / `characters/Tagame` / `docs/anime.md` / 办公室 | `tagame-anime`，不要本 skill |
