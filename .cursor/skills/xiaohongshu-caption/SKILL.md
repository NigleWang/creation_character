---
name: xiaohongshu-caption
description: >-
  Writes Xiaohongshu (小红书) posting copy for photoreal stills and pose-series —
  short scene + detail + emotion, title, 30–80字 body, 6–10 hashtags. Teo/Kai
  copy uses Teo (受) and Kai (攻), with #TeoKai #TeoKaiDaily. 小川/大海 copy
  uses those names. Do not add #小川大海 #小川大海日常 #双人设 #固定角色.
  Prefer hot discovery tags such as #肌肉男 when the body reads muscular.
  Do not write 受/攻.
  Teo/Kai still mixes self-built tags with the discovery pool. Use after
  pose-series, or when the user asks for 文案, 标题, 标签, 小红书发布, caption.
---

# Xiaohongshu Caption — 发布文案

从成图写出可直接发小红书的 **标题 + 正文 + 标签**。核心：**短、有画面感、带一点情绪，像在看他们的生活片段**。

本 skill **只写文案**。不要调用 `GenerateImage`。不要走换脸 / 换姿态。

| Pipeline | Input | Output |
|----------|--------|--------|
| `pose-series` | 系列成图 | **一组一张文案**（本 skill，Turn 2 结束后必跑） |
| `virtual-couple` / `text-scene` | 单张成图 | 一张文案（用户要文案时跑） |
| **本 skill 单独** | 已有成图 + 文案/标题/标签 | 复制即发的笔记 |

源文档：`docs/code_task/文案.md`。先定 cast。Teo/Kai 文案只用 **Teo / Kai**，不要写 Tom / James。小川/大海文案只用 **小川 / 大海**，不要写成 Teo/Kai，也不要写受/攻。

---

## Names (mandatory)

| ID | 显示名 | 定位 | 文案气质 |
|----|--------|------|----------|
| `teo` | **Teo** | 受 | 软感 / 表情 + 小心思 |
| `kai` | **Kai** | 攻 | 气场 / 动作 + 小情绪 |

正文、标题、标签里，Teo/Kai 稿只出现 Teo / Kai。Tom / James 已废弃。

标签策略：**自建词 + 大池子各一半**。Teo/Kai 每条必带 `#TeoKai` `#TeoKaiDaily`。不必写 AI/虚拟，但别只用自建标签。

### 小川 / 大海

成图或用户点名是这一对时，不要用上面的受/攻表。

| ID | 显示名 | 文案气质 |
|----|--------|----------|
| `ogawa` | **小川** | 安静、表情少、干净 |
| `dahai` | **大海** | 厚实、可靠、生活感 |

标签不要用 `#小川大海` `#小川大海日常` `#双人设` `#固定角色`。身材结实或手臂很厚时，优先热门词 `#肌肉男` `#肌肉男日常` `#型男` `#壮男`，再按画面加 `#帅哥` `#氛围感男生` `#男生拍照` `#人夫感` `#日常碎片`。双人可以写一个很小的相处细节，不要披外套、耳尖红、受攻互动。单人就写那一个人正在做的事。

仅小川例：小川今天话很少，杯子放到一半又停住了。  
仅大海例：大海收工回来，衬衫袖口还卷着，先在门口把灰拍掉。  
双人例：两个人并排走，小川看着路，大海把袋子换到了另一只手。

---

## When to run

**必跑：** `pose-series` Turn 2 QC 通过、系列文件夹写好之后。一组图只出 **一条** 笔记文案。

**也跑：** 用户说 文案 / 标题 / 标签 / 小红书发布 / caption / 配文；或指着 `outputs/approved/`（含 `series/`）要发布文案。

不要在 pose-series Turn 1 写文案（图还没出）。

---

## Workflow (one shot)

1. Identify images: user @path, `outputs/approved/series/<task_id>/`, or latest approved still.
2. Read 1–3 frames (cover + one mid + last if series). Also read `outputs/drafts/look_lock_<task_id>.json` if present.
3. Resolve cast from look-lock / filename / user @. 整齐短发淡胡茬 = 小川，短须结实 = 大海，眉框眼镜圆寸 = Teo，刺发 = Kai。看不清就按文件名和用户点名，不要把小川认成 Teo。双人：Teo 左 Kai 右，或小川左大海右。
4. Write **one** note using the formula below. Series = one life fragment, **do not** list every pose.
5. Save:
   - `outputs/drafts/caption_<task_id>.json`
   - `outputs/drafts/caption_<task_id>.txt` (copy-paste body only)
6. Reply with the template. Put the publish block in **one** fenced `text` code block.

If the user already gave 标题 / 情绪 / 不要提问, honor that.

---

## 文案公式

```
1. 开头抛一个小场景/情绪（1句）
2. 加一个细节或互动（1–2句）
3. 结尾轻轻收住，或留一个小问题（可选）
```

好文案 = **一个小场景 + 一个细节 + 一点点情绪**。

| 项 | 规则 |
|----|------|
| 标题 | ≤20 字，情绪钩子，不要「1/n」 |
| 正文 | **30–80 字**（汉字计）。太长没人看 |
| 标签 | **6–10 个**，放正文最后；自建词 + 大池子各一半 |

### 进阶

1. 多用「今天」「刚才」「刚刚」，增加真实感。
2. 少用夸张词（「绝美」「神颜」「完美」），用细节。
3. 适当留白，不要把情绪写满。
4. 结尾可加一句互动，提高评论。
5. 不要写虚拟、AI、换脸、生成。不要剧透拍摄。

### 按人设选模板

**仅 Kai：** 气场/动作 + 小情绪  
例：今天的Kai有点懒，外套都懒得拉链。 / 刚运动完的Kai，耳尖还有点红。

**仅 Teo：** 软感/表情 + 小心思  
例：Teo今天好像有点困，眼睛都是水润的。 / 低头玩手机的样子，莫名很想揉他头发。

**双人：** 一个小互动 + 情绪  
例：Kai把外套披到Teo肩上，Teo嘴上说着不要，身体却没躲开。 / Kai低头说了什么，Teo耳尖瞬间红了。

互动句式参考：披外套、手搭后腰、靠肩睡着、并排不说话、耳尖红。Kai 先动、Teo 接收。

---

## 标签

每条笔记 **6–10 个**。Teo/Kai 是自建词加大池子各一半。小川/大海不用自建词，改用热门发现词。不要堆无关热搜。

### 自建词（账号沉淀，约一半）

Teo/Kai 每条必带：`#TeoKai` `#TeoKaiDaily`，再补 `#双人设` `#固定角色`。

小川/大海不要用上面这四个自建词。改用热门发现词，身材明显时先放 `#肌肉男` `#肌肉男日常` `#型男` `#壮男`。

### 大池子（按画面选，约一半）

优先从画面里挑：

`#氛围感男生` `#男生拍照` `#健身` `#人夫感` `#日常碎片`

| 画面 | 用 |
|------|----|
| 男生单人 / 氛围照 | `#氛围感男生` `#男生拍照` |
| 生活片段、碎片感 | `#日常碎片` |
| 居家、成熟、照顾感 | `#人夫感` |
| 健身、运动、肌肉、工装出力 | `#健身` |

对不上的不要硬加。还差条数时，按 cast 从下面补，仍算大池子。

| Cast | 补位 |
|------|------|
| 仅 Kai | `#帅哥` `#侧颜杀` |
| 仅 Teo | `#帅哥` `#清冷感` |
| 仅 大海 | `#帅哥` `#人夫感`（画面是居家或收工时） |
| 仅 小川 | `#帅哥` `#清冷感` |
| Teo/Kai 双人 | `#情侣日常` `#双人照` `#氛围感情侣` `#情侣拍照` |
| 小川/大海 双人 | `#双人照` `#日常碎片`。不要 `#情侣日常`，除非用户要求写成情侣 |

氛围（最多再 1 个）：`#氛围感` `#胶片感` `#日系氛围` `#生活感`

场景（0–1 个）：`#办公室` `#咖啡馆` `#居家` `#厨房` `#雨天` `#旅行` `#海边`

### 禁止

不要加 `#虚拟情侣` `#BL` `#AI`。正文也不写虚拟、AI、换脸。

---

## Reply template

Chat order:

1. 成品图 + 简短 QC（若本轮刚出图；纯文案请求可跳过）
2. 中文头：封面建议 + 谁
3. **一个** `text` fence = 标题空行正文空行标签（整段可复制）
4. 可选两句备选标题（fence 外）
5. 系列文件夹路径

```
✅ 小红书文案已写好（可直接复制发布）

【谁】{仅Teo / 仅Kai / 双人 Teo左 Kai右 / 仅小川 / 仅大海 / 双人 小川左 大海右}
【封面】系列第 {n} 张（{pose 一句话}）— 脸在画面上三分之二、情绪最清楚的那张

【复制发布】
```

Fence contents only (no 【标题】label):

```text
{标题}

{正文，2–4 短行}

{6–10 hashtags, space-separated, one line}
```

Closing: `改法直接说，例如：再甜一点、不要提问、改成只写Kai。`

---

## JSON schema

```json
{
  "task_id": "20260829_kai_office_series",
  "source": "outputs/approved/series/20260829_kai_office_series/",
  "cast": ["kai"],
  "cover_file": "01_look_camera.png",
  "title": "今天的侧颜有点犯规",
  "body": "刚开完会的Kai，袖口还挽着。\n靠回椅背的时候，下颌线突然变得很锋利。\n看久了会有点移不开眼。",
  "tags": ["#TeoKai", "#TeoKaiDaily", "#双人设", "#固定角色", "#氛围感男生", "#男生拍照", "#人夫感", "#日常碎片"],
  "alt_titles": ["刚散会的下颌线", "今天懒得拉链"]
}
```

`cast` 用 `teo` / `kai`，或 `ogawa` / `dahai`。不要用 tom/james。小川/大海不要填 `#TeoKai`，也不要填 `#小川大海` `#小川大海日常` `#双人设` `#固定角色`。

---

## Iteration

用户改甜度 / 不要提问 / 只写其中一个：

1. 改 JSON
2. 重写 `caption_<task_id>.txt`
3. 回复 **完整** 新复制块（不要只给 diff）

---

## Routing

- pose-series 出图中 → 先把图做完，再跑本 skill
- 只要文案、不要出图 → 只要本 skill
- 图生视频 → `gemini-video`，不是本 skill
- Tagame / 抖音 / 猛男日语教学 → `douyin-caption`，不是本 skill
- 首页拼接封面 → `cover-collage`（默认封面上不叠字；若用户要求加字，封面钩子 **不要** 和本 skill 的笔记标题重复）

## Sub-skills

不强制加载 bible；需要职业/气质细节时读 `character-registry`（Teo=室内设计，Kai=健康科技产品总监）。

See [examples.md](examples.md).
