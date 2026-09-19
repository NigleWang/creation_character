# Tagame 10s formula

Source analysis: `docs/anime.md`. Reusable playbook — **do not** reuse the same three lines every video.

**One-line job:** a mature muscular anime man talks **to the viewer** in Japanese. The emotional arc **must vary**. The classic invite → heat → possession is **one option**, never the only option.

## Must keep

1. **Same face + same body** as `characters/Tagame/references/face_01.jpeg`
2. **Direct address:** `おまえ` / 你. No third-person narrator
3. **Clothed tension:** heat / damp / closeness through fabric. No nudity
4. **Visual motif:** suit + tight white shirt (often sweat-damp) + undone buttons. Repeat; only change place and motion
5. **10s clips.** Default: 3 spoken lines, first line **at 2.0s**. Long user script → **N independent 10s clips** (3 lines each). Each clip is generated from its own reference image (clip 1 = still; clip 2+ = last frame of previous). They must **look like consecutive moments**, not like slices of one 40s render. Micro-motion only; do not push-in every clip; do not reset to the original still
6. **First frame hits:** low angle, imposing, wet/open shirt if chosen
7. **Anime lock:** never photoreal in prompt or stills
8. **Bilingual for publish:** Japanese speech in the model; Chinese (and original English if any) in chat for captions. Do not ask the model to render subtitles. Do not have him speak English in the i2v prompt

## Timing (structure only — beats are not always 邀请/热/占有)

| t | What happens | Motion |
|---|--------------|--------|
| 0.0–2.0s | Breath only | Blink, chest rise, inhale. No mute stare as the whole opening |
| **2.0s** | **Line 1** | First spoken line. Motion matches the **chosen arc** |
| ~4.5s | Line 2 | Second line. Slightly closer or a new micro-gesture |
| ~7.0s | Line 3 | Third line. Hold gaze |
| 9.5–10s | End hold | Short; do not freeze mute |

Solo **3 lines**, 6–14 mora each. First line **at 2.0s** (never later than 2.5s).

Always ひらがな / カタカナ in paste quotes. No 漢字.

---

## Turn C1 — read the still first, then 5 options (mandatory)

**Before any invented Japanese lines:** open the source still + scene card + bible. Write a short 【读图】block (place, time, pose, clothes, wet/dry, light, intensity, why he would speak). **Then** post **exactly 5** numbered dialogue sets. Then **STOP**.

**Skip this entire turn** if the user already pasted Japanese or English 台词 — go to C2 or C2-S.

Do **not** invent lines from the catalog without looking at this image. Do **not** write the video prompt in the same turn as the options.

### How to pick

1. **Read the original still first.** Extract: who (Tagame only), place, time, pose, outfit, wet/dry, lighting, camera, intensity. If a scene-card JSON exists, use it; if the user uploaded an older still, trust the pixels over a generic office default.
2. Lines must fit **this character** (mature office superior, `おまえ`, low voice, clothed tension) **and this scene**. A locker-room still cannot say hotel/rain/overtime; a dry shirt cannot claim sweat; a car still cannot talk about a hallway.
3. Choose **5 different arcs** from the catalog below — **5 different styles**, not one mood rewritten five times. **Never** five variants of 邀请→热→占有.
4. Match place first: 加班/走廊 → overtime or classic; 更衣室 → locker; 雨 → rain; 车 → car; 酒店 → hotel. Then mix moods that still make sense on **this** frame (温柔 / 命令 / 调戏 / 教学).
5. Honor intensity: 温柔 → prefer gentle / overtime-soft; 强势 → command / claim; 调戏 → tease / rain / car; 标准 → mix five styles.
6. Each option must differ in **arc_zh** (情绪弧) **and** speaking style. If two sets share the same three-beat labels or the same tone, rewrite one.
7. Prefer at least **one 好教** option (clear grammar: `～てみたい` / `だけ` / `んだぞ` / `おいで` / `まだ～ない`) so `douyin-caption` can teach it.
8. Scene-swap words (更衣室用 `まださめない`, 雨用 `ぬれ`, 加班用 `こんなじかん`) instead of always saying `むね` + `スーツごし` + `おまえだけ`.

Skip C1 only if the user **already pasted exact 台词** (Japanese or English, any length) or said「直接用第N套 / 用经典三段」in this conversation. English → spoken Japanese kana; long copy → C2-S (multiple 10s, continuous).

---

## User-supplied JP / EN script (C2 / C2-S)

1. Read the still first. Keep the user's plot; only wrap it in Tagame's mouth (`おまえ`, low, mature).
2. Japanese → kana. English → natural spoken Japanese → kana. Chat shows original + kana + 中文. Model speaks Japanese only.
3. Split into breath-lines of **6–16 mora**. Pack **3 lines per 10s clip**. Line 4+ starts the next clip.
4. **Continuity (C2-S):** each clip is **independently generated**. Clip 1 uploads the still; clip 2+ uploads the **last frame of the previous video** as the new source of truth. Same location/clothes/light because the **image** says so — if text conflicts, the image wins. Pose stays almost the same (breath, blink, mouth). Camera matches the current reference; only a tiny micro push-in; character stays the same size. Last 1s is an **intermediate frame**, not an ending (no fade, no freeze). Never write `Clip 1 of 4 in one continuous take` or `slow push-in toward chest` on every clip.
5. Each clip still opens the first spoken line at **2.0s**. Speak **only this clip's lines**. Do not improvise. Do not repeat previous clips.

---

## Arc catalog

Use these as **templates**. Change words so they fit **this still** (place, wet/dry, pose). Do not dump the whole catalog into chat — pick **5** different styles. Drop any template that contradicts the image.

### A. 邀请占有（经典，最多选 1 组）

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `このむね、さわってみたくないか？` | 这胸膛，不想摸摸看吗？ | ～てみたくないか |
| 2 | `スーツごしでもわかるくらい、あついんだぞ` | 隔着西装也能感觉到有多热 | ごし／んだぞ |
| 3 | `おまえだけのものだ` | 只属于你 | おまえだけ |

Motion: hand to chest → closer → smirk.

### B. 加班责问

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `こんなじかんまで、のこってたのか` | 都这时候了，你还留着？ | こんなじかん |
| 2 | `おまえのせいだ、かえれなくなる` | 都是你的错，我回不去了 | ～せいだ |
| 3 | `ほら、こっちをみろ` | 喂，看这边 | 命令形 |

Motion: glance then lock eyes → lean in → chin down at camera.

温柔替换 L1: `まだいたのか` / L3: `もう、すこしだけ`

### C. 命令靠近

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `こっち、おいで` | 过来 | おいで |
| 2 | `にげようとしても、むだだぞ` | 想逃也没用 | ～てもむだ |
| 3 | `おれのものだ。おまえのな` | 我的。你的也是 | ものだ |

Motion: beckon / two fingers → step into lens → hold.

强势可把 L1 改成 `いま、こい`

### D. 温柔允许

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `さわってみてもいいんだぞ` | 摸摸看也可以哦 | ～てもいい |
| 2 | `あったかいだろ` | 很暖和吧 | だろ（确认） |
| 3 | `おまえにだけだ` | 只给你 | にだけ |

Motion: slower; palm over shirt; small smile. Do not undo more buttons unless user asked.

### E. 调戏装没事

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `まだしらんぷりするか？` | 还要装作没事吗？ | しらんぷり |
| 2 | `こんなにあついのに` | 都这么热了 | こんなに～のに |
| 3 | `しょうじきになれよ` | 老实点 | 命令形 |

Motion: tilt head → closer → half-laugh smirk.

Do **not** default to genital / かたい lines. Only if user explicitly asks 调戏露骨, and stay clothed. If i2v refuses, drop it.

### F. 更衣室余热（健身房 / 刚运动）

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `うんどう、おわったばかりだ` | 刚练完 | たばかり |
| 2 | `まださめないんだ` | 还没凉下来 | まだ～ない |
| 3 | `ちゃんと、みろよ` | 给我好好看着 | 命令形 |

Motion: hand on chest/collar → breath → hold gaze.

### G. 雨湿

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `ぬれちまったな` | 湿透了啊 | ちまった（后悔/无奈） |
| 2 | `ぬれても、まだあつい` | 湿了也还是热 | ても |
| 3 | `にげんなよ` | 别跑啊 | なよ（禁止） |

Motion: wipe collar / shake rain → closer → stop-the-viewer look.

### H. 车里很近

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `せまいな` | 好挤啊 | な（感叹） |
| 2 | `にげられないぞ` | 逃不掉了 | ～られない |
| 3 | `こんやは、いかせない` | 今晚不让你走 | いかせない |

Motion: shift in seat toward camera → closer → hold. No grip / restraint wording in English motion (Gemini refusal).

### I. 酒店小声

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `しずかにしろ` | 安静点 | しろ |
| 2 | `こえ、だすなよ` | 别出声 | なよ |
| 3 | `こんやは、おまえのだ` | 今晚是你的 | のだ |

Motion: lean in, lower voice → closer → claim. Clothes on.

### J. 好教口语句（教学向，建议每轮至少 1 组）

| # | Kana | 中文 | 语法钩 |
|---|------|------|--------|
| 1 | `ちょっと、きいてくれ` | 听我说一句 | ～てくれ |
| 2 | `あつい、っていみ、わかるか` | 「热」是什么意思，懂吗 | ～っていう |
| 3 | `きょうのたんご、おまえだけだ` | 今天的单词：只属于你 | たんご／だけ |

Motion: point at own chest or at camera → lean in as if teaching → smirk on line 3. Still Tagame, not a classroom lecture.

Intensity swaps for J: 强势 L1 `きけ`; 温柔 L1 `ちょっと、いいか`

---

## Intensity

User picks one on the scene card. Default **标准**. Intensity **filters which arcs** you offer; it does not force 邀请→热→占有.

| 强度 | Prefer arcs | Avoid |
|------|-------------|--------|
| 温柔 | D, B-soft, J | C 强命令、E 过嘲 |
| **标准** | mix five styles (one may be A) | repeating A, or five sets in one mood |
| 强势 | C, I, B | D 过软 |
| 调戏 | E, G, H | A as the only option |

## Motion upgrades (clothed)

For **stills**, low angle + imposing pose is fine.

For **i2v**, convert any arc beat into **micro-motion only**: blink, breath, mouth, tiny head/eye. Do **not** write walk, step closer, hand-to-chest, big lean, or a push-in on every clip — those drift the face, clothes, and background when stitching 10s clips.

Optional if user asks and the still already supports it: undo one more button. Shirt stays on. Still no large arm motion in the video prompt.

## Places to rotate

办公室走廊（默认）→ 健身房更衣室 → 车里 → 酒店走廊 → 雨中 → 深夜加班。

Same man, same tone, new room **and** new dialogue arc.

## Avoid

- New face, slim body, pretty-boy, photoreal, Teo/Kai
- Pose-only, no speech
- Opening with 5s of silent eye contact
- Full nudity / starting already undressed
- Chinese-only speech in the model (JP speech + CN caption in chat)
- Third-person 旁白
- **Every video using A. 邀请占有** (`さわってみたくないか` / `スーツごし` / `おまえだけのものだ`)
- Writing the i2v prompt before the user picks a numbered option (unless they already pasted JP/EN lines)
- Writing C1 lines without first reading the still / scene card
- Five sets that share one style (all 邀请, all 命令, or five near-copies)
- Stuffing a long user script into one 10s clip
- Starting every clip from the original still pose (breaks continuity)
- Writing `Clip N of M in one continuous take` (model thinks it is slicing a longer video)
- Writing a slow push-in on every clip (gets closer and closer)
- Large story gestures in i2v (face/clothes/background drift)

## Gemini / i2v refusal

Trigger wording: gripping, restraint, "won't let go", explicit sex, fetish, domination-kneel.

Keep: fictional **anime** adult, clothes on, heat-through-fabric, おまえ.

If refused, rewrite once milder using catalog D or J. Keep `FICTION` + `ART STYLE LOCK` + no nudity. Do not resend the refused sentence.

## Voice

Low, unhurried, slightly breathy mature Japanese male. Optional light breath after line 2. No upbeat BGM in the prompt.
