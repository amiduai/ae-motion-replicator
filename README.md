# AE Motion Replicator

一套基于 AI Agent + Adobe After Effects 的 **2D 动效复刻 Skill**：输入一个参考 GIF 动效，自动完成逐帧拆解、透明分件生图（有生图能力直接出图，无生图能力则输出结构化提示词）、Alpha 自动切分去杂边，并通过 ExtendScript 自动在 AE 中建合成、打弹性关键帧、生成纯 Alpha 光效/星芒并导出验收。

## 目录结构

```text
ae-motion-replicator/
├── SKILL.md                    # Skill 主指令（4 步 SOP + AE ExtendScript 避坑规范）
├── scripts/
│   └── split_sprites.py        # GIF 逐帧联系表工具 & 透明合图自动切分去白边脚本
└── dist/
    └── ae-motion-replicator.skill  # 打包好的 .skill 安装包，可直接分享导入
```

## 快速安装

### 方式一：直接下载 `.skill` 安装包
下载仓库中的 [`dist/ae-motion-replicator.skill`](dist/ae-motion-replicator.skill)，导入到支持 `.skill` 的 Agent（如 Antigravity / Claude Code）。

### 方式二：Git 克隆到本地 Skills 目录
```bash
git clone https://github.com/amiduai/ae-motion-replicator.git ~/.agents/skills/ae-motion-replicator
```
*(若使用 Antigravity，可再软链到 `~/.gemini/antigravity/skills/ae-motion-replicator`)*

## 依赖环境
- Python 3（`pillow`, `numpy`, `scipy`）
- Adobe After Effects（macOS 下通过 `osascript` / `after-effects` MCP 驱动 ExtendScript）
