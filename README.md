# AE & Figma Motion Replicator

一套基于 AI Agent 的 **2D 动效复刻 Skill**，同时支持 **Adobe After Effects** 与 **Figma 原生 Motion [Beta]** 双端自动搭建：输入一个参考 GIF 动效，自动完成逐帧拆解、透明分件生图（有生图能力直接出图，无生图能力则输出结构化提示词）、Alpha 自动切分去杂边，并直接写入 AE 合成或 Figma Motion [Beta] 时间轴关键帧。

## 目录结构

```text
ae-motion-replicator/
├── SKILL.md                       # Skill 主指令（GIF 拆解 / 切图 / AE & Figma Motion 双端规范）
├── scripts/
│   └── split_sprites.py           # GIF 逐帧联系表工具 & 透明合图自动切分去白边脚本
└── dist/
    └── ae-motion-replicator.skill # 打包好的 .skill 安装包，可直接分享导入
```

## 快速安装

### 方式一：直接下载 `.skill` 安装包
下载仓库中的 [`dist/ae-motion-replicator.skill`](dist/ae-motion-replicator.skill)，导入到支持 `.skill` 的 Agent（如 Antigravity / Claude Code）。

### 方式二：Git 克隆到本地 Skills 目录
```bash
git clone https://github.com/amiduai/ae-motion-replicator.git ~/.agents/skills/ae-motion-replicator
```
*(若使用 Antigravity，可再软链到 `~/.gemini/antigravity/skills/ae-motion-replicator`)*

## 依赖环境与 MCP 配置

1. **Python 3**：`pip install pillow numpy scipy`
2. **Adobe After Effects 端**：
   - macOS 下通过 `osascript`（ExtendScript）自动控制 AE，可选配 [after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp)
3. **Figma 原生 Motion [Beta] 端**：
   - 配置 **`localfig` MCP**（在 MCP 配置中添加 `npx -y localfig`）：
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
   - 在 Figma Desktop 中导入 `~/.localfig/plugin/manifest.json` 本地开发插件并打开桥接即可。
