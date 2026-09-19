如果你的核心目标是：

> **把同一组图片分别生成多个 10s clip，最后拼成一个完整视频，而且每个 clip 都严格继承图片中的人物、服装、场景、光线和姿态。**

那么你现在这版 prompt 最大的问题不是“描述不够详细”，而是**把单个 Clip 的要求和整个 4-Clip 连续性的要求混在了一起**。

尤其是 `Clip 1 of 4`、`next clip can continue` 这些描述，对视频模型来说通常不够稳定。你需要把 Prompt 改造成一种 **「视觉锚点 + Clip 状态 + 片尾状态」** 的结构。

---

# 一、最需要修改的几个地方

## 1. `SERIES LOCK` 要从“连续视频”改成“独立 Clip + 状态继承”

你现在：

> `Clip 1 of 4 in one continuous office-corridor take`

这个容易让模型理解成：

> “我要生成一段 40 秒视频，只不过现在截取第 1 段。”

但实际上你的工作流应该是：

```text
图片1 → Video 1 10s
              ↓
图片2 → Video 2 10s
              ↓
图片3 → Video 3 10s
              ↓
图片4 → Video 4 10s
```

因此更应该强调：

> **每个 10 秒视频都是独立生成，但视觉连续性必须像同一个长镜头。**

建议改成：

```text
SERIES CONTINUITY:
This is one clip in a multi-clip sequence.
Each clip is generated independently from its own reference image,
but all clips must look like consecutive moments of the SAME continuous scene.

Preserve continuity across clips:
- same character identity
- same face
- same hairstyle
- same beard
- same body proportions
- same clothing
- same clothing condition
- same sweat/dampness
- same location
- same lighting
- same time of day
- same visual style
- same camera height and lens feel

Do NOT reset the character or scene at the beginning of the clip.
Do NOT introduce a new pose, new outfit, new lighting, or new background.
```

这个比 `Clip 1 of 4` 更重要。

---

# 二、你现在最缺的是「图片优先级」

你现在写了：

> `IDENTITY LOCK`

但实际上你的需求不是单纯“人物身份锁定”。

你需要的是：

> **Reference Image Priority**

也就是告诉模型：

**如果文字描述和图片冲突，以图片为准。**

建议直接加入：

```text
REFERENCE IMAGE PRIORITY:

The uploaded image is the primary visual source of truth.

Follow the uploaded image exactly for:
- character appearance
- face
- hair
- beard
- body proportions
- clothing
- clothing position
- pose
- hand position
- facial expression
- background
- architecture
- lighting
- shadows
- color palette
- camera angle
- framing

Do not reinterpret, redesign, beautify, or regenerate these elements.

If any textual instruction conflicts with the reference image,
PRIORITIZE THE REFERENCE IMAGE.
```

这个非常重要。

因为你现在：

> `Camera stays low-angle and only eases closer`

实际上是在**主动限制模型改变镜头**。

如果你的图片本身已经是非常好的构图，最好直接：

> **Camera angle and initial framing must match the reference image.**

而不是重新指定 low-angle。

---

# 三、`Motion` 需要改：不要写太多剧情动作

你现在：

```text
0-2 breathing
2-4.5 glance
4.5-7 head tilt
7-9.5 chin dips
9.5-10 hold
```

对于图生视频来说，这有一个问题：

**动作太多。**

模型可能会为了完成这些动作而产生：

* 脸变
* 手臂变形
* 衣服变化
* 肌肉变化
* 身体比例变化
* 背景漂移
* 镜头突然移动

尤其你希望多个 clip 连起来。

我建议：

> **动作幅度小，镜头运动小，人物变化小。**

也就是：

```text
MOTION PRIORITY:
Natural micro-motion is more important than large movements.

The character remains mostly in the same pose as the reference image.

Allowed motion:
- subtle breathing
- natural blinking
- tiny facial movements
- small eye movement
- subtle head movement
- very small weight shift
- natural mouth movement during speech

Avoid:
- large arm movements
- dramatic body movement
- turning around
- walking
- changing posture
- touching the face
- changing clothes
- exaggerated gestures
```

这会明显提高多 clip 的一致性。

---

# 四、最关键：增加 `END STATE LOCK`

你现在虽然写了：

> `end in a living hold that the next clip can continue`

但还不够具体。

如果你要把：

```text
Clip 1 + Clip 2 + Clip 3 + Clip 4
```

拼起来，那么每一个视频最后 0.5~1 秒其实非常重要。

建议加入：

```text
END STATE:

The final 1 second must remain visually stable.

At the end of the clip:
- maintain the same body position
- maintain the same camera position
- maintain the same facial identity
- maintain the same eye direction
- maintain the same lighting
- finish with a natural breathing / blinking motion
- no dramatic gesture
- no camera reset
- no transition
- no fade
- no freeze-frame effect

The final frame should look like a natural intermediate frame,
not like an ending frame.
It must be easy to continue seamlessly into the next clip.
```

这个概念很重要：

### 不要让模型“结束”。

而是让它：

> **停留在一个“故事还没结束”的中间状态。**

---

# 五、你现在的 `CAMERA` 也建议改

现在：

> `low-angle slow push-in toward chest and face`

问题是：

如果 4 个 clip 都这么写：

```text
Clip 1 → push in
Clip 2 → push in
Clip 3 → push in
Clip 4 → push in
```

最后会越来越近。

而且每个 clip 的模型都会把：

> “push-in”

理解成重新设计自己的镜头运动。

建议：

```text
CAMERA CONTINUITY:

Preserve the exact camera angle and framing of the reference image.

Camera movement is extremely subtle and continuous.

Only a very slow micro push-in is allowed.
The camera must never:
- zoom out
- whip pan
- orbit
- tilt dramatically
- change height
- change lens perspective
- reveal a new area of the environment
- reframe the character

The character should remain approximately the same size in frame.
```

如果你的四张图本身已经有不同构图，那就更加应该：

> **每个 Clip 的 camera 以对应图片为绝对锚点。**

---

# 六、你现在的 Dialogue 也有一个结构问题

你写：

```text
FIRST LINE STARTS at 2.0s
...
second line
...
third line
```

然后：

> `After 2s keep dialogue dense.`

如果你的四个 clip 是一个连续对话，那么建议明确：

```text
DIALOGUE CONTINUITY:

The dialogue is part of one continuous conversation.

Do not repeat previous lines.
Do not restart the conversation.
Do not add narration.
Do not improvise additional dialogue.

Speak only the provided lines.
Natural pauses are allowed, but speech should remain conversational.

The final spoken phrase should end naturally near the end of the clip,
leaving a short breathing pause before the next clip.
```

尤其：

> **Do not improvise additional dialogue.**

很重要。

否则视频模型经常会自己加一句。

---

# 七、还有一个很重要的问题：你把「人物名字」放进去了

你写：

> `CAST: The muscular anime man is Tagame`

如果 `Tagame` 是你自己的虚构角色名字，没问题。

但从 prompt engineering 角度，我甚至建议减少这种信息。

直接：

```text
CHARACTER:
The adult muscular anime man shown in the reference image.
```

因为真正重要的是：

> **reference image 中的这个人**

而不是名字。

尤其你的目标是：

```text
Image → Video
```

那么：

**图片 > 角色文字描述**

---

# 八、建议删掉一些“重复约束”

你现在 prompt 有大量：

```text
ANIME
FICTION
IDENTITY LOCK
SERIES LOCK
CAMERA
CONSTRAINTS
```

其实有很多重复。

例如：

> `Do NOT restyle into photorealistic live action.`

> `Anime, not photoreal.`

重复。

又比如：

> `Do not fade out.`

> `Do not cut.`

> `Single continuous shot.`

> `Do not whip-pan.`

这些可以集中成：

```text
SHOT:
One continuous shot.
No cuts.
No transitions.
No fade.
No scene change.
No camera reset.
```

Prompt 越清晰，模型越容易抓住真正重要的约束。

---

# 九、我建议你把整个 Prompt 重构成这 8 层

你现在比较适合这个结构：

```text
1. FORMAT
2. REFERENCE IMAGE PRIORITY
3. CHARACTER LOCK
4. SCENE LOCK
5. SERIES CONTINUITY
6. MOTION
7. CAMERA
8. AUDIO / DIALOGUE
9. END STATE
10. NEGATIVE CONSTRAINTS
```

而不是现在这种“各种 Lock 混在一起”。

---

# 十、给你一版更适合「10s × 4 连续视频」的完整 Prompt

你可以直接拿这版作为基础模板：

ANIME IMAGE-TO-VIDEO.

Create a 10-second vertical video from the uploaded reference image.

FORMAT:

* Duration: 10 seconds
* Aspect ratio: 9:16
* Single continuous shot
* No cuts
* No transitions
* No fade
* No new location
* No costume change

REFERENCE IMAGE PRIORITY:

The uploaded image is the PRIMARY VISUAL SOURCE OF TRUTH.

Follow the reference image exactly for:

* character identity
* face
* hairstyle
* beard
* body proportions
* musculature
* clothing
* clothing position
* pose
* hand position
* facial appearance
* background
* architecture
* lighting
* shadows
* color palette
* camera angle
* framing

Do not redesign, reinterpret, beautify, or regenerate the character.

If any textual instruction conflicts with the reference image, PRIORITIZE THE REFERENCE IMAGE.

ART STYLE LOCK:

Preserve the exact high-quality Japanese anime / digital illustration style of the reference image.

Do not convert the character into photorealistic live action.
Do not make him look like a real person.
Do not change the anime rendering style.

CHARACTER LOCK:

The adult muscular anime man shown in the reference image.

Preserve exactly:

* face identity
* dark-brown short spiked hair
* brown beard
* extreme muscular build
* body proportions
* clothing
* sweat / damp clothing condition
* facial characteristics

Do not slim the character.
Do not make him younger.
Do not make him look like a pretty-boy.
Do not change his body proportions.

SCENE LOCK:

The scene remains exactly the same as the reference image.

Same:

* office corridor
* architecture
* background
* lighting
* time of day
* atmosphere
* color palette

Do not introduce new people.
Do not remove existing people.
Do not add new objects.
Do not change the location.

SERIES CONTINUITY:

This is one clip in a multi-clip sequence.

Each 10-second clip is generated independently from its own reference image, but all clips must look like consecutive moments of ONE continuous scene.

Maintain continuity across clips:

* same character
* same face
* same hairstyle
* same beard
* same body proportions
* same clothing
* same clothing condition
* same sweat / dampness
* same environment
* same lighting
* same visual style
* same camera language

Do not reset the scene at the beginning of the clip.

Do not introduce a new pose, new outfit, new lighting, or new environment.

MOTION:

Preserve the original pose from the reference image.

Use subtle natural movement only.

Allowed:

* natural breathing
* subtle chest movement
* natural blinking
* small eye movement
* subtle facial movement
* small head movement
* very small weight shift
* natural mouth movement while speaking

Avoid large movements.

Do not:

* walk
* turn around
* dramatically change posture
* make large arm gestures
* raise or lower the arms significantly
* touch the face
* change the clothing
* change body proportions

The character should remain visually close to the original reference pose throughout the clip.

TIMELINE:

0.0–2.0s:
Very subtle living motion from the exact reference pose.
Natural breathing, blinking and a small preparatory inhale.
Do not stare unnaturally like a frozen image.

2.0–4.5s:
Begin the first dialogue line.
Natural eye movement toward the camera.
Maintain the original body pose.

4.5–7.0s:
Continue the second dialogue line.
Only subtle facial and head movement.
No large gesture.

7.0–9.5s:
Continue the third dialogue line.
Maintain direct eye contact.
Only minimal natural movement.

9.5–10.0s:
Natural living hold.
Mouth closes naturally after the final word.
Continue subtle breathing.
Do not freeze.
Do not create an ending pose.

CAMERA CONTINUITY:

Preserve the camera angle and initial framing of the reference image.

Camera movement must be extremely subtle.

Only allow a very slow micro push-in.

Do not:

* zoom out
* whip-pan
* orbit
* dramatically tilt
* change camera height
* change perspective
* reveal a new area of the environment
* reframe the character
* reset the camera

The character should remain approximately the same size in frame.

END STATE:

The final 1 second must look like a natural intermediate moment in an ongoing scene.

Do not create a cinematic ending.

Do not fade out.
Do not freeze.
Do not change expression dramatically.
Do not change pose.

The final frame should be easy to continue into the next 10-second clip.

DIALOGUE:

Japanese speech only.

Use a low, mature Japanese male voice with natural conversational delivery.

Lip-sync accurately to the provided dialogue.

Speak ONLY the provided lines.
Do not improvise.
Do not add narration.
Do not repeat previous dialogue.

No English.
No Chinese.
No subtitles.
No captions.
No on-screen text.
No logos.
No watermarks.

DIALOGUE:

"おまえが あんきできない ほん"

"だれかが あんきできる"

"おまえが できない もんだい"

AUDIO:

No background music.

Quiet office corridor room tone.
Distant HVAC.
Natural breathing.
Subtle clothing / fabric sounds.
One soft natural footstep only if consistent with the reference pose.

FINAL CONSTRAINTS:

Anime only.
Preserve the reference image.
Preserve character identity.
Preserve clothing.
Preserve location.
Preserve lighting.
Preserve body proportions.
Preserve camera language.
Minimal natural motion.
No scene change.
No character redesign.
No photorealism.
No cuts.
No transitions.
No fade.
No freeze-frame.
No new dialogue.

---

# 十一、如果你真正要做「4段拼接」，还有一个更重要的技巧

我反而建议你**不要把 4 个 prompt 完全写死成一样的东西**。

应该有：

### 一个 Base Prompt

负责：

```text
人物
画风
服装
场景
光线
声音
镜头语言
一致性
```

然后每个 Clip 只改变：

```text
CLIP STATE
+
DIALOGUE
+
MOTION
+
END STATE
```

例如：

```text
BASE
  ↓
Clip 1
  起始状态 = Image 1
  动作 = 微表情
  台词 = A
  结束状态 = State A

  ↓

Clip 2
  起始状态 = Image 2
  动作 = 从 State A 自然延续
  台词 = B
  结束状态 = State B

  ↓

Clip 3
  起始状态 = Image 3
  动作 = 从 State B 自然延续
  台词 = C
  结束状态 = State C
```

这比单纯写：

> `Clip 1 of 4`

稳定很多。

---

## 最核心的一点

你这个项目其实不是普通的：

**Image → Video**

而是：

**Reference Image → Controlled Video Segment → Temporal Continuity → Next Segment**

所以 Prompt 的核心优先级应该是：

```text
图片一致性
    ↓
人物一致性
    ↓
场景一致性
    ↓
动作连续性
    ↓
镜头连续性
    ↓
台词连续性
```

而不是：

```text
剧情动作
↓
镜头运动
↓
人物表演
```

**尤其如果你后面要把 4×10s 拼成一个 40s 视频，宁可每个 10s 的动作小一点，也不要为了“丰富动作”导致人物脸、服装和背景发生漂移。**

另外，你现在的 **Clip 1** 可以专门设计成“建立连续状态”的第一段；Clip 2–4 则应该采用同样的 Base Prompt，但分别描述上一段结束状态 → 当前图片状态 → 下一段结束状态。这样四段拼起来会比单纯要求“same character”稳定得多。
