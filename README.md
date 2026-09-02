# Xiaohongshu Virtual Couple Studio

**Teo（受）× Kai（攻）** — 角色驱动的小红书内容生产流水线。

上传场景参考图 → @角色名 → 自动分析场景、绑定角色、生图、QC → 返回可发小红书竖图。

---

## 角色

| 角色 | 定位 | 默认位置 | 参考图 |
|------|------|----------|--------|
| **Teo** | 受 | 左 | `characters/teo/references/face_01.jpeg` |
| **Kai** | 攻 | 右 | `characters/kai/references/face_01.jpeg` |

原始参考图备份：`data/imgs/Teo.jpeg`、`data/imgs/Kai.jpeg`

---

## Cursor 手机版 / Cloud 用法（两轮对话）

> Cloud Agent **不会弹窗**，必须分 **两轮** 对话。

**第 1 轮（上传场景图）：**
```text
@virtual-couple @Kai
```

Agent 应回复编号选项并 **停止**，不会生图。

**第 2 轮（你回复选项）：**
```text
2,3,2,3
```
或 `角色默认，上衣藏青，下装灰`

Agent 才调用 GenerateImage。

**第 1 轮（只发文字，不传图）：**
```text
按人设出图：周末早上两个人在厨房
```
Agent 补全场景卡并停止。你回 `生成` 才出图。

**一条消息跳过询问（换脸，可选）：**
```text
@virtual-couple @Kai
全部保持原场景
```

---

## Cloud 远程出图并提交到同一条 branch

默认 Cloud Agent 会推到新的 `cursor/…` 分支。本仓库脚本强制 `workOnCurrentBranch: true`、`autoCreatePR: false`，把系列 PNG 提交到你指定的 branch（默认当前 git 分支）。

图必须写在 `outputs/approved/series/<task_id>/*.png`（gitignore 已放行）。根目录的 `outputs/approved/xiaohongshu_*.png` 提交不进去。

```bash
export CURSOR_API_KEY="cursor_..."   # Dashboard → Integrations / API Keys
# GitHub 仓库需已在 Cursor Integrations 里连上

# 新建 Cloud Agent，生成后 commit + push 到当前分支
node scripts/launch_cloud_series.mts launch \
  --task-id 20260902_kai_office_series \
  -- "全套日常姿态，锁定现有形象与服装，生成后提交到当前分支"

# 同一 agent、同一分支再补图（不要重新 launch）
node scripts/launch_cloud_series.mts follow -- "再补 04_coffee.png"

node scripts/launch_cloud_series.mts status
```

agent id 会写到 gitignored 的 `outputs/drafts/cloud_agent.json`。指定分支：`--branch main`。已有 PR 往 head 堆 commit：`--pr-url https://github.com/…/pull/123`。

---

## Pipeline

```text
用户上传 Scene + @角色
        ↓
  @virtual-couple（主编排）
        ↓
  character-registry → 加载 Teo/Kai Bible
        ↓
  scene-analyzer → 提取构图/动作/光影（不识别原图人物）
        ↓
  scene-customizer → ★ 聊天里发编号选项，等你文字回复 ★
        ↓
  character-composer → 左=Teo(受) 右=Kai(攻)
        ↓
  prompt-builder → 组装生图 Prompt
        ↓
  GenerateImage（scene + 角色参考图）
        ↓
  quality-control → 角色/场景/小红书 QC
        ↓
  outputs/approved/ + 标题/标签建议
```

另两条入口：

- **文字场景**（无照片）→ `@text-scene`：先补全场景卡，你回复「生成」后再出一张
- **已有成图换姿态** → `@pose-series`：先选编号姿态，组图进 `outputs/approved/series/`，出图后自动给小红书文案（Teo / Kai）
- **成图转动画** → `@gemini-video`：写出可复制进 Gemini 的 10 秒图生视频提示词（台词日语假名）
- **只要文案** → `@xiaohongshu-caption`：对着成图/系列写标题+正文+标签

---

## 项目结构

```text
creation_character/
├── .cursor/
│   ├── skills/
│   │   ├── virtual-couple/      ← 主入口，手机 @ 这个
│   │   ├── character-registry/
│   │   ├── scene-analyzer/
│   │   ├── scene-customizer/    ← 换脸前询问装饰/服装选项
│   │   ├── character-composer/
│   │   ├── prompt-builder/
│   │   ├── pose-series/         ← 成图锁定形象，换姿态做系列
│   │   ├── xiaohongshu-caption/ ← 系列/成图 → 小红书发布文案（Teo/Kai）
│   │   ├── text-scene/          ← 文字场景按人设补全后再出一张
│   │   ├── gemini-video/        ← 成图 → Gemini 10s 视频提示词（假名台词）
│   │   ├── quality-control/
│   │   └── xiaohongshu-post/
│   └── rules/
├── characters/
│   ├── teo/                     # 受
│   └── kai/                     # 攻
├── relationship/
├── templates/
├── workflows/
├── scripts/
│   └── launch_cloud_series.mts  # Cloud 出图并 push 到同一条 branch
├── scenes/                      # 上传的场景图存这里
├── outputs/
│   ├── drafts/
│   ├── approved/                # 可发小红书成品
│   └── rejected/
└── data/imgs/                   # 原始参考图
```

---

## Skills 一览

| Skill | 作用 |
|-------|------|
| `virtual-couple` | 主编排，手机端 @ 入口 |
| `character-registry` | 加载角色 Bible 与参考图路径 |
| `scene-analyzer` | 场景结构提取 → Scene Blueprint |
| `scene-customizer` | **换脸前询问**：装饰物、衣服颜色、图案 |
| `character-composer` | 角色与场景位置绑定 |
| `prompt-builder` | 生成 GenerateImage 描述 |
| `quality-control` | 成品质检 |
| `xiaohongshu-caption` | 成图/系列 → 小红书标题+正文+标签（Teo/Kai） |
| `xiaohongshu-post` | 3:4 规格 / 封面构图 / 交付格式 |
| `gemini-video` | 成图 → Gemini 10s 图生视频提示词（台词假名，复制即用） |

---

## 核心规则

```
Character 决定「是谁」（脸、身材、发型、气质）
Scene 决定「在哪、做什么、怎么构图」
左 = Teo（受）  右 = Kai（攻）  永不互换
```

---

## 技术文档

详细架构设计见 [`docs/code_task/swap_face.md`](docs/code_task/swap_face.md)
