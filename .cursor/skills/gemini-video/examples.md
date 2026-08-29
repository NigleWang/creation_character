# gemini-video examples

台词全部假名。复制块才是给 Gemini 的。

## 1) 仅 James · 办公室成图

**User:** `@gemini-video` + `outputs/approved/xiaohongshu_20260829_james_office.png`

**台词：** James「きょうははやくあがるよ。」

**复制到 Gemini：**

```text
Animate the uploaded image into a photorealistic 10-second video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change.

IDENTITY LOCK: Keep the exact face, short spiky black hair, no glasses, muscular build, clothing, dual monitors, and office from the uploaded image. Do not restyle. Do not add people.

CAST: The broader East Asian man is James. Warm protective energy. Voice: lower warm Japanese male, late 30s.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: he breathes, blinks, fingers rest on the desk; monitors stay in frame.
2.0-5.5s: he glances at the screen, then looks toward camera, shoulders drop as if deciding to leave soon.
5.5-8.0s: he says the line with a small warm smile; slight nod.
8.0-10.0s: he looks back to the desk, hand moves toward the mouse, natural end hold.

CAMERA: slow push-in, eye level, slight handheld. Do not whip-pan. Do not cut.

AUDIO: Japanese speech only. Lip-sync the quoted line. Hiragana/katakana only. No English. No Chinese. No on-screen text, subtitles, captions, logos, or watermarks. No background music. Room tone: quiet open office, distant keyboards, soft HVAC. Foley: chair leather, one mouse click after the line.

DIALOGUE (spoken in Japanese, written in kana):
James says: "きょうははやくあがるよ。"

CONSTRAINTS: Photorealistic. Face stays sharp and matches the still. Tasteful, not explicit. Natural pause after the line. Do not fill all 10 seconds with talking.
```

---

## 2) 仅 Tom · 工作室成图

**台词：** Tom「このいろ、いいかも。」

```text
Animate the uploaded image into a photorealistic 10-second video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change.

IDENTITY LOCK: Keep the exact face, buzz-cut hair, browline glasses, slim athletic build, clothing, material samples, and small design studio from the uploaded image. Glasses stay on. Do not add people.

CAST: The slimmer East Asian man with browline glasses is Tom. Soft reserved energy. Voice: quiet gentle Japanese male, late 20s.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: he studies a fabric or board sample, blinks behind the glasses.
2.0-5.5s: he tilts the sample toward the window light, head slightly down.
5.5-8.0s: he looks up a little and says the line, almost to himself.
8.0-10.0s: small closed-mouth smile, looks back at the sample, hold.

CAMERA: static with tiny breathing handheld, eye level, medium shot. Do not cut.

AUDIO: Japanese speech only. Lip-sync the quoted line. Hiragana/katakana only. No English. No Chinese. No on-screen text or subtitles. No background music. Room tone: quiet studio, distant street through the window. Foley: paper or fabric rustle.

DIALOGUE (spoken in Japanese, written in kana):
Tom says: "このいろ、いいかも。"

CONSTRAINTS: Photorealistic. Glasses and buzz cut unchanged. Tasteful. Natural pause. Do not fill 10 seconds with talking.
```

---

## 3) 双人 · 周末厨房成图

**台词：**  
James「ごはん、できたよ。」  
Tom「うん、いいにおい。」

```text
Animate the uploaded image into a photorealistic 10-second video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change.

IDENTITY LOCK: Keep both men exactly as in the image — faces, hair, Tom's browline glasses, James's spiky hair and broader build, clothes, kitchen, window light. Tom stays left. James stays right. Do not swap. Do not add people.

CAST:
Tom (left): slimmer, glasses, buzz cut. Quiet gentle Japanese male, late 20s.
James (right): broader, no glasses, spiky hair. Lower warm Japanese male, late 30s.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: both breathe; James's hands stay near the pan or counter; Tom holds his cup.
2.0-5.5s: James glances at Tom and says his line, body still turned from cooking.
5.5-8.0s: Tom looks at James, small nod, says his shorter line.
8.0-10.0s: James's mouth softens; they hold the look; steam or light shift only; end hold.

CAMERA: slow subtle push-in, eye level, slight handheld. Keep both faces in frame. Do not cut.

AUDIO: Japanese speech only. Lip-sync each quoted line to the correct speaker. Hiragana/katakana only. No English. No Chinese. No on-screen text or subtitles. No background music. Room tone: quiet home kitchen, distant fridge hum. Foley: light pan or utensil, one cup ceramic tap.

DIALOGUE (spoken in Japanese, written in kana):
James says: "ごはん、できたよ。"
Tom says: "うん、いいにおい。"

CONSTRAINTS: Photorealistic. Do not swap Tom and James. Tom keeps glasses. Tasteful intimate domestic energy, not explicit. Pause between the two lines. Do not fill all 10 seconds with talking.
```

---

## 假名库存（按场景挑，不要堆）

**James 办公室**  
`ちょっとまって。いまおわる。`  
`きょうははやくあがるよ。`  
`かえったら、れんらくする。`

**Tom 工作室**  
`このいろ、いいかも。`  
`もうすこし。`  
`きょうじゅうにしあげたい。`

**居家双人**  
James `つかれた？` / Tom `うん、ちょっと。`  
James `ごはん、つくるよ。` / Tom `いっしょに。`  
James `きょう、はやくかえれた。` / Tom `まってた。`

**不要台词**  
Prompt 写：`No spoken dialogue. Only breath, room tone, and foley.`
