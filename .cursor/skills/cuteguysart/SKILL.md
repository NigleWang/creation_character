---
name: cuteguysart
description: >-
  CuteGuysArt style prompts from docs/STYLE: glossy digital anime, warm skin
  gradients, cheek blush, large catchlight eyes, extreme V-taper. Use when the
  user says CuteGuysArt, Cute Guys Art, 风格 CuteGuysArt, 限定 CuteGuysArt, or
  points at docs/STYLE or docs/tagame_style.md. Supplies the style block only.
  Tagame identity, clothes, and dialogue stay in tagame-anime.
---

# CuteGuysArt

画风参考：`docs/STYLE/` 里的三张图。说明：`docs/tagame_style.md`。

用户点名 **CuteGuysArt** 才用。没点名时，Tagame 仍走默认日系动漫，不要套这套。

角色是 Tagame 时，身份、场景、衣服、台词、视频流程仍走 `tagame-anime`。本 skill 只提供要粘贴的画风段。脸图仍是 `characters/Tagame/references/face_01.jpeg`。

## 三张图里真正一致的东西

- 光泽数码动漫，不是彩铅，也不是只有硬边平涂
- 皮肤从桃色过渡到暖橙色，轮廓线加柔和渐变
- 肩、胸、手臂和头发上有高光
- 脸颊有暖红晕
- 眼睛大、湿润、有高光；大笑时可以眯成一条
- 短发有发丝高光；下颌有浅胡茬
- 胸肌、手臂、脖子极大，腰相对收，手大，上身比下身重
- 背景和人物是同一套插画：大块平涂、干净轮廓线、道具也是画出来的。没有照片景深、没有真实金属和玻璃质感
- 表情开朗、友好，不凶

风格参考里的网球场、白背心、彩虹袜、温泉、眼镜、裸胸，以及截图上的头像、爱心、页码、喇叭，都不是画风。用户没要那个场景，就不要画进去。

## 静帧：粘贴这一段

`{identity}`：Tagame 时写成深棕短刺发、棕色胡茬、方颌、约 40 岁，并写 Match the attached face reference。别的角色就写那个人的脸。

```text
CuteGuysArt style. Polished glossy digital anime illustration of a friendly hyper-muscular man. Clean dark outlines with moderate varied weight. Warm skin gradients from peach to sun-tan orange, muscle contours plus soft shading, glossy specular highlights on the shoulders, chest, arms, and hair. Warm blush on the cheeks. Large glossy anime eyes with catchlights, or a happy squint when he laughs. Thick eyebrows. Short hair with strand highlights. Light stubble on a strong jaw. A bright open smile or a gentle confident smile. Extremely bulky V-taper: huge chest, massive biceps and forearms, thick neck, narrower waist, large hands, upper body larger than the lower body. Saturated clear color. He fills most of the frame. Use a low angle when he is standing or in a heroic pose.

BACKGROUND — same illustration as the figure, not a photograph behind a drawn man:
The whole frame is one CuteGuysArt picture. Backdrop and props use the same clean dark outlines and large flat saturated shapes as docs/STYLE: simple drawn objects, open color fields, little texture. No photographic depth of field, no realistic metal, glass, concrete, or mirror reflections, no photo bokeh, no HDR room light. A gym, office, or street must still look drawn.

NOT photorealistic. NOT live-action. NOT 3D CGI. NOT a real photo background. NOT dry colored-pencil. NOT flat hard-cel only. NOT grim dark office anime.

{identity}
Do not slim him. Do not replace him with a different person.
Light stubble stays. Add light chest or arm hair only where bare skin is already part of the requested outfit. Do not force a heavy pelt.
Keep the scene wardrobe. Do not copy the style samples: tennis court, white tank top, denim or tennis shorts, rainbow socks, tinted glasses, hot spring, or a bare chest, unless the user asked for that place.
Do not copy interface chrome: profile circles, hearts, page numbers, speaker icons, or social-app margins.
```

Tagame 的 `{identity}` 用这句，不要再写 `High-quality Japanese anime`：

```text
The man is Tagame. Match the attached face reference: mature East Asian man about 40, dark-brown short slightly wavy spiked hair swept up, neat brown beard, square jaw, thick eyebrows. Redraw that same face in CuteGuysArt: glossy eyes with catchlights and a warm smile.
```

## 图生视频：替换 ART STYLE LOCK

成图已经是 CuteGuysArt 时，视频词用这段，不要写回日系细腻光影或彩铅硬边。

```text
ART STYLE LOCK:
Preserve the exact CuteGuysArt rendering of the reference image: glossy digital anime, warm peach-to-orange skin gradients, cheek blush, specular highlights on skin and hair, large catchlight eyes, clean dark outlines, extreme V-taper. Keep the background illustrated with the same outlines and flat color shapes. Do not turn the room into a photograph.
Do not convert him into photorealistic live action, flat hard-cel, colored pencil, or the default refined Japanese office illustration.
Do not make him look like a real person.
```

## QC

| 失败 | 原因 |
|------|------|
| 像照片或 3D，或背景比人物更写实 | 人物是插画、环境却像照片 |
| 只有灰暗办公室细线动漫 | 没点到这套光泽暖色 |
| 干巴巴的彩铅、没有高光和腮红 | 还是旧提示词 |
| 出现网球场、彩虹袜、温泉、白背心，或头像爱心页码 | 把参考图内容抄进来了 |
| 人被画瘦、没了胡茬或发色不对 | 身份丢了 |
