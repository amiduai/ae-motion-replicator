---
name: ae-motion-replicator
description: Replicate 2D game/UI animations from reference GIFs into Adobe After Effects, Figma native Motion [Beta], or lightweight HTML+GSAP web animations automatically. Covers GIF frame-by-frame breakdown, adaptive sprite-sheet generation, alpha-based sprite splitting with edge decontamination, ExtendScript automation for AE, Figma Motion [Beta] via localfig MCP, and zero-software HTML+GSAP rendering via Playwright+ffmpeg. Use when the user asks to analyze a reference animation GIF, generate sprite-sheet prompts, split sprite sheets, or replicate an animation in AE, Figma Motion, or HTML/GSAP.
---

# AE / Figma / Web Motion Replicator (2D 动效复刻流水线)

一套支持 **Adobe After Effects**、**Figma 原生 Motion [Beta]** 与 **轻量 HTML+GSAP（零重型软件）** 三端输出的 2D 动效复刻工作流：
`参考 GIF 拆解` → `透明分件合图（直出或提示词）` → `Python 自动切图去杂边` → `AE / Figma Motion / HTML+GSAP 自动构建` → `视觉验收`。

---

## Step 1：参考 GIF 逐帧拆解

拿到参考 GIF 路径后，先用内置脚本导出帧序列、元数据与带帧号标注的联系表：

```bash
python3 ~/.agents/skills/ae-motion-replicator/scripts/split_sprites.py inspect-gif <gif_path> <out_dir>
```

用 `read_file` 查看生成的 `contact_sheet.png` 及关键帧，输出 3 项核心结论：
1. **基础参数与动作节奏**：总帧数、总时长、单帧延迟（含停顿帧）、5 段节奏（待机 → 挤压蓄力 → 弹开/爆发 → 过冲回弹 → 淡出重置）。
2. **软件可程序化生成的特效（无需出图）**：径向光晕、垂直/放射光束、四角星芒粒子、扫光、高光泛光。
3. **最少静态透明分件清单**：通常只需 2–4 个结构件（例如：底座、闭合态组件、开启态组件）。
   - **特殊艺术字/造型字体规则**：若参考动效中包含**游戏质感立体艺术字、金属斜角描边字或特殊手写/造型字体**（非普通系统扁平字），**同样作为独立静态透明分件放进合图里生图**（不要硬用系统字体代替）；后续在 AE 中通过「复制亮部高光层 + 羽化斜扫蒙版」即可对图片字做丝滑扫光。

---

## Step 2：生成透明分件精灵合图（有生图能力则直出，否则输出提示词）

根据 Step 1 确定的「最少静态透明分件清单」，构造下方结构化英文提示词：

```text
Create a 2D casual mobile game UI sprite sheet (component sheet) of <主体描述>, arranged horizontally with <N> separate static parts on a 100% pure transparent background (PNG with alpha channel).

Art Style & Perspective:
- <画风描述，如：Casual mobile game 2D hand-painted vector-like illustration style, clean smooth shading, rounded bevels>.
- Consistent <视角描述，如：3/4 top-down angled> perspective across all parts, matching scale and lighting.

Layout & Separation Rules (CRITICAL):
- Place the <N> parts side by side in a single horizontal row with generous empty transparent spacing between each part. No overlapping, no touching edges.
- Pure transparent background ONLY. NO checkerboard pattern, NO gray/white grid, NO drop shadows, NO ground shadows, NO glow, NO light beams, NO sparkles, NO particles, NO text, NO guide lines.

The <N> Exact Parts (from left to right):
1. [Left] <分件 1 名称与结构细节>
2. [Center] <分件 2 名称与结构细节>
3. [Right] <分件 3 名称与结构细节>
```

### 执行策略（按环境能力自动分支）
1. **环境具备生图能力时（优先直出）**：
   - 若当前 Agent 拥有生图子智能体（如 `image-generator`）或生图 MCP/工具，**直接调用生图**；
   - 若生图工具仅支持纯白底 JPG/PNG（如 `#FFFFFF`），切图前先用外围连通域泛洪抠除纯白背景并做边缘柔化去杂色，再进入 **Step 3**。
2. **环境无生图能力时（降级输出提示词）**：
   - 将上述填好内容的英文提示词直接输出给用户，等待用户发给 GPT 生图后回传合图文件再继续 **Step 3**。

---

## Step 3：透明合图自动切分与边缘去杂色

拿到透明合图后，运行内置脚本自动按透明通道横向投影切分（并用距离变换替换半透明边缘像素 RGB，彻底消除白边/黑边杂色）：

```bash
python3 ~/.agents/skills/ae-motion-replicator/scripts/split_sprites.py split <sprite_sheet.png> <out_dir> [--names part_0,part_1,part_2]
```

切分后务必用 `read_file` 目视检查每个独立 PNG 的完整度与边缘干净度。

---

## Step 4A：Adobe After Effects 自动建合成与打关键帧

使用 `osascript -e 'tell application "Adobe After Effects 2027" to DoScriptFile "<script.jsx>"'`（可先用 `after-effects` MCP 检查桥接连通性）。

### ExtendScript 编写铁律（避坑清单）
1. **避免保存弹窗阻塞**：新建工程前先静默关闭旧工程：
   ```javascript
   if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
   var proj = app.newProject();
   ```
2. **强制使用语言无关 Match Name**（兼容中文/英文 AE）：
   - 变换：`ADBE Transform Group`、`ADBE Anchor Point`、`ADBE Position`、`ADBE Scale`、`ADBE Rotate Z`、`ADBE Opacity`
   - 效果：`ADBE Effect Parade`、`ADBE Brightness & Contrast 2`、`ADBE Gaussian Blur 2`、`ADBE Glo2`
   - 矢量/蒙版：`ADBE Root Vectors Group`、`ADBE Vector Group`、`ADBE Vectors Group`、`ADBE Vector Shape - Star`、`ADBE Vector Graphic - Fill`、`ADBE Mask Parade`、`ADBE Mask Atom`
3. **`setTemporalEaseAtKey` 数组长度规则**：
   - `TwoD_SPATIAL`（Position）、`ThreeD_SPATIAL`、`OneD`（Opacity / Rotation）必须传 **1 元数组** `[ease]`；
   - 非空间二维属性 `TwoD`（Scale）必须传 **2 元数组** `[ease, ease]`。
4. **透明底特效防黑边与防矩形裁切**：
   - 导入 PNG 时显式设置 `item.mainSource.alphaMode = AlphaMode.STRAIGHT;`。
   - **禁止**对小尺寸 Shape Layer 直接加超大半径 `Gaussian Blur 2`（易在图层紧密包围盒处出现矩形硬裁切）；改用 **Comp 尺寸 Solid + 羽化蒙版**。
5. **打开预览、保存与视觉验收**：
   - 结尾调用 `comp.openInViewer();` 并 `proj.save(new File(aepPath));`，再导出关键帧 PNG（`comp.saveFrameToPng`）用 `read_file` 验收。

---

## Step 4B：Figma 原生 Motion [Beta] 自动搭建（via `localfig` MCP）

当用户要求在 **Figma** 中用原生 **Motion [Beta]** 复刻时，通过 `localfig` MCP（`npx -y localfig`）驱动：

1. **上传透明分件**：先用 `figma_eval` 创建对应尺寸的占位矩形，再调用 `figma_place_image`（`scaleMode: "FIT"`）把本地切好的 PNG 上传到画布。
2. **构建扁平主画板**：创建单个主画板（如 `480 × 480`），将所有分件、光晕、光束、矢量星芒作为**直属子图层**平铺在画板内，方便在 Motion 时间轴直接查看与调整。
3. **调用 Figma 原生 Motion [Beta] Plugin API 写关键帧**：
   ```javascript
   // 设置总时长与循环播放
   frame.setTimelineDuration(frame.id, 3.06);
   frame.playbackSettings = { autoplay: true, loop: true, muted: false };

   // 为图层写入关键帧轨道
   node.applyManualKeyframeTrack(
     { type: "PROPERTY", name: propName }, // 支持 OPACITY, TRANSLATION_X, TRANSLATION_Y, SCALE_X, SCALE_Y, ROTATION, WIDTH, HEIGHT
     {
       keyframes: [
         { timelinePosition: 0.0, value: { type: "FLOAT", value: 1 }, easing: { type: "LINEAR" } },
         { timelinePosition: 0.78, value: { type: "FLOAT", value: 0 }, easing: { type: "EASE_IN_AND_OUT" } }
       ]
     },
     frame.id
   );
   ```
   - **1 帧硬切技巧**：在 `t - 0.001` 与 `t` 处放置一对 `LINEAR` 关键帧实现瞬切（如 `0.779s: 1` → `0.780s: 0`）。
   - **纯 Alpha 防黑边光效**：径向光晕用外环同色 `a: 0` 渐变 + `LAYER_BLUR`；星芒用矢量 `STAR`（4 角）+ 金色柔光 `DROP_SHADOW`。
4. **视觉验收**：调用 `figma_export` 导出关键帧 PNG，用 `read_file` 验收后选中主画板聚焦，提示用户按空格即可预览。


---

## Step 4C：轻量 Web 引擎自动搭建（HTML + GSAP，零重型软件依赖）

当用户不需要打开 AE 或 Figma，希望用最轻量方式直接预览、嵌入前端或导出透明 GIF/MP4 时：

1. **生成单文件动效 HTML**：
   - 将切分好的透明 PNG 分件以相对路径（或 Base64）引入绝对定位舞台容器；
   - 使用 **GSAP**（`gsap.timeline({ repeat: -1 })`）精确编写挤压拉伸（`scaleX/scaleY` + `transformOrigin: "bottom center"`）、过冲回弹（`back.out` / `elastic.out`）、径向渐变光晕（`radial-gradient(..., transparent)` 无黑边）、垂直光柱与 SVG 4 角星芒粒子；
   - **必须暴露确定性时间跳转钩子**，方便无头浏览器逐帧导出：
     ```javascript
     window.__seek = (t) => { tl.pause(); tl.seek(t); };
     ```
2. **浏览器预览与确定性导出 GIF/MP4**：
   - 用户可直接双击 HTML 在浏览器实时观看（支持直接复用进 Web/小程序 WebView）；
   - 如需导出 GIF / MP4（支持 `--transparent` 纯透明底），运行内置脚本：
     ```bash
     python3 ~/.agents/skills/ae-motion-replicator/scripts/render_web_gif.py <index.html> <out.gif> --duration 3.06 --fps 25 --width 480 --height 480 --transparent
     ```
   - 导出后用 `read_file` 查看 GIF 或抽帧检查，确认无闪烁与裁切问题。
