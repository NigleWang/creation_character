---
name: xiaohongshu-caption
description: >-
  Writes Xiaohongshu (小红书) posting copy for Teo/Kai stills and pose-series —
  short scene + detail + emotion, title, 30–80字 body, 6–10 hashtags. Names
  are Teo (受) and Kai (攻). Use after pose-series generates a set, or when
  the user asks for 文案, 标题, 标签, 小红书发布, caption, or copy for
  approved images.
---

# Xiaohongshu Caption — 发布文案

从成图写出可直接发小红书的 **标题 + 正文 + 标签**。核心：**短、有画面感、带一点情绪，像在看他们的生活片段**。

本 skill **只写文案**。不要调用 `GenerateImage`。不要走换脸 / 换姿态。

| Pipeline | Input | Output |
|----------|--------|--------|
| `pose-series` | 系列成图 | **一组一张文案**（本 skill，Turn 2 结束后必跑） |
| `virtual-couple` / `text-scene` | 单张成图 | 一张文案（用户要文案时跑） |
| **本 skill 单独** | 已有成图 + 文案/标题/标签 | 复制即发的笔记 |

源文档：`docs/code_task/文案.md`。角色名只用 **Teo / Kai**，不要写 Tom / James。

---

## Names (mandatory)

| ID | 显示名 | 定位 | 文案气质 |
|----|--------|------|----------|
| `teo` | **Teo** | 受 | 软感 / 表情 + 小心思 |
| `kai` | **Kai** | 攻 | 气场 / 动作 + 小情绪 |

正文、标题、标签、prompt、新文件名里 **只出现 Teo / Kai**（`teo` / `kai`）。Tom / James 已废弃。

专属标签（每条都带，长期固定）：`#TeoKai` `#TeoKaiDaily`

---

## When to run

**必跑：** `pose-series` Turn 2 QC 通过、系列文件夹写好之后。一组图只出 **一条** 笔记文案。

**也跑：** 用户说 文案 / 标题 / 标签 / 小红书发布 / caption / 配文；或指着 `outputs/approved/`（含 `series/`）要发布文案。

不要在 pose-series Turn 1 写文案（图还没出）。

---

## Workflow (one shot)

1. Identify images: user @path, `outputs/approved/series/<task_id>/`, or latest approved still.
2. Read 1–3 frames (cover + one mid + last if series). Also read `outputs/drafts/look_lock_<task_id>.json` if present.
3. Resolve cast from look-lock / filename / glasses+buzz = Teo, spiky+muscular = Kai, two men = couple (Teo left / Kai right).
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
| 标签 | **6–10 个**，放正文最后 |

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

每条笔记 **6–10 个**。不要堆无关热搜。

### 固定核心（每条都带，至少前 2 个）

`#TeoKai` `#TeoKaiDaily` `#双人设` `#固定角色` `#日常碎片`

双人再加 `#情侣日常`。单人可不加重复的情侣词。

### 内容类型（按 cast 选 3–4 个）

| Cast | 标签 |
|------|------|
| 仅 Kai | `#帅哥` `#氛围感男生` `#侧颜杀` `#男生拍照` |
| 仅 Teo | `#帅哥` `#氛围感男生` `#清冷感` `#男生拍照` |
| 双人 | `#双人照` `#氛围感情侣` `#甜度超标` `#情侣拍照` |

### 氛围（选 1–2 个）

`#氛围感` `#胶片感` `#日系氛围` `#温柔系` `#高级感` `#生活感` `#治愈系`

### 场景（0–1 个，从画面来）

`#办公室` `#咖啡馆` `#居家` `#厨房` `#雨天` `#旅行` `#海边`

不要加 `#虚拟情侣` `#BL` `#AI`。

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

【谁】{仅Teo / 仅Kai / 双人 Teo左 Kai右}
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
  "tags": ["#TeoKai", "#TeoKaiDaily", "#双人设", "#帅哥", "#氛围感男生", "#侧颜杀", "#男生拍照", "#氛围感"],
  "alt_titles": ["刚散会的下颌线", "今天懒得拉链"]
}
```

`cast` 用 `teo` / `kai`（或 both）。新 `task_id` 用 teo/kai，不要用 tom/james。

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
- 首页拼接封面 → `cover-collage`（默认封面上不叠字；若用户要求加字，封面钩子 **不要** 和本 skill 的笔记标题重复）

## Sub-skills

不强制加载 bible；需要职业/气质细节时读 `character-registry`（Teo=室内设计，Kai=健康科技产品总监）。

See [examples.md](examples.md).
