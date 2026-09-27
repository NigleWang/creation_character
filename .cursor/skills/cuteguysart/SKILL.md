---
name: cuteguysart
description: >-
  CuteGuysArt style prompts from docs/tagame_style.md: wholesome muscular
  cartoon, bold hand-drawn contour lines, cel-plus-painterly warm skin,
  medium kind eyes, bright saturated lifestyle scenes. Use when the user
  says CuteGuysArt, Cute Guys Art, 风格 CuteGuysArt, 限定 CuteGuysArt, or
  points at docs/STYLE or docs/tagame_style.md. Supplies the style block
  only. Tagame identity, clothes, and dialogue stay in tagame-anime.
---

# CuteGuysArt

风格限定：`docs/tagame_style.md`。参考图：`docs/STYLE/`。

用户点名 **CuteGuysArt** 才用。没点名时，Tagame 仍走默认日系动漫，不要套这套。

角色是 Tagame 时，身份、场景、衣服、台词、视频流程仍走 `tagame-anime`。本 skill 只提供要粘贴的画风段。脸图仍是 `characters/Tagame/references/face_01.jpeg`。不要把风格文档里的 28–35 岁、190cm 写进 Tagame。

一句话：成年、强壮、亲和的猛男，用粗线条现代卡通画出来，加上柔和肌肉光影、暖肤色和高饱和的生活场景。

## 必须锁住的特征

- 成年猛男。宽肩、粗臂、胸肌明显、腹肌可见、大腿和小腿都有肌肉、手脚偏大。头身比例偏真实。写 `powerful but natural muscular physique`。不要 `bishounen`、`pretty boy`、`slim anime boy`，也不要 `extreme bodybuilder` 或健美比赛体。
- 亲和帅脸，不是霸总脸。粗眉、方颌、浅胡茬、短发、温暖自信的笑。眼睛中等、有神。不要过大的二次元眼睛。
- 轮廓线粗、干净、略带手绘的深色墨线。不要极细动漫线，也不要无线稿数字油画。
- 上色是赛璐璐加柔和笔触：暖肤色、平滑过渡、暖橙褐阴影、皮肤上的柔和高光。不是纯平涂，也不是照片皮肤。
- 高明度、高饱和、暖肤、明亮。不要暗调、低饱和、高级灰、电影感压色。
- 背景和人物是同一张插画，而且是具体的生活场景：能认出的日常道具、清楚的活动。不要人像加虚化照片背景。

风格参考里的网球场、白背心、彩虹袜、温泉、眼镜、裸胸，以及截图上的头像、爱心、页码、喇叭，都不是画风。用户没要那个场景，就不要画进去。

情绪是阳光、好相处，带一点日常反差。不要把画风段写成脱衣、健身房展示或危险性感。

## 静帧：粘贴这一段

`{identity}`：Tagame 时用下面的 Tagame 句。别的角色就写那个人的脸，并锁成这套画法。

```text
CuteGuysArt style. A charming adult muscular male character illustrated in a modern high-end cartoon illustration style.

Strong masculine physique with very broad shoulders, large muscular arms, defined chest, visible abdominal muscles, thick muscular thighs, powerful legs, large hands and feet, and natural athletic proportions. Powerful but natural muscular physique.

Handsome but approachable masculine face, strong jawline, thick eyebrows, short textured hair, subtle beard stubble, warm expressive medium-sized eyes, friendly confident smile, and wholesome masculine charm.

Bold clean contour lines, expressive hand-drawn ink outlines, slightly textured linework, simplified but sophisticated cartoon forms.

Stylized cel shading combined with soft painterly rendering, smooth tonal transitions, warm natural skin tones, subtle orange-brown shadows, soft skin highlights, gentle ambient occlusion, and carefully rendered muscle definition.

Bright cheerful color palette, vibrant colors, warm sunlight, high color contrast, clean luminous lighting, playful and optimistic visual atmosphere.

Detailed environmental illustration with recognizable everyday objects, natural background storytelling, cinematic but cheerful composition, strong character silhouette, dynamic natural pose. The whole frame is one illustration. Backdrop and props use the same bold contour lines and bright saturated color as the figure. No photographic depth of field, no realistic metal, glass, concrete, or mirror reflections, no photo bokeh.

Premium digital illustration, polished commercial artwork, expressive character acting, appealing masculine character design, wholesome masculine charm, playful humor, visually rich but clean composition.

NOT photorealistic. NOT live-action. NOT 3D CGI. NOT a real photo background. NOT bishounen. NOT a pretty boy. NOT oversized anime eyes. NOT thin manga linework. NOT extreme bodybuilder. NOT a bodybuilding competition. NOT dark moody color. NOT desaturated. NOT flat hard-cel only. NOT lineless digital painting.

{identity}
Do not slim him. Do not replace him with a different person. Do not turn him into a teenager or a fashion model.
Light stubble stays. Add a little chest or arm hair only where bare skin is already part of the requested outfit. Do not force a heavy pelt.
Keep the scene wardrobe and the requested place. Do not copy the style samples: tennis court, white tank top, denim or tennis shorts, rainbow socks, tinted glasses, hot spring, or a bare chest, unless the user asked for that place.
Do not copy interface chrome: profile circles, hearts, page numbers, speaker icons, or social-app margins.
```

Tagame 的 `{identity}` 用这句，不要再写 `High-quality Japanese anime`：

```text
The man is Tagame. Match the attached face reference: mature East Asian man about 40, dark-brown short slightly wavy spiked hair swept up, neat brown beard, square jaw, thick eyebrows. Redraw that same face in CuteGuysArt: medium kind eyes, warm confident smile, approachable masculine features. Do not give him oversized anime eyes.
```

## 图生视频：替换 ART STYLE LOCK

成图已经是 CuteGuysArt 时，视频词用这段。不要写回日系细线、暗调办公室，也不要写成大眼睛光泽倒三角。

```text
ART STYLE LOCK:
Preserve the exact CuteGuysArt rendering of the reference image: modern cartoon illustration, bold clean hand-drawn contour lines, cel shading mixed with soft painterly skin, warm skin tones with orange-brown shadows and soft highlights, medium expressive eyes, wholesome masculine face, bright saturated color, and a detailed illustrated everyday background. Keep the powerful natural muscular build, including thick thighs.
Do not convert him into photorealistic live action, 3D CGI, a pretty boy, oversized anime eyes, thin manga linework, an extreme bodybuilder, dark moody grading, or the default refined Japanese office illustration.
Do not make him look like a real person.
```

## QC

| 失败 | 原因 |
|------|------|
| 像照片、3D，或背景比人物更写实 | 整张图必须是同一套卡通插画 |
| 细线暗调日系办公室 | 没点到粗线、暖色、高饱和 |
| 眼睛过大，或变成美少年 | 风格文档明确排除 |
| 健美比赛体，或人被画瘦、腿细 | 要自然的大型肌肉，含粗腿 |
| 线又细又干净像普通动漫，或完全没有轮廓线 | 要粗的手绘墨线 |
| 发灰、发暗、低对比 | 要明亮高饱和 |
| 出现网球场、彩虹袜、温泉、白背心，或头像爱心页码 | 把参考图内容抄进来了 |
| 没了胡茬或发色不对 | 身份丢了 |
