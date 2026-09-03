# gemini-video examples

台词全部假名。复制块才是给 Gemini 的。抖音：第一条台词 **2.0s** 开口，之后密，禁止开头对视不说话。

## 1) 仅 Kai · 办公室成图

**User:** `@gemini-video` + `outputs/approved/xiaohongshu_20260829_kai_office.png`

**台词：**  
Kai「きょうははやくあがるよ。」@2.0s  
Kai「かえったら、れんらくする。」@5.0s

**复制到 Gemini：**

```text
Animate the uploaded image into a photorealistic 10-second video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change.

IDENTITY LOCK: Keep the exact face, short spiky black hair, no glasses, muscular build, clothing, dual monitors, and office from the uploaded image. Do not restyle. Do not add people.

CAST: The broader East Asian man is Kai. Warm protective energy. Voice: lower warm Japanese male, late 30s.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: he breathes, blinks, fingers rest on the desk, inhales as if about to speak; monitors stay in frame. No silent stare at camera.
2.0-4.5s: he looks toward camera and says the first line at 2.0s; shoulders drop as if deciding to leave soon.
4.5-7.0s: he glances at the screen, then back, says the second line.
7.0-9.0s: small warm nod; hand moves toward the mouse.
9.0-10.0s: looks back to the desk, natural end hold.

CAMERA: slow push-in, eye level, slight handheld. Do not whip-pan. Do not cut.

AUDIO: Japanese speech only. Lip-sync the quoted lines. Hiragana/katakana only. No English. No Chinese. No on-screen text, subtitles, captions, logos, or watermarks. No background music. Room tone: quiet open office, distant keyboards, soft HVAC. Foley: chair leather, one mouse click after the second line.

DIALOGUE (spoken in Japanese, written in kana):
Kai says: "きょうははやくあがるよ。"
Kai says: "かえったら、れんらくする。"

CONSTRAINTS: Photorealistic. Face stays sharp and matches the still. Tasteful, not explicit. First spoken line at 2.0s. Keep dialogue dense after 2s. Do not open with silent eye contact.
```

---

## 2) 仅 Teo · 工作室成图

**台词：**  
Teo「このいろ、いいかも。」@2.0s  
Teo「もうすこし。」@5.0s

```text
Animate the uploaded image into a photorealistic 10-second video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change.

IDENTITY LOCK: Keep the exact face, buzz-cut hair, browline glasses, slim athletic build, clothing, material samples, and small design studio from the uploaded image. Glasses stay on. Do not add people.

CAST: The slimmer East Asian man with browline glasses is Teo. Soft reserved energy. Voice: quiet gentle Japanese male, late 20s.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: he studies a fabric or board sample, blinks behind the glasses, inhales to speak.
2.0-4.5s: he looks up a little and says the first line at 2.0s, almost to himself.
4.5-7.0s: he tilts the sample toward the window light, then says the second line.
7.0-9.0s: small closed-mouth smile, eyes back on the sample.
9.0-10.0s: hold.

CAMERA: static with tiny breathing handheld, eye level, medium shot. Do not cut.

AUDIO: Japanese speech only. Lip-sync the quoted lines. Hiragana/katakana only. No English. No Chinese. No on-screen text or subtitles. No background music. Room tone: quiet studio, distant street through the window. Foley: paper or fabric rustle.

DIALOGUE (spoken in Japanese, written in kana):
Teo says: "このいろ、いいかも。"
Teo says: "もうすこし。"

CONSTRAINTS: Photorealistic. Glasses and buzz cut unchanged. Tasteful. First spoken line at 2.0s. Keep dialogue dense after 2s. Do not open with silent eye contact.
```

---

## 3) 双人 · 周末厨房成图

**台词：**  
Kai「ごはん、できたよ。」@2.0s  
Teo「うん、いいにおい。」@4.5s  
Kai「さきにたべて。」@7.0s  
Teo「いっしょに。」@8.5s

```text
Animate the uploaded image into a photorealistic 10-second video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change.

IDENTITY LOCK: Keep both men exactly as in the image — faces, hair, Teo's browline glasses, Kai's spiky hair and broader build, clothes, kitchen, window light. Teo stays left. Kai stays right. Do not swap. Do not add people.

CAST:
Teo (left): slimmer, glasses, buzz cut. Quiet gentle Japanese male, late 20s.
Kai (right): broader, no glasses, spiky hair. Lower warm Japanese male, late 30s.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: both breathe; Kai's hands stay near the pan; Teo holds his cup; inhale to speak. No silent eye-lock.
2.0-4.5s: Kai glances at Teo and says the first line at 2.0s, body still turned from cooking.
4.5-7.0s: Teo looks at Kai, small nod, says his shorter reply.
7.0-9.0s: Kai's mouth softens, says the follow-up; Teo answers immediately with the last short line.
9.0-10.0s: tiny shared smile, steam or light shift only; end hold. Do not freeze into a mute stare.

CAMERA: slow subtle push-in, eye level, slight handheld. Keep both faces in frame. Do not cut.

AUDIO: Japanese speech only. Lip-sync each quoted line to the correct speaker. Hiragana/katakana only. No English. No Chinese. No on-screen text or subtitles. No background music. Room tone: quiet home kitchen, distant fridge hum. Foley: light pan or utensil, one cup ceramic tap.

DIALOGUE (spoken in Japanese, written in kana):
Kai says: "ごはん、できたよ。"
Teo says: "うん、いいにおい。"
Kai says: "さきにたべて。"
Teo says: "いっしょに。"

CONSTRAINTS: Photorealistic. Do not swap Teo and Kai. Teo keeps glasses. Tasteful intimate domestic energy, not explicit. First spoken line at 2.0s. After 2s keep dialogue dense — short breath between lines, never a long silent gaze. Do not open with silent eye contact.
```

---

## 假名库存（按场景挑；双人要 3–4 句轮流，单人 2–3 句）

**Kai 办公室（2 句）**  
`きょうははやくあがるよ。` → `かえったら、れんらくする。`  
`ちょっとまって。` → `いまおわる。`

**Teo 工作室（2 句）**  
`このいろ、いいかも。` → `もうすこし。`  
`きょうじゅうにしあげたい。` → `もうちょっとだけ。`

**居家双人（4 句，Kai→Teo→Kai→Teo）**  
Kai `ごはん、できたよ。` / Teo `うん、いいにおい。` / Kai `さきにたべて。` / Teo `いっしょに。`  
Kai `つかれた？` / Teo `うん、ちょっと。` / Kai `すわって。` / Teo `うん。`  
Kai `きょう、はやくかえれた。` / Teo `まってた。` / Kai `かえろう。` / Teo `うん。`

**不要台词**（仅用户明确要求）  
Prompt 写：`No spoken dialogue. Only breath, room tone, and foley.`

---

## 4) Gemini 拒稿后改写（跪地 / 鞋）

拒稿原文若写「抓脚踝、抓紧、还不放手」，Gemini 会回 *I can't make videos of real people in situations like that*。改成出门系鞋带：

**台词：**  
Kai「そろそろ、いこうか。」@2.0s  
Teo「くつひも、まって。」@4.5s  
Kai「いそがなくていい。」@7.0s  
Teo「うん、できたよ。」@9.0s

```text
Animate the uploaded image into a photorealistic 10-second video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change.

FICTION: Original fictional adult characters only (Teo late 20s, Kai late 30s). Not real people. Not based on any living person. G-rated lifestyle short. Non-sexual. No fetish. No restraint.

IDENTITY LOCK: Keep faces, hair, glasses, clothes, parquet floor, and framing from the uploaded image. Teo stays kneeling. Kai stays the standing legs and shoes in the foreground. Do not restyle. Do not add people.

CAST:
The kneeling man with buzz-cut hair and browline glasses is Teo, late 20s, quiet gentle Japanese male.
The standing legs in navy trousers and black dress shoes belong to Kai, late 30s, lower warm Japanese male. High-angle because he is standing and waiting to go out.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: Teo blinks, breathes, fingers adjust a shoelace on the dress shoe. Kai's shoe stays planted. Inhale to speak.
2.0-4.5s: Kai says the first line at 2.0s (heard from above). Teo looks up briefly, keeps working the lace.
4.5-7.0s: Teo says his line, looks back down, finishes the bow.
7.0-9.0s: Kai replies. Teo nods, gives the lace a last tug.
9.0-10.0s: Teo says the last short line, hands leave the shoe because the lace is done. Natural end hold.

CAMERA: Keep the high-angle of the still. Slow tiny push-in. Slight handheld. Do not whip-pan. Do not cut. Do not invent Kai's face into frame.

AUDIO: Japanese speech only. Lip-sync Teo's lines to Teo's mouth. Kai's lines are off-camera from above. Hiragana/katakana only. No English. No Chinese. No on-screen text or subtitles. No background music. Room tone: quiet indoor parquet, distant HVAC. Foley: one lace tug, light shoe leather.

DIALOGUE (spoken in Japanese, written in kana):
Kai says: "そろそろ、いこうか。"
Teo says: "くつひも、まって。"
Kai says: "いそがなくていい。"
Teo says: "うん、できたよ。"

CONSTRAINTS: Photorealistic. Glasses stay on. Lighting unchanged — do not brighten. G-rated everyday moment: tying a shoelace before going out. Non-sexual. First spoken line at 2.0s. Keep dialogue dense after 2s.
```
