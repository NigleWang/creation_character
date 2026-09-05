# tagame-anime examples

## 1) Turn A — 用户只说角色

**User:** `@Tagame` 按 anime 方案出一条

```text
✅ Tagame 场景已按人设补全（动漫画风锁定，可改）

【谁】仅 Tagame，对镜头里的「你」
【时间地点】深夜加班后 · 公司办公室走廊
【构图】3:4 中近景，仰拍
【第一帧】双手插腰，白衬衫汗湿贴身，解开两颗扣，直视镜头
【服装】紧身白衬衫（汗湿）、黑西裤、黑皮带银扣；外套未穿
【光】走廊冷色灯，正常曝光不要提亮
【情绪强度】标准
【10秒三段】邀请 → 身体热度 → 占有
【台词预览】
1 このむね、さわってみたくないか？ ｜ 这胸膛，不想摸摸看吗？
2 スーツごしでもわかるくらい、あついんだぞ ｜ 隔着西装也能感觉到有多热
3 おまえだけのものだ ｜ 只属于你

快捷：「生成」
⏸️ 请确认后再出图。
```

---

## 2) Turn B — 静帧 prompt 要点

身份 + 动漫锁定 + 仰拍第一帧。参考图只有 Tagame 脸。

关键句必须出现：`High-quality Japanese anime`、`NOT photorealistic`、`Match the attached character reference`、`LOW-ANGLE`。

---

## 3) Turn C — 走廊成图 → 10s

**台词：**  
Tagame「このむね、さわってみたくないか？」@2.0s  
Tagame「スーツごしでもわかるくらい、あついんだぞ」@4.5s  
Tagame「おまえだけのものだ」@7.0s

**复制到模型：**

```text
Animate the uploaded image into a 10-second ANIME video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 3:4 vertical. Single continuous shot, no cuts, no new locations, no costume change, no nudity.

ART STYLE LOCK: Keep high-quality Japanese anime / digital illustration look of the still. Do NOT restyle into photorealistic live action. Do NOT turn him into a real person.

FICTION: Original fictional adult anime character only (Tagame, about 40). Not a real person. Not based on any living person. Suggestive but clothed. No explicit nudity.

IDENTITY LOCK: Keep the exact anime face, dark-brown short spiked hair, brown beard, extreme musculature, sweat-damp white shirt, black trousers, corridor, and lighting from the uploaded image. Do not add people. Do not slim him.

CAST: The muscular anime man is Tagame. He speaks directly to the viewer. Voice: low, slightly breathy mature Japanese male.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: chest rises with breath, blink, fingers stay on hips, inhale to speak. Low angle unchanged.
2.0-4.5s: first line at 2.0s; right hand moves from hip to the open shirt over his chest.
4.5-7.0s: second line; he leans a little closer to camera; fabric stays on the body.
7.0-9.5s: third line; holds the gaze with a small smirk.
9.5-10.0s: short end hold on face and chest.

CAMERA: low-angle slow push-in toward chest and face. Do not whip-pan. Do not cut.

AUDIO: Japanese speech only. Lip-sync the quoted lines. Hiragana/katakana only. No English. No Chinese. No on-screen text, subtitles, captions, logos, or watermarks. No background music. Room tone: quiet office corridor, distant HVAC. Foley: shirt cotton, one soft footstep, breath.

DIALOGUE (spoken in Japanese, written in kana; he is talking to YOU):
Tagame says: "このむね、さわってみたくないか？"
Tagame says: "スーツごしでもわかるくらい、あついんだぞ"
Tagame says: "おまえだけのものだ"

CONSTRAINTS: Anime, not photoreal. Clothes stay on. First spoken line at 2.0s. Dense talk after 2s. Direct address only.
```

---

## 4) 强度改温柔（仍三段）

`さわってみてもいいんだぞ` → `あったかいだろ` → `おまえにだけだ`

Motion 更慢、手只覆在衬衫上，不更解开扣子。

---

## 5) 已有成图、只要视频词

**User:** `@outputs/approved/tagame_20260905_office_corridor.png` 图生视频

跳过 Turn A/B。读图 → 按公式写 Turn C。画风句仍要 `ANIME` / `NOT photorealistic`。

---

## 6) 拒稿后改写

若模型拒「触摸/占有」过强：

`こっち、おいで` → `まださめないんだ` → `おまえだけだ`

保留 ART STYLE LOCK + FICTION + 衣服不脱。整段重新贴复制块，不要只发 diff。
