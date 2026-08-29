# Pose Catalog

Pick 6–8 items that fit the locked environment. Skip anything that would force a location change.

Ids are stable (use in `pose_series_*.json`). Display names are Chinese for chat options.

## office

| id | Name | Action |
|----|------|--------|
| `desk_work` | 伏案工作 | Sit forward at desk, both hands on keyboard, eyes on dual monitors |
| `phone_call` | 打电话 | Sit, phone to one ear, other hand on chair arm or desk |
| `look_camera` | 看镜头 | Sit facing camera, hands on thighs or chair arms, slight smile |
| `lean_back` | 靠背放松 | Lean back in mesh chair, one hand behind head, other on armrest |
| `coffee` | 端咖啡 | Sit, hold a ceramic mug, glance at camera or window |
| `stand_desk` | 站在桌边 | Stand beside desk, one hand on chair back, look at camera |
| `read_files` | 翻文件 | Sit, look down at stacked papers, one hand turning a page |
| `side_sit` | 侧身倚椅 | Sit angled, forearm on chair back, look back toward camera |
| `chin_hand` | 托腮思考 | Elbow on desk, chin on fist, gaze off to the side |

Source pose for typical office still: arms crossed in chair → do **not** offer `arms_crossed` as a series pick.

## cafe

| id | Name | Action |
|----|------|--------|
| `cup_two_hands` | 捧杯 | Both hands on cup, looking at camera |
| `window_seat` | 看窗外 | Body toward window, profile or 3/4, cup on table |
| `lean_table` | 伏桌 | Forearms on table, slight forward lean, eye contact |
| `phone_scroll` | 滑手机 | Looking down at phone, relaxed shoulders |
| `chair_turn` | 转身看镜头 | Seated, torso turned toward camera |

## home

| id | Name | Action |
|----|------|--------|
| `sofa_relax` | 沙发靠坐 | Deep sit, one arm on backrest |
| `read` | 看书 | Book in hands, downward gaze |
| `kitchen_stand` | 厨房站姿 | Stand at counter, mug or pan in hand |
| `window_light` | 窗边 | Stand or sit in window light, looking out then back |

## outdoor

| id | Name | Action |
|----|------|--------|
| `walk` | 走路 | Mid-stride, one foot forward, natural arm swing |
| `pocket` | 插口袋 | Stand, hands in pockets, look at camera |
| `lean_wall` | 靠墙 | Shoulder to wall, ankles crossed |
| `look_back` | 回眸 | Walk away, head turned back to camera |

## couple (Tom left, James right — never swap)

Only if source already has both. Keep relative left/right.

| id | Name | Action |
|----|------|--------|
| `walk_side` | 并肩走 | Side by side, same direction |
| `sit_close` | 并坐 | Seated close, James slightly more upright |
| `look_each` | 对视 | Facing each other, eye contact |
| `from_behind` | 背后环抱 | James behind or beside, arm around Tom |

## Chat option lines

Format each option as:

```text
1️⃣ {Name}：{Action one-liner}
```

Offer 2 shortcuts:

- **日常三连** — 3 poses that tell a mini story (work → pause → look at camera)
- **全套** — all listed options this turn
