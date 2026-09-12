# tagame-anime examples

## 1) Turn A — 用户只说角色

**User:** `@Tagame` 按 anime 方案出一条

场景卡 **不要** 预填「邀请 → 身体热度 → 占有」，也 **不要** 贴定稿三句。

```text
✅ Tagame 场景已按人设补全（动漫画风锁定，可改）

【谁】仅 Tagame，对镜头里的「你」
【时间地点】深夜加班后 · 公司办公室走廊
【构图】3:4 中近景，仰拍
【第一帧】双手插腰，白衬衫汗湿贴身，解开两颗扣，直视镜头
【服装】紧身白衬衫（汗湿）、黑西裤、黑皮带银扣；外套未穿
【光】走廊冷色灯，正常曝光不要提亮
【情绪强度】标准
【台词】出图后先读成图设定，再给 5 组不同风格的日语台词（贴合本角+本场景），你选一组再写图生视频提示词

快捷：「生成」
⏸️ 请确认后再出图。
```

---

## 2) Turn B — 静帧 prompt 要点

身份 + 动漫锁定 + 仰拍第一帧。参考图只有 Tagame 脸。

关键句必须出现：`High-quality Japanese anime`、`NOT photorealistic`、`Match the attached character reference`、`LOW-ANGLE`。

出图通过后 **进入 C1**，不要直接写 i2v。

---

## 3) Turn C1 — 走廊成图 → 台词选项（STOP）

**User:** 成图已通过 / `@outputs/approved/tagame_20260905_office_corridor.png` 图生视频

必须先写【读图】，再给 **5 种不同风格**，不能 5 组都是摸胸邀请，也不能忽略走廊/加班/汗湿衬衫这些成图事实。

```text
✅ 台词选项（先读成图，再按本角+本场景写；选一组后我再写 10 秒图生视频提示词）

【读图】
地点：公司办公室走廊
时间：深夜加班后
姿态：双手插腰，直视镜头 · 镜头：仰拍中近景
服装：紧身白衬衫汗湿、解开两颗扣、黑西裤
光 / 强度：走廊冷色灯 · 标准
本图能说：他在空楼里拦住还没走的你

【谁】仅 Tagame，对镜头（お前）——办公室肌肉上司

1️⃣ 【加班责问】深夜留人 ·好教
1 こんなじかんまで、のこってたのか ｜ 都这时候了，你还留着？（こんなじかん）
2 おまえのせいだ、かえれなくなる ｜ 都是你的错，我回不去了
3 ほら、こっちをみろ ｜ 喂，看这边

2️⃣ 【命令靠近】
1 こっち、おいで ｜ 过来（おいで）
2 にげようとしても、むだだぞ ｜ 想逃也没用
3 おれのものだ。おまえのな ｜ 我的。你的也是

3️⃣ 【温柔允许】
1 さわってみてもいいんだぞ ｜ 摸摸看也可以哦（～てもいい）
2 あったかいだろ ｜ 很暖和吧
3 おまえにだけだ ｜ 只给你

4️⃣ 【教学向】·好教
1 ちょっと、きいてくれ ｜ 听我说一句（～てくれ）
2 あつい、っていみ、わかるか ｜ 「热」是什么意思，懂吗
3 きょうのたんご、おまえだけだ ｜ 今天的单词：只属于你

5️⃣ 【邀请占有】经典一组（备选，不是默认）
1 このむね、さわってみたくないか？ ｜ 这胸膛，不想摸摸看吗？
2 スーツごしでもわかるくらい、あついんだぞ ｜ 隔着西装也能感觉到有多热
3 おまえだけのものだ ｜ 只属于你

回复编号即可。
⏸️ 请选择后再生成图生视频提示词。
```

本回合 **没有** 英文复制块。

---

## 4) Turn C2 — 用户回 `1`（加班责问）

【情绪弧】加班责问  
动作：对上镜头 → 靠近 → 下巴压向镜头，**不要**写成手摸胸口公式。

**台词：**  
Tagame「こんなじかんまで、のこってたのか」@2.0s  
Tagame「おまえのせいだ、かえれなくなる」@4.5s  
Tagame「ほら、こっちをみろ」@7.0s

**复制到模型：**（MOTION 跟弧走）

```text
Animate the uploaded image into a 10-second ANIME video. Image-to-video. Use the uploaded image as frame 0 / first frame. Duration: 10 seconds. Aspect ratio: 9:16 vertical. Single continuous shot, no cuts, no new locations, no costume change, no nudity.

ART STYLE LOCK: Keep high-quality Japanese anime / digital illustration look of the still. Do NOT restyle into photorealistic live action. Do NOT turn him into a real person.

FICTION: Original fictional adult anime character only (Tagame, about 40). Not a real person. Not based on any living person. Suggestive but clothed. No explicit nudity.

IDENTITY LOCK: Keep the exact anime face, dark-brown short spiked hair, brown beard, extreme musculature, sweat-damp white shirt, black trousers, corridor, and lighting from the uploaded image. Do not add people. Do not slim him.

CAST: The muscular anime man is Tagame. He speaks directly to the viewer. Voice: low, slightly breathy mature Japanese male.

MOTION (10s, continue this pose, do not freeze):
0.0-2.0s: chest rises with breath, blink, fingers stay on hips, inhale to speak. Low angle unchanged.
2.0-4.5s: first line at 2.0s; he glances as if catching someone still in the building, then locks eyes with the camera.
4.5-7.0s: second line; he leans a little closer; shirt stays on.
7.0-9.5s: third line; chin dips toward camera, “look here” beat; small smirk.
9.5-10.0s: short end hold on face and chest.

CAMERA: low-angle slow push-in toward chest and face. Do not whip-pan. Do not cut.

AUDIO: Japanese speech only. Lip-sync the quoted lines. Hiragana/katakana only. No English. No Chinese. No on-screen text, subtitles, captions, logos, or watermarks. No background music. Room tone: quiet office corridor, distant HVAC. Foley: shirt cotton, one soft footstep, breath.

DIALOGUE (spoken in Japanese, written in kana; he is talking to YOU):
Tagame says: "こんなじかんまで、のこってたのか"
Tagame says: "おまえのせいだ、かえれなくなる"
Tagame says: "ほら、こっちをみろ"

CONSTRAINTS: Anime, not photoreal. Clothes stay on. First spoken line at 2.0s. Dense talk after 2s. Direct address only.
```

同一回合再出抖音文案（见 `douyin-caption` examples）。

---

## 5) 强度改温柔

C1 应多给 D 温柔允许、B 加班软化、J 教学向；少给命令/调戏。  
不要只把经典三段换成温柔同义词还叫「邀请→占有」。

---

## 6) 已有成图、只要视频词

**User:** `@outputs/approved/tagame_20260905_office_corridor.png` 图生视频

跳过 Turn A/B。**先读成图设定** → **C1 五组不同风格 STOP**。用户选编号后才 C2。画风句仍要 `ANIME` / `NOT photorealistic`。台词必须吃进这张图的地点/服装/姿态。

---

## 7) 用户直接贴台词

跳过 C1。转成假名后走 C2 + `douyin-caption`。

---

## 8) 拒稿后改写

若模型拒「触摸/占有」过强：改用目录 D 或 J，整段重新贴复制块，不要只发 diff。保留 ART STYLE LOCK + FICTION + 衣服不脱。
