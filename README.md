# Xiaohongshu Virtual Couple Studio

**Tom（受）× James（攻）** — 角色驱动的小红书内容生产流水线。

上传场景参考图 → @角色名 → 自动分析场景、绑定角色、生图、QC → 返回可发小红书竖图。

---

## 角色

| 角色 | 定位 | 默认位置 | 参考图 |
|------|------|----------|--------|
| **Tom** | 受 | 左 | `characters/tom/references/face_01.jpeg` |
| **James** | 攻 | 右 | `characters/james/references/face_01.jpeg` |

原始参考图备份：`data/imgs/Tom.jpeg`、`data/imgs/James.jpeg`

---

## Cursor 手机版 / Cloud 用法（两轮对话）

> Cloud Agent **不会弹窗**，必须分 **两轮** 对话。

**第 1 轮（上传场景图）：**
```text
@virtual-couple @James
```

Agent 应回复编号选项并 **停止**，不会生图。

**第 2 轮（你回复选项）：**
```text
2,3,2,3
```
或 `角色默认，上衣藏青，下装灰`

Agent 才调用 GenerateImage。

---

**一条消息跳过询问（可选）：**
```text
@virtual-couple @James
全部保持原场景
```

---

## Pipeline

```text
用户上传 Scene + @角色
        ↓
  @virtual-couple（主编排）
        ↓
  character-registry → 加载 Tom/James Bible
        ↓
  scene-analyzer → 提取构图/动作/光影（不识别原图人物）
        ↓
  scene-customizer → ★ 聊天里发编号选项，等你文字回复 ★
        ↓
  character-composer → 左=Tom(受) 右=James(攻)
        ↓
  prompt-builder → 组装生图 Prompt
        ↓
  GenerateImage（scene + 角色参考图）
        ↓
  quality-control → 角色/场景/小红书 QC
        ↓
  outputs/approved/ + 标题/标签建议
```

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
│   │   ├── quality-control/
│   │   └── xiaohongshu-post/
│   └── rules/
├── characters/
│   ├── tom/                     # 受
│   └── james/                   # 攻
├── relationship/
├── templates/
├── workflows/
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
| `xiaohongshu-post` | 标题/标签/交付格式 |

---

## 核心规则

```
Character 决定「是谁」（脸、身材、发型、气质）
Scene 决定「在哪、做什么、怎么构图」
左 = Tom（受）  右 = James（攻）  永不互换
```

---

## 技术文档

详细架构设计见 [`docs/code_task/swap_face.md`](docs/code_task/swap_face.md)
