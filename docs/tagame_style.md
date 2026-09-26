# CuteGuysArt

风格名：**CuteGuysArt**。只有用户点名这个名字才用。默认 Tagame 仍是日系动漫。

可粘贴提示词在 `.cursor/skills/cuteguysart/SKILL.md`。参考图在 `docs/STYLE/`，只锁定画法，不锁定场景和衣服。

人如果是 Tagame：深棕短刺发、棕色胡茬、方颌仍锁 `characters/Tagame/references/face_01.jpeg`。

## 从三张参考图里看到的画法

1. **渲染：** 光泽数码动漫。干净的深色轮廓线，线不算极粗。皮肤是桃色到暖橙色的柔和渐变，肌肉用轮廓线加重，肩、胸、手臂和头发有高光。脸颊有暖红晕。不是彩铅，也不是只有一块块硬边平涂。
2. **脸：** 短发有发丝高光。下颌浅胡茬。眼睛大、湿润、有高光；大笑时可以眯眼。眉毛浓。表情是露齿笑或轻轻的自信笑，友好，不凶。
3. **体型：** 胸肌、二头肌、前臂和脖子极大，腰相对收，手大，上身比下身重。
4. **身体毛发：** 脸上是浅胡茬。胸口和手臂的毛很淡，只在裸露皮肤上出现，不是每张图都有厚胸毛。
5. **构图：** 人物占满画面。站立或英雄姿态常用仰拍。气氛健康、阳光、好接近。
6. **背景：** 和人物同一套插画。大块平涂、干净轮廓线，哑铃、树、球拍都是画出来的。没有照片景深，没有真实金属、玻璃或水泥质感。

参考图里的网球场、白背心、短裤、彩虹袜、有色眼镜、夜景温泉、裸胸，以及截图上的头像、爱心、页码和喇叭，都不要带进别的场景。

## 静帧提示词

`{identity}` 在 Tagame 出图时换成 skill 里的 Tagame 身份句。

```text
CuteGuysArt style. Polished glossy digital anime illustration of a friendly hyper-muscular man. Clean dark outlines with moderate varied weight. Warm skin gradients from peach to sun-tan orange, muscle contours plus soft shading, glossy specular highlights on the shoulders, chest, arms, and hair. Warm blush on the cheeks. Large glossy anime eyes with catchlights, or a happy squint when he laughs. Thick eyebrows. Short hair with strand highlights. Light stubble on a strong jaw. A bright open smile or a gentle confident smile. Extremely bulky V-taper: huge chest, massive biceps and forearms, thick neck, narrower waist, large hands, upper body larger than the lower body. Saturated clear color. He fills most of the frame. Use a low angle when he is standing or in a heroic pose.

BACKGROUND — same illustration as the figure, not a photograph behind a drawn man:
The whole frame is one CuteGuysArt picture. Backdrop and props use the same clean dark outlines and large flat saturated shapes as the style references: simple drawn objects, open color fields, little texture. No photographic depth of field, no realistic metal, glass, concrete, or mirror reflections, no photo bokeh, no HDR room light.

NOT photorealistic. NOT live-action. NOT 3D CGI. NOT a real photo background. NOT dry colored-pencil. NOT flat hard-cel only. NOT grim dark office anime.

{identity}
Do not slim him. Do not replace him with a different person.
Light stubble stays. Add light chest or arm hair only where bare skin is already part of the requested outfit. Do not force a heavy pelt.
Keep the scene wardrobe. Do not copy the style samples: tennis court, white tank top, denim or tennis shorts, rainbow socks, tinted glasses, hot spring, or a bare chest, unless the user asked for that place.
Do not copy interface chrome: profile circles, hearts, page numbers, speaker icons, or social-app margins.
```

## 视频画风锁

```text
ART STYLE LOCK:
Preserve the exact CuteGuysArt rendering of the reference image: glossy digital anime, warm peach-to-orange skin gradients, cheek blush, specular highlights on skin and hair, large catchlight eyes, clean dark outlines, extreme V-taper. Keep the background illustrated with the same outlines and flat color shapes. Do not turn the room into a photograph.
Do not convert him into photorealistic live action, flat hard-cel, colored pencil, or the default refined Japanese office illustration.
Do not make him look like a real person.
```
