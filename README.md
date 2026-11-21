# AE & Figma Motion Replicator

> **给 AI 一张参考 GIF，全自动拆帧分析 → AI 生图并切分透明分件 → 自动写入 Adobe After Effects 合成 & Figma 原生 Motion [Beta] 时间轴关键帧！**

---

## 实测效果对比（原图动画 vs AI 全自动复刻 GIF）

以下 **5 个完整游戏 UI / 特效动画**均由本 Skill 自动拆解、生成/切分透明分件，并在 **Adobe After Effects 2027** 中全自动打帧渲染导出：

### 1.「恭喜通关」破土金奖杯动效
> 自动拆解为「奖杯 + 土堆」2 个静态分件，AE 内自动搭建破土遮罩弹出、弹性回弹、纯 Alpha 爆光白烟、12 枚彩纸屑抛物线、双层描边艺术字扫光与收尾星芒。

| 参考原图 | AI 全自动复刻效果（AE 渲染） |
| :---: | :---: |
| ![恭喜通关原图](assets/trophy_original.gif) | ![恭喜通关复刻](assets/trophy_replicated.gif) |

### 2.「失败」结算徽章动效
> 自动拆解为「银冠 + 紫盾 + 冰银单翼（镜像复用）」3 个静态分件，AE 内自动完成王冠弹出、盾牌与双翼展开、紫蓝爆光冲击波，以及结尾王冠向左歪斜 `-12°` 的趣味细节。

| 参考原图 | AI 全自动复刻效果（AE 渲染） |
| :---: | :---: |
| ![失败结算原图](assets/defeat_original.gif) | ![失败结算复刻](assets/defeat_replicated.gif) |

### 3. 卡通宝箱开启动效（AE + Figma Motion 双端复刻）
> 自动拆解为「底座 + 闭合盖 + 开启盖」3 个透明分件，实现挤压蓄力 → 瞬切开盖过冲 → 径向光晕 & 垂直光束 → 四角星芒扩散。

| 参考原图 | AI 全自动复刻效果（AE 渲染） |
| :---: | :---: |
| ![宝箱开启原图](assets/chest_original.gif) | ![宝箱开启复刻](assets/chest_replicated.gif) |

### 4. 胜利徽章展翼横幅动效
> 自动拆解皇冠、双翼、飘带、盾牌底座等透明分件，AE 内自动完成展翼弹性展开、金色扫光、金币喷发与粒子闪烁。

| 参考原图 | AI 全自动复刻效果（AE 渲染） |
| :---: | :---: |
| ![胜利徽章原图](assets/victory_original.gif) | ![胜利徽章复刻](assets/victory_replicated.gif) |

### 5. 炸弹炸塔动效
> 自动拆解石塔、炸弹、旗帜等 13 个透明分件，AE 内自动完成炸弹抛物线砸塔、爆炸冲击波、烟尘与碎片四溅。

| 参考原图 | AI 全自动复刻效果（AE 渲染） |
| :---: | :---: |
| ![炸弹炸塔原图](assets/bomb_original.gif) | ![炸弹炸塔复刻](assets/bomb_replicated.gif) |

---

## 傻瓜式一键安装（按需三选一，复制发给你的 AI 助手）

无论你使用的是哪种 AI Agent，不用自己敲命令，按你常用的软件**三选一**复制下方提示词发给 AI 即可自动配好：

### 方案 A：仅安装 After Effects 版
```text
请帮我一键安装并配置 https://github.com/amiduai/ae-motion-replicator 的 After Effects 环境：
1. 克隆仓库并安装到你当前 Agent 对应的全局 Skills 目录；
2. 检查并安装 Python 依赖：pip install pillow numpy scipy；
3. 安装 After Effects MCP（https://github.com/Dakkshin/after-effects-mcp）：克隆到 ~/mcp-servers/after-effects-mcp，执行 npm install && npm run build && npm run install-bridge，并写入我的 MCP 配置文件（node ~/mcp-servers/after-effects-mcp/build/index.js）；
4. 检查配置无误后，告诉我最后需要在 AE 里手动打开哪个桥接面板。
```

### 方案 B：仅安装 Figma 原生 Motion [Beta] 版
```text
请帮我一键安装并配置 https://github.com/amiduai/ae-motion-replicator 的 Figma Motion 环境：
1. 克隆仓库并安装到你当前 Agent 对应的全局 Skills 目录；
2. 检查并安装 Python 依赖：pip install pillow numpy scipy；
3. 配置 Figma MCP（https://github.com/LucasGorgal/localfig）：在我的 MCP 配置文件中加入 localfig（command: "npx", args: ["-y", "localfig"]）；
4. 检查配置无误后，告诉我如何在 Figma Desktop 中导入 ~/.localfig/plugin/manifest.json 开启桥接面板。
```

### 方案 C：极简轻量版（HTML + GSAP，免装 AE / Figma）
```text
请帮我一键安装并配置 https://github.com/amiduai/ae-motion-replicator 的轻量 Web 动效环境：
1. 克隆仓库并安装到你当前 Agent 对应的全局 Skills 目录；
2. 安装 Python 依赖：pip install pillow numpy scipy playwright && playwright install chromium；
3. 检查本机是否已安装 ffmpeg（如未安装则提示或通过 brew/apt 安装）；
4. 全部完成后告诉我，以后我发参考 GIF 就可以直接走 HTML + GSAP 方案生成浏览器可预览代码并导出透明 GIF。
```

---

## 分步手动操作提示词（不装 Skill 也能直接用）

如果你想自己一步步控制节奏，或者只发给普通对话 AI，直接按顺序复制以下 3 段提示词即可：

### 第 1 步：拆解参考动效（GIF / 视频）
```text
帮我拆解这个动效（路径：<你的GIF路径>）：
1. 分析它的总帧数、总时长、单帧间隔、动作节奏（蓄力/爆发/回弹/停顿），以及用到了哪些光效和粒子；
2. 如果要复刻它，最少需要拆成哪几个静态透明分件？（能用软件生成的光晕、光柱、星芒、粒子不用出图；特殊立体艺术字单独算分件）；
3. 写出直接发给 GPT 生图的英文提示词：要求一次生成一张纯透明背景、同画风同视角、间距拉开的「分件精灵合图」。
```

### 第 2 步：GPT 透明分件精灵合图模板
```text
Create a 2D casual mobile game UI sprite sheet (component sheet) of <主体描述>, arranged horizontally with <N> separate static parts on a 100% pure transparent background (PNG with alpha channel).

Art Style & Perspective:
- <画风描述，如：Casual mobile game 2D hand-painted vector-like illustration style, clean smooth shading, rounded bevels>.
- Consistent <视角描述，如：3/4 top-down angled> perspective across all parts, matching scale and lighting.

Layout & Separation Rules (CRITICAL):
- Place the <N> parts side by side in a single horizontal row with generous empty transparent spacing between each part. No overlapping, no touching edges.
- Pure transparent background ONLY. NO checkerboard pattern, NO gray/white grid, NO drop shadows, NO ground shadows, NO glow, NO light beams, NO sparkles, NO particles, NO text, NO guide lines.

The <N> Exact Parts (from left to right):
1. [Left] <分件1名称及结构描述>
2. [Center] <分件2名称及结构描述>
3. [Right] <分件3名称及结构描述>
```
*(若生图带了棋盘格背景或零件宽度不一致，追加：)*

### 第 3 步：自动切图去白边 + 生成动效（三选一）
```text
这是我生成的透明分件合图（路径：<合图路径>），请帮我：
1. 用 Python 按透明通道自动裁切拆分成独立的透明 PNG 分件，并清理边缘半透明白边杂色；
2. 按第 1 步拆解的节奏搭建动效（任选其一）：
   - [AE 版] 通过 ExtendScript / after-effects MCP 自动导入 AE，对齐锚点、打好挤压拉伸与过冲关键帧，用纯 Alpha 渐变/矢量补充光束与星芒（防黑边/防裁切），打开合成并保存 .aep；
   - [Figma Motion 版] 通过 localfig MCP 传图并调用 Figma 原生 Motion [Beta] API（applyManualKeyframeTrack）写入时间轴关键帧；
   - [轻量 Web 版] 生成单文件 HTML + GSAP 动效（暴露 window.__seek(t)），并用 Playwright + ffmpeg 导出透明 GIF。
```

---

## 手动安装与依赖清单

### 1. 安装 Skill
- **方式 A（直接导入）**：下载 [`dist/ae-motion-replicator.skill`](dist/ae-motion-replicator.skill) 导入到你的 Agent。
- **方式 B（Git 克隆）**：
  ```bash
  git clone https://github.com/amiduai/ae-motion-replicator.git ~/.agents/skills/ae-motion-replicator
  pip install pillow numpy scipy
  ```

### 2. 配置 Adobe After Effects MCP（可选，macOS 亦支持 osascript 直连）
仓库地址：[Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp)
```bash
git clone https://github.com/Dakkshin/after-effects-mcp.git ~/mcp-servers/after-effects-mcp
cd ~/mcp-servers/after-effects-mcp
npm install && npm run build && npm run install-bridge
```
在 `mcp_config.json` 中添加：
```json
{
  "mcpServers": {
    "after-effects": {
      "command": "node",
      "args": ["/你的用户目录/mcp-servers/after-effects-mcp/build/index.js"]
    }
  }
}
```
> 使用前在 AE 顶部菜单打开 **窗口 → 扩展 / 脚本 → MCP Bridge Auto**。

### 3. 配置 Figma 原生 Motion [Beta] MCP（第三方开源依赖）
依赖开源项目：[LucasGorgal/localfig](https://github.com/LucasGorgal/localfig)（MIT License）。在 `mcp_config.json` 中添加：
```json
{
  "mcpServers": {
    "localfig": {
      "command": "npx",
      "args": ["-y", "localfig"]
    }
  }
}
```
> 首次运行会在 `~/.localfig/plugin/manifest.json` 生成本地桥接插件，在 Figma Desktop 中通过 **Plugins → Development → Import plugin from manifest** 导入并保持开启即可。

---

## 仓库目录结构

```text
ae-motion-replicator/
├── SKILL.md                        # Skill 主指令（GIF 拆解 / 生图 / 切图 / AE & Figma Motion 规范）
├── scripts/
│   ├── split_sprites.py            # GIF 逐帧联系表工具 & 透明合图自动切分去白边脚本
│   └── render_web_gif.py           # 轻量 HTML/GSAP 确定性逐帧导出透明 GIF/MP4 脚本
├── dist/
│   └── ae-motion-replicator.skill  # 打包好的 .skill 安装包，可直接下载导入
├── assets/                         # 5 组原图 vs 复刻 GIF 对比素材
└── README.md
```
