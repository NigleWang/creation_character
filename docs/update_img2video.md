你的提示词有一个很典型的问题：**你把人物一致性和场景一致性控制得非常好，但几乎把视频生成模型最需要的东西——动作变化空间——全部限制住了。**

你现在的提示词更像是在要求模型：

> 请把这张静态图片变成一个只有呼吸、眨眼和嘴唇运动的动态壁纸。

但你的真实目标应该是：

> 保持原图的人物、服装和场景不变，让人物在 10 秒内完成一段有吸引力、有情绪变化、有视觉节奏的连续表演。

这两种目标需要完全不同的提示词设计。

考虑到你是在运营抖音账号，我建议不要简单地增加动作，而是把整个视频设计成一个**以人物为核心、以动作和情绪变化为驱动的微型剧情**。人物不一定需要大幅度运动，但必须持续给观众新的视觉信息。

下面我从提示词的问题、动作设计策略、具体修改方案三个层面分析。

---

# 一、为什么你现在生成的视频人物动作变化很少？

## 1. 最大的问题：MOTION PRIORITY 主动限制了动作

你原来的提示词：

```text
The character remains mostly in the same pose as the reference image.

Allowed: subtle breathing, chest rise, blinking, tiny facial movement,
small eye movement, subtle head movement, very small weight shift,
natural mouth movement during speech.

Avoid: large arm movements, walking, turning around, changing posture,
touching the face or chest, raising/lowering arms, changing clothes,
exaggerated gestures.
```

这里有三个问题。

### 问题 A：你给模型的动作指令都是低强度动作

你允许的动作主要是：

| 动作 | 视觉变化 | 对视频观看体验的潜在影响 |
|---|---|---|
| 呼吸 | 极低 | 主要用于营造生命感 |
| 眨眼 | 极低 | 避免人物像静态图片 |
| 眼球移动 | 低 | 可以传达注意力变化 |
| 细微头部运动 | 低 | 可以传达情绪 |
| 嘴唇运动 | 低至中 | 主要用于配合台词 |
| 微小重心变化 | 低 | 可以增加身体的真实感 |

这些动作适合制作动态壁纸，但未必适合你想要的短视频。

尤其是当人物本身非常强壮、表情严肃、服装和场景又比较固定时，细微动作很容易被观众忽略。

**问题不在于模型不会生成动作，而是你没有给它生成显著动作的权限。**

### 问题 B：你禁止了几乎所有能够改变人物姿态的动作

例如：

```text
Avoid:
large arm movements
turning around
changing posture
touching the face or chest
raising/lowering arms
exaggerated gestures
```

这些限制本身并没有错。

如果你的目标是保持角色一致性，确实应该禁止人物突然转身、走出画面、改变服装等行为。

但你把以下三类动作混在了一起：

1. **破坏一致性的动作**：人物突然转身、服装改变、身体比例变化。
2. **改变身体姿态的动作**：低头、抬头、转动肩膀、调整站姿。
3. **具有叙事意义的动作**：伸手邀请、向观众靠近、回头注视、抬手示意。

第一类应该严格限制，第二类应该适度允许，第三类则应该根据场景有选择地使用。

你的提示词几乎把后两类也禁止了。

### 问题 C：你没有指定一个明确的核心动作

你告诉模型人物可以呼吸、眨眼、说话，但没有告诉它：

- 这个人物接下来想做什么？
- 他为什么要做这个动作？
- 动作发生在什么时候？
- 动作应该如何结束？
- 动作发生后，人物与观众之间的关系有什么变化？

模型得到的自然结果，就是让人物保持原始姿势，只增加最容易生成的微动作。

**改进原则：不要只告诉模型哪些动作不允许，还要明确指定哪些动作必须发生。**

---

## 2. CAMERA CONTINUITY 进一步限制了视频的视觉变化

你原来的要求：

```text
Camera movement is extremely subtle.
Only a very slow micro push-in is allowed.

The character must remain approximately the same size in frame.

Do not zoom out, whip-pan, orbit, tilt dramatically,
change height, change lens perspective, reveal a new area,
or reframe the character.
```

如果你希望固定人物和场景，这些要求大部分都合理。

但是，镜头和人物动作是两个不同的维度。

你可以完全固定镜头，同时允许人物完成丰富的动作。

例如：

- 人物保持在画面中央，但低头后重新抬眼注视观众。
- 人物站在原地，但伸出一只手邀请观众靠近。
- 人物保持相同的站立位置，但缓慢转动上半身。
- 人物向前伸手，随后收回手臂，恢复自然姿态。
- 人物先看向远处，再缓慢转向镜头。

这些动作不需要切镜头，也不需要改变背景。

所以，你不必首先放宽镜头约束，而应该**把人物动作与摄像机运动分开控制**。

我建议第一阶段继续保留固定机位，不要同时引入复杂运镜。

---

## 3. REFERENCE IMAGE PRIORITY 可能被你用得过于绝对

你写道：

```text
Follow it exactly for:
character appearance, face, hair, beard, body proportions,
musculature, clothing, clothing position, hand position,
facial expression, background, architecture, lighting,
shadows, color palette, camera angle, framing.
```

这里有一个很重要的细节：

**人物的初始状态需要严格参考原图，但视频中的后续状态不应该全部被冻结在原图上。**

举个例子。

假设原图里人物双手自然下垂。

你的提示词又要求：

```text
hand position
facial expression
pose
Follow it exactly.
```

接着，你要求人物在视频中伸出一只手。

这两组指令就存在潜在冲突。

模型需要同时满足：

- 手的位置必须与原图一致。
- 手又必须移动到新的位置。

在这种情况下，模型可能会优先满足静态图像的一致性要求，降低动作幅度。

### 正确的做法：区分初始状态和动态状态

把一致性约束分成两类。

**需要始终保持不变的属性：**

- 人物身份与面部特征。
- 发型、胡须、肌肉比例。
- 服装设计和颜色。
- 场景布局和建筑结构。
- 光照风格与整体色彩。
- 动漫画风。

**允许随动作发生变化的属性：**

- 手臂和手的位置。
- 头部角度。
- 眼睛注视方向。
- 面部表情。
- 肩膀和上半身姿态。
- 身体重心。

你需要锁定的是人物的身份，而不是人物的每一个像素和关节位置。

---

# 二、你真正需要的不是更多随机动作，而是动作设计系统

如果你的目标是提高抖音视频的播放时长，我建议你把视频设计成：

**人物身份固定 + 场景固定 + 核心动作明确 + 情绪逐渐变化 + 结尾具有吸引力。**

这里有一个重要区别：

随机增加动作，不等于提高观看时长。

如果人物在 10 秒内不停挥手、转身、耸肩，虽然动作多了，但也可能破坏人物魅力和画面质感。

你应该优先设计那些能够体现人物性格、与观众建立关系、让人期待下一秒的动作。

## 1. 建立人物动作的四个层级

我建议你把动作分成四个层级。

| 层级 | 动作类型 | 具体动作 | 主要作用 |
|---|---|---|---|
| L1 | 生命感动作 | 呼吸、眨眼、眼神变化 | 避免画面僵硬 |
| L2 | 姿态动作 | 低头、抬头、肩膀转动、身体重心变化 | 增加视觉变化 |
| L3 | 互动动作 | 伸手、招手、示意靠近、整理衣领 | 建立人物与观众的联系 |
| L4 | 情绪转折动作 | 先冷漠注视，再露出微笑；先转头，再突然回望 | 制造视觉记忆点 |

你现在的提示词几乎全部集中在 L1。

而对于你这种固定人物、固定场景的动漫人物视频，我建议：

- L1：作为全程基础动作。
- L2：作为主要的身体动作。
- L3：作为核心互动动作。
- L4：根据人物设定选择性使用。

**每条视频不需要四种层级全部出现，但应该至少有一个明确的 L2 或 L3 动作。**

如果人物设定适合带有强烈情绪张力的表现，再增加 L4。

---

## 2. 用一个核心动作串联整段视频

这是我认为你最应该改变的地方。

不要再使用：

```text
0-2s: breathing and blinking.
2-4.5s: subtle mouth movement.
4.5-7s: subtle facial movement.
7-9.5s: maintain eye contact.
```

这相当于把 10 秒拆成了几个微动作时间段，但没有形成动作发展的过程。

你应该设计一个完整的动作链。

例如，你现在的日语台词是：

- こんなじかんまで、なにしてんだよ
- しゅうでん、もうないだろ
- さむいだろ。こっち、こい

从台词的语义来看，人物不是在进行普通的自言自语，而是在深夜发现观众还在外面，随后表现出关心，并邀请对方靠近。

这段台词天然就有三个情绪阶段：

1. 发现：注意到观众还在外面。
2. 关心：意识到观众可能已经很冷。
3. 邀请：示意观众靠近自己。

如果视频只让人物动嘴说话，这些情绪就无法充分表达出来。

因此，你可以设计这样的动作链：

**注意到观众 → 低头观察 → 抬眼注视 → 轻微皱眉 → 伸出手邀请 → 等待观众回应。**

注意，这不是要求人物完成一套夸张的肢体表演，而是通过几个连续动作把台词的含义视觉化。

这样，即使场景、服装和镜头完全不变，人物也会呈现出更丰富的表现力。

---

# 三、如何重新设计你的 10 秒时间轴？

你的原始提示词将三个句子分配在 2.0—9.5 秒之间，但没有充分考虑动作与台词的同步关系。

建议你使用一个更有叙事性的时间轴。

以下是基于你当前台词设计的示例。

## 推荐方案：深夜关心型人物互动

| 时间 | 台词 | 人物动作 | 情绪目的 |
|---|---|---|---|
| 0.0–1.0s | 无台词 | 人物先看向一侧，随后注意到镜头，眼神停留 | 制造注意力变化 |
| 1.0–3.5s | こんなじかんまで、なにしてんだよ | 人物微微低头，皱眉，随后抬眼看向观众 | 表现疑惑和一点责备 |
| 3.5–5.8s | しゅうでん、もうないだろ | 人物轻轻摇头，目光短暂移向远处，再回到观众身上 | 强化深夜环境和关心 |
| 5.8–8.5s | さむいだろ。こっち、こい | 人物伸出一只手，掌心朝上，做出邀请靠近的动作 | 形成核心视觉变化 |
| 8.5–10.0s | 无台词 | 人物保持伸手姿态，眼神柔和下来，等待观众回应 | 留下互动感 |

这里最值得注意的是最后 1.5 秒。

你原来的提示词要求结尾保持稳定：

```text
The final 1 second stays visually stable.
```

这个要求本身没问题，但你把它放在了一个几乎没有动作的整体结构中，导致结尾只是延续静态状态。

新的设计则不同：人物在结尾维持一个具有明确意义的动作。

观众看到的不再是一个没有变化的人物，而是一个正在等待自己回应的人物。

这种互动感可以成为视频的吸引力来源之一。

当然，**动作和情绪设计只能增加潜在吸引力，不能保证播放时长提高**。最终仍然需要通过账号的实际数据验证。

另外，以上时间轴只是一个设计方案。实际生成时，要考虑台词长度、模型的动作执行能力以及音画同步情况。如果伸手动作导致手部变形，可以先改成抬手示意，降低动作复杂度。

---

# 四、直接修改你的提示词：保留一致性，放开动作

我不建议你把原来的提示词全部推倒重写。

你的提示词在画风、角色身份、场景、声音和镜头约束方面已经比较完整。

真正需要改的是以下四个模块：

1. `REFERENCE IMAGE PRIORITY`
2. `CAMERA CONTINUITY`
3. `MOTION PRIORITY`
4. `TIMELINE`

尤其是第三个模块。

下面给出可以直接替换原提示词中相应部分的英文版本。

## 1. 修改 REFERENCE IMAGE PRIORITY

将原来的静态属性锁定与动态动作分开。

```text
REFERENCE IMAGE PRIORITY:

The uploaded image is the definitive reference for the character's
identity, visual design, anime art style, clothing, environment,
lighting, and initial pose.

Preserve the exact character identity:
face, hairstyle, beard, muscular build, body proportions,
clothing design, and overall visual appearance.

Preserve the original environment, architecture, lighting,
color palette, and camera angle.

IMPORTANT DISTINCTION:

The reference image defines the initial visual state,
not a frozen pose that must be maintained throughout the video.

The character is allowed to move naturally from the initial pose
to perform the explicitly specified actions.

Temporary changes in hand position, arm position, head angle,
gaze direction, facial expression, shoulder orientation,
and upper-body posture are allowed when required by the action.

All movements must remain anatomically coherent and consistent
with the original character design.

Do not redesign the character.
Do not alter his identity, body proportions, clothing design,
or the surrounding environment.
```

这里最重要的是：

`The reference image defines the initial visual state, not a frozen pose.`

这句话明确告诉模型：原图是初始状态，不是整个视频的姿态限制。

## 2. 修改 CAMERA CONTINUITY

保留固定机位，但不要把固定机位与固定姿态绑定。

```text
CAMERA CONTINUITY:

Maintain a single continuous shot with no cuts or transitions.

Keep the original camera angle, lens perspective,
composition, and background layout.

The camera remains locked in place.
No orbiting, panning, tilting, reframing, or dramatic zooming.

The character may perform meaningful upper-body movements
while remaining in approximately the same position in the frame.

Allow the character's hands and arms to move naturally
within the visible frame when required by the specified action.

The character's body may change pose temporarily,
but his identity, body proportions, and visual design must remain
consistent with the reference image.

Prioritize character performance over camera movement.
```

这里的关键不是让镜头动起来，而是允许人物在原有画面内改变姿态。

需要注意，如果原图只显示人物胸部以上，那么伸手动作也应该受到画面边界限制，不要要求模型生成原图中根本没有的完整身体。

## 3. 重点修改 MOTION PRIORITY

这是整个提示词最重要的改动。

建议用下面这段替换原来的 `MOTION PRIORITY`。

```text
MOTION PRIORITY:

The goal is to create an engaging animated character performance,
not a minimally animated still image.

Preserve the character's identity and the original scene,
but allow clear, intentional, emotionally motivated movements.

The character must perform the specified primary action.
Do not replace the primary action with breathing, blinking,
lip movement, or other negligible micro-movements.

ACTION HIERARCHY:

1. PRIMARY ACTION:
   One clear, readable character action that changes the visual state
   and communicates the meaning of the dialogue.

2. SECONDARY ACTION:
   A complementary head movement, gaze shift, facial expression,
   or upper-body movement that supports the primary action.

3. CONTINUOUS MICRO-MOTION:
   Natural breathing, blinking, subtle eye movement,
   and small facial changes throughout the shot.

MOVEMENT DESIGN:

Every major dialogue beat should produce a visible change
in the character's expression, gaze, posture, or hand position.

Use deliberate, smooth, anatomically coherent movements.
Actions should develop progressively rather than occurring randomly.

Allow moderate head movement, shoulder rotation,
small upper-body posture changes, and natural arm gestures.

When explicitly specified, allow the character to raise one hand,
extend one arm toward the viewer, or make a clear beckoning gesture.

The character may briefly shift his gaze away from the viewer
and then return to direct eye contact.

Avoid repetitive idle animation.

Do not keep the character in exactly the same pose for the entire video.

Do not introduce unrelated gestures or excessive movement.
Avoid abrupt pose changes, exaggerated body deformation,
extra fingers, distorted hands, or inconsistent anatomy.

The character must complete the specified action
and settle into the intended final pose.
```

这段提示词做了三件重要的事。

**第一，明确主要动作的优先级。**

`The character must perform the specified primary action.`

这比简单地说允许某些动作更有用，因为它明确指定了动作是必须完成的任务，而不是可有可无的选项。

**第二，把动作设计成层级结构。**

核心动作负责改变画面，辅助动作负责表达情绪，微动作负责维持生命感。

这样，模型就不会只生成呼吸和眨眼。

**第三，允许动作发生，但要求动作有明确的结束状态。**

例如，人物伸手之后，需要自然地停留在邀请姿态，而不是手臂随机摆动。

这有助于降低动作不连贯的风险。

不过，不同视频模型对复杂动作的执行能力不同。如果你的模型对英文长提示词遵循程度不高，可以优先保留 `PRIMARY ACTION`、`ACTION TIMELINE` 和明确的禁止项，而不是继续增加大量形容词。

---

# 五、TIMELINE 也需要重新设计

你原来的时间轴主要围绕台词安排，没有给动作设置明确的开始、发展和结束。

我建议改成以下结构。

```text
ACTION TIMELINE:

0.0-1.0s — NOTICE THE VIEWER

Begin from the exact reference pose.

The character notices the viewer and shifts his gaze toward
the camera. His expression becomes slightly more attentive.

Keep natural breathing and subtle facial movement.
Do not remain completely motionless.

1.0-3.5s — QUESTION

Dialogue:
"こんなじかんまで、なにしてんだよ"

The character slightly lowers his head and looks directly
at the viewer with a mildly concerned, questioning expression.

He then raises his eyes while maintaining his original stance.

The head movement and facial expression must be clearly visible,
but controlled and natural.

3.5-5.8s — EXPRESS CONCERN

Dialogue:
"しゅうでん、もうないだろ"

The character briefly shifts his gaze toward the distant platform,
gives a subtle head shake, and returns his attention to the viewer.

His expression communicates concern rather than anger.

Keep the body grounded and the camera completely stable.

5.8-8.5s — INVITE THE VIEWER

Dialogue:
"さむいだろ。こっち、こい"

The character raises one arm and extends one hand toward
the viewer in a natural beckoning gesture.

The gesture should be deliberate and clearly readable.
The palm and fingers move naturally.

His expression softens slightly as he invites the viewer closer.

Keep the gesture within the original composition.
Do not move the camera.

8.5-10.0s — HOLD THE INVITATION

The character maintains the final inviting hand gesture.

He keeps eye contact with the viewer and shows a subtle,
warm change in facial expression.

Natural breathing and one small blink are allowed.

The pose remains stable without freezing completely.

No new action begins during the final hold.
```

### 一个非常重要的细节

你原来规定：

```text
9.5-10.0s: Natural living hold.
```

我建议不要把结尾固定成完全没有动作的停留，而是让人物在完成核心动作后保持一个有意义的姿态。

如果这条视频的核心是伸手邀请，那么最后的画面就应该是人物伸着手、注视观众。

这样，结尾既可以保持稳定，也能延续人物的情绪。

另外，时间轴应当服务于动作，而不是机械地服从固定秒数。

如果实际模型对 10 秒内的三句日语台词无法准确同步，就应该先测试较短的台词或减少动作数量，而不是强行把所有内容塞进同一条视频。

---

# 六、比修改提示词更重要：建立自己的动作素材库

考虑到你想持续运营账号，我建议你不要每次都从零开始构思人物动作。

你可以为固定人物建立一套动作库。

每条视频只需要选择一个核心动作，再搭配一两个辅助动作。

下面是我建议优先测试的动作类型。



| 动作编号 | 核心动作 | 辅助动作 | 适用情绪 | 生成难度 |
|---|---|---|---|---|
| A01 | 从低头转为抬眼注视 | 轻微皱眉 | 冷峻、压迫感 | 低 |
| A02 | 向观众伸出一只手 | 头部轻微倾斜 | 邀请、关心 | 中 |
| A03 | 轻轻招手，示意靠近 | 眼神变柔和 | 亲密互动 | 中 |
| A04 | 缓慢转动肩膀并回头注视 | 短暂停顿 | 神秘、警觉 | 中 |
| A05 | 抬手整理衣领 | 低头后重新抬眼 | 自信、成熟 | 中 |
| A06 | 双臂交叉，然后轻微低头 | 眉毛和目光变化 | 冷酷、克制 | 中 |
| A07 | 将手伸向画面前方后停留 | 目光跟随手部动作 | 强互动感 | 中高 |
| A08 | 先看向远处，再回望观众 | 轻微皱眉 | 剧情感、悬念 | 低至中 |

这里的难度只是相对估计，实际表现会受到原图构图、手部是否可见、模型能力等因素影响。

对于你现在的目标，我会优先测试 A01、A02、A03 和 A08。

原因很简单：

- A01 的动作幅度小，比较容易保持人物一致性。
- A02 和 A03 可以产生明确的互动感。
- A08 可以通过目光变化制造注意力转移。

而且，这些动作都不需要更换场景。

你可以在不同视频中反复使用同一种动作结构，但要改变台词、情绪和动作时机，避免账号内容变得机械重复。

---

# 七、真正应该做的是实验，而不是一次性重写所有提示词

这里我建议你采用一个简单的对照实验。

因为你目前有两个明确目标：

1. 人物和场景保持一致。
2. 人物动作更有吸引力，进而提高播放时长。

你需要验证的是：**在一致性基本不变的前提下，增加明确的动作设计，是否真的能改善账号表现。**

## 实验一：比较三种动作强度

固定同一张参考图、同一段台词、同一模型、相同生成参数。

只改变动作提示词。

| 实验组 | 动作策略 | 预期结果 |
|---|---|---|
| A：基线组 | 呼吸、眨眼、说话 | 测量当前效果 |
| B：中等动作组 | 低头、抬眼、轻微转头 | 测试姿态变化的价值 |
| C：互动动作组 | 低头、抬眼、伸手邀请 | 测试明确互动动作的价值 |

每组最好生成多个样本，以降低随机生成结果对判断的影响。

注意，这个实验不是为了验证 C 一定比 A 好，而是为了确定你的模型能够稳定完成哪一类动作。

如果 C 组动作更明显，但手部变形严重、人物一致性下降，就需要在 B 和 C 之间寻找平衡。

## 实验二：比较动作发生的时机

确定最适合你的动作类型之后，再测试动作时机。

例如：

- 版本 A：人物在前 2 秒就开始移动。
- 版本 B：人物先注视观众，再开始移动。
- 版本 C：人物在说到最后一句话时完成核心动作。

这三个版本的动作可以完全相同，只改变动作出现的时间。

你可以观察哪种开场和动作节奏更容易让观众继续观看。

这里需要注意：不要预先认定悬念式开场一定有效。应该让数据决定哪种方式适合你的账号。

## 实验三：建立质量和播放表现的双重评估

不要只看播放时长，也不要只看画面是否漂亮。

建议至少记录以下指标：

| 指标 | 用途 |
|---|---|
| 人物一致性评分 | 检查脸部、肌肉、服装是否发生漂移 |
| 动作完成率 | 检查指定动作是否真的发生 |
| 动作自然度 | 检查身体和手部是否变形 |
| 平均播放时长 | 衡量整体观看时间 |
| 平均播放时长 / 视频时长 | 比较不同视频的相对观看表现 |
| 完播率 | 观察观众是否看到了结尾 |
| 互动率 | 观察动作是否激发了点赞、评论等行为 |

其中，前面三项用于评估视频生成质量，后面几项用于评估账号运营表现。

这两组指标需要分开分析。

例如，某个动作的画面质量很好，但播放时长没有提升，这说明动作生成成功不等于内容吸引力提高。

反过来，如果某个视频播放表现很好，但人物严重变形，也不适合直接将其作为长期生产模板。

还要注意，如果不同视频的时长不一致，平均播放时长不能单独作为唯一判断标准。

---

# 八、最后，我建议你把整个提示词系统拆成三个部分

如果你准备长期运营这个抖音账号，并且每周导出一次数据，那么最适合你的方式不是维护一条越来越长的提示词，而是建立一个可以组合的提示词系统。

我建议分成三个模块。

### 模块一：Identity Lock

负责保持人物身份和视觉风格。

包括：

- 人物身份。
- 面部、发型、胡须。
- 肌肉比例。
- 服装。
- 动漫画风。
- 场景和光照。

这一部分尽量固定。

### 模块二：Action Plan

负责定义每条视频的具体表演。

例如：

```text
PRIMARY ACTION:
The character extends one hand toward the viewer
in a deliberate, inviting gesture.

SECONDARY ACTION:
He briefly lowers his head, then raises his eyes
to establish direct eye contact.

EMOTIONAL PROGRESSION:
Concern → attention → invitation.

FINAL POSE:
The character holds the inviting gesture
while maintaining eye contact.
```

这一部分应该根据每条视频的台词、人物情绪和运营实验进行调整。

### 模块三：Performance Timeline

负责把动作安排到具体时间段。

例如：

```text
0-1s:
Establish eye contact.

1-3s:
Lower the head slightly and show concern.

3-6s:
Raise the eyes and shift the gaze.

6-8s:
Extend one hand toward the viewer.

8-10s:
Hold the inviting gesture and maintain eye contact.
```

这样，你就可以在不修改人物设定和场景约束的前提下，独立测试不同的动作方案。

这也是你以后设计自动化运营 Agent 时很有价值的一个思路：**将人物一致性作为固定约束，将动作方案作为可实验变量，再用后验数据判断哪些动作模式值得继续生产。**

---

## 我的最终建议

你当前的提示词不需要继续增加更多关于人物身份、服装、场景和镜头的约束。这些部分已经相当完整。

你最需要做的，是下面三项调整：

1. **把参考图定义为初始状态，而不是整段视频的固定姿态。**
2. **明确指定每条视频必须完成的一个核心动作，并为其安排开始、发展和结束。**
3. **让人物动作与台词中的情绪和互动意图对应，而不是只按时间安排呼吸、眨眼和口型。**

第一轮测试，我建议你保留现有的 `CHARACTER LOCK`、`SCENE LOCK`、`ART STYLE LOCK` 和大部分 `AUDIO` 约束，只替换动作相关模块。

优先测试这三个版本：

- **版本 A：** 低头 → 抬眼注视。
- **版本 B：** 低头 → 抬眼注视 → 伸手邀请。
- **版本 C：** 先看向远处 → 回望观众 → 伸手邀请。

先比较这三种动作方案在同一张参考图上的生成质量，再根据结果决定是否需要放宽其他限制。

**核心原则是：固定人物身份，不固定人物姿态；固定场景，不固定人物的情绪和行为。**