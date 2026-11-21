# AE & Figma Motion Replicator

> **给 AI 一张参考 GIF，全自动拆帧分析 → 生成/切分透明分件 → 写入 Adobe After Effects 合成 & Figma 原生 Motion [Beta] 时间轴关键帧！**

---

## 实测还原效果展示

### 案例一：游戏「恭喜通关」破土奖杯动效（After Effects 全自动搭建）
从参考 GIF 自动拆解出「奖杯 + 土堆」2 个静态分件，AI 生图并自动抠除白底去杂边后，通过 ExtendScript 自动在 AE 中完成：**破土遮罩弹出 + 弹性回弹 + 纯 Alpha 爆光白烟 + 12 枚红绿彩纸屑 + 双层描边艺术字扫光 + 尾帧星芒**。

| 破土爆发（0.24s） | 艺术字斜向扫光（0.68s） | 收尾星芒闪烁（0.98s） |
| :---: | :---: | :---: |
| ![破土爆发](assets/trophy_ae_burst.png) | ![艺术字扫光](assets/trophy_ae_sweep.png) | ![星芒闪烁](assets/trophy_ae_sparkle.png) |

---

### 案例二：卡通宝箱开启动效（AE + Figma 原生 Motion [Beta] 双端复刻）
3 分件（底座 + 闭合盖 + 开启盖）自动切分去白边后，直接通过 `localfig` MCP 调用 Figma 官方 **Motion [Beta] Plugin API**，一次性将 17 个图层的 3.06s 关键帧轨道写入时间轴，按空格即可预览。

| 开盖爆发光束（Figma Motion） | 星芒粒子扩散（Figma Motion） |
| :---: | :---: |
| ![开盖爆发](assets/chest_figma_burst.png) | ![星芒扩散](assets/chest_figma_sparkles.png) |

---

## 傻瓜式一键安装（复制这一段发给你的 AI 助手）

如果你使用的是 **Antigravity / Claude Code / Cursor** 等 AI Agent，不用自己敲命令，**直接复制下面这段提示词发给 AI**，它会自动帮你把 Skill、Python 环境、`after-effects` MCP 和 `localfig` MCP 全部配好：

```text
请帮我一键安装并配置 https://github.com/amiduai/ae-motion-replicator 的全部运行环境：
1. 克隆仓库到 ~/.agents/skills/ae-motion-replicator（如使用 Antigravity 请同步软链到 ~/.gemini/antigravity/skills/ae-motion-replicator）；
2. 检查并安装 Python 依赖：pip install pillow numpy scipy；
3. 安装 After Effects MCP：克隆 https://github.com/Dakkshin/after-effects-mcp 到 ~/mcp-servers/after-effects-mcp，执行 npm install && npm run build && npm run install-bridge，并将其加入我的 MCP 配置文件（node ~/mcp-servers/after-effects-mcp/build/index.js）；
4. 配置 Figma Motion MCP：在我的 MCP 配置文件中加入 localfig（command: "npx", args: ["-y", "localfig"]）；
5. 全部完成后检查一遍依赖和配置格式，并告诉我最后需要在 AE 和 Figma 里手动点开哪两个桥接面板。
```

---

## 手动安装与依赖清单

如果你想手动配置，按以下 3 步即可：

### 1. 安装 Skill
- **方式 A（推荐）**：直接下载 [`dist/ae-motion-replicator.skill`](dist/ae-motion-replicator.skill) 导入到你的 Agent。
- **方式 B（Git）**：
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

### 3. 配置 Figma 原生 Motion [Beta] MCP
在 `mcp_config.json` 中添加：
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
│   └── split_sprites.py            # GIF 逐帧联系表工具 & 透明合图自动切分去白边脚本
├── dist/
│   └── ae-motion-replicator.skill  # 打包好的 .skill 安装包，可直接下载导入
├── assets/                         # README 效果展示图
└── README.md
```
