# Tagame 10s formula

Source analysis: `docs/anime.md`. This file is the reusable playbook. Do not invent a new hook each time.

**One-line job:** a mature muscular anime man flirts at the viewer and claims possession — not a beauty showcase.

## Must keep

1. **Same face + same body** as `characters/Tagame/references/face_01.jpeg`
2. **Direct address:** `おまえ` / 你. No third-person narrator
3. **Body sensation through clothes:** 熱 / 湿 / 隔着西装也能感觉到 / 只属于你
4. **Visual motif:** suit + tight white shirt (often sweat-damp) + undone buttons. Repeat; only change place and motion
5. **10s three-beat:** invite → body heat → possession
6. **First frame hits:** low angle, imposing, wet/open shirt if chosen
7. **Anime lock:** never photoreal in prompt or stills
8. **Bilingual for publish:** Japanese speech in the model; Chinese translation in chat for burned-in captions. Do not ask the model to render subtitles (garbled text)

## Three-beat timing

| t | Beat | Motion default |
|---|------|----------------|
| 0.0–2.0s | Breath only | Blink, chest rise, inhale. No mute stare as the whole opening |
| **2.0s** | **Invite** | First line. Hand to chest or lean toward camera |
| ~4.5s | Heat | Second line. Closer; fabric tension |
| ~7.0s | Possession | Third line. Hold gaze, slight smirk |
| 9.5–10s | End hold | Short; do not freeze mute |

Solo **3 lines**, 6–14 mora each. First line **at 2.0s** (never later than 2.5s). Dense talk after 2s.

## Default lines (proven)

| Beat | Kana | 中文 |
|------|------|------|
| Invite | `このむね、さわってみたくないか？` | 这胸膛，不想摸摸看吗？ |
| Heat | `スーツごしでもわかるくらい、あついんだぞ` | 隔着西装也能感觉到有多热 |
| Possession | `おまえだけのものだ` | 只属于你 |

Always ひらがな / カタカナ in the paste quotes. No 漢字.

## Intensity

User picks one. Default **标准**.

| 强度 | Invite | Heat | Possession |
|------|--------|------|------------|
| 温柔 | `さわってみてもいいんだぞ` | `あったかいだろ` | `おまえにだけだ` |
| **标准** | default above | default | default |
| 强势 | `さわってみろ。いま` | `スーツごしでも、わかるだろ` | `おれのものだ。おまえのな` |
| 调戏 | `まだしらんぷりするか？` | `こんなにあついのに` | `にげられないぞ` |

Do **not** default to genital / かたい lines. That belongs only to 调戏 if the user explicitly asks, and must stay clothed. If the i2v model refuses, drop it and use 标准.

Scene-specific swaps (keep three-beat):

| Place | Heat line idea |
|-------|----------------|
| 更衣室 | `まださめない` |
| 车里 | `せまいな。にげられないぞ`（调戏时） |
| 雨中 | `ぬれても、まだあつい` |
| 加班 | `こんなじかんまで、おまえのせいだ` |

Possession should stay some form of 只属于你 / おまえだけ.

## Motion upgrades (clothed)

Low angle → hand on chest → closer to camera.

Optional if user asks and still supports it: undo one more button, take the viewer's implied hand toward the chest (camera as POV), pull the viewer closer. Shirt stays on.

## Places to rotate

办公室走廊（默认）→ 健身房更衣室 → 车里 → 酒店走廊 → 雨中 → 深夜加班。

Same man, same tone, new room.

## Avoid

- New face, slim body, pretty-boy, photoreal, Teo/Kai
- Pose-only, no speech
- Opening with 5s of silent eye contact
- Full nudity / starting already undressed
- Chinese-only speech in the model (JP speech + CN caption in chat)
- Third-person 旁白

## Gemini / i2v refusal

Trigger wording: gripping, restraint, "won't let go", explicit sex, fetish, domination-kneel.

Keep: fictional **anime** adult, clothes on, heat-through-fabric, おまえだけ.

If refused, rewrite once milder:

1. `こっち、おいで`
2. `まださめないんだ`
3. `おまえだけだ`

Keep `FICTION` + `ART STYLE LOCK` + no nudity. Do not resend the refused sentence.

## Voice

Low, unhurried, slightly breathy mature Japanese male. Optional light breath after line 2. No upbeat BGM in the prompt.
