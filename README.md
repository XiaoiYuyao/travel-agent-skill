# 🧳 私人旅行管家 · Travel Agent

> **Claude Code Skill + Gradio 网页版，同一份数据，两种用法。**
> 用 Claude Code 深度规划 + 一键生成攻略，或者直接打开浏览器直接用。

---

## 🎯 项目定位

本项目包含 **两个入口**，面向不同用户群体：

| | 🟣 Claude Code Skill | 🌐 Gradio 网页版 |
|:---|:---|---|
| 目标用户 | Claude Code 用户/极客 | **所有人**（无需任何工具） |
| 使用方式 | `npx skills install XiaoiYuyao/travel-agent-skill` | 打开浏览器访问 |
| 能力 | AI 深度对话规划 + 联网查实时信息 | 选城市→生成攻略（数据驱动） |
| 输出 | 文字行程 + 网页/Word 攻略 | 精美 HTML 攻略文件 |
| 谁在用 | 会用 AI 的深度用户 | 普通用户 |

---

## 🚀 Claude Code Skill（面向极客/开发者）

在 Claude Code 中一句话就能用：

```bash
# 安装 skill
npx skills install XiaoiYuyao/travel-agent-skill
```

然后在 Claude Code 中说出：

> 「帮我规划一下从广州去贵阳的旅行，3天，预算2000」
> 「暑假想去成都玩，4天，一个人」
> 「帮我生成一份西安攻略，导出网页」

**Claude Code 会做什么：**
1. 问清楚出发地、天数、预算、风格偏好
2. 联网查实时高铁/景点/美食信息（确保推荐真实存在）
3. 输出完整行程，每日含交通衔接、住宿、景点、美食
4. 可选生成精美网页攻略或 Word 文档

> 适合已经有 Claude Code、习惯深度对话式规划的用户。

## 🌐 Gradio 网页版（面向所有人）

无需任何工具，打开浏览器就能用：

```bash
cd gradio_app
pip install gradio
python app.py
```

然后打开 `http://localhost:7870`，选择城市和天数，点击生成即可。

**特性：**
- 数据驱动，编辑 `data/cities.json` 即可加新城市
- 生成的攻略是独立 HTML 文件，双击就能打开
- 每个景点/美食都带 12306/携程/大众点评/高德/小红书直达链接

> 适合普通用户，不需要懂 Claude Code 或任何命令行。

---

## 📁 目录结构

```
travel-agent-skill/
├── SKILL.md                          # Claude Code Skill 入口
├── README.md                         # 本文件
├── LICENSE
├── scripts/                          # ✨ Claude Code 配套脚本
│   ├── generate_travel_web.py        # 网页攻略生成器
│   ├── generate_travel_doc.py        # Word 攻略生成器
│   └── trip.json                     # 行程数据模板
├── gradio_app/                       # ✨ 网页版（人人可用）
│   ├── app.py                        # Gradio 主程序
│   └── data/
│       └── cities.json               # 城市数据库
├── examples/                         # 示例输出
└── plugin-entry.json                 # Build with Claude 市场入口
```

---

## 🔧 给两家都加上城市

| 你想做的 | 路径 |
|:---|:---|
| 让 Claude 规划新目的地 | 对话中告诉 Claude，它会自动处理 |
| 加到网页版 | 编辑 `gradio_app/data/cities.json`，加一个城市条目即可 |

---

## 🎬 预览

**网页版截图：**  
选择城市 → 点击生成 → 获得精美 HTML 攻略

**Claude Code 演示：**  
说「帮我规划旅行」→ AI 对话查信息 → 输出完整行程

---

## 🌐 平台跳转支持

每个行程项都带跳转链接：

| 平台 | 用途 | 跳转方式 |
|:---|:---|:---:|
| 🚄 **12306** | 查高铁/火车票 | 底部栏点击直达 |
| 🏨 **携程** | 订酒店 | 底部栏点击直达 |
| 🍜 **大众点评** | 找餐厅 | 底部栏点击直达 |
| 📕 **小红书** | 搜攻略 | 美食卡片直接跳转搜索 |
| 🗺️ **高德地图** | 导航 | 底部栏点击直达 |

---

## 📄 License

MIT — 随便用，随便改，随便分享。

---

## 💡 灵感

由 [Claude Code](https://claude.ai/code) + 实际旅行体验驱动。
发现「做攻略→订票→导航」的链条太割裂，于是做了这个从规划到导出的闭环工具。

## 📊 版本历史

| 版本 | 日期 | 更新内容 |
|:---|:---:|:---|
| v4.0 | 2026-07 | **Gradio 网页版** — 人人都能用，无需 Claude Code |
| v3.1 | 2026-07 | 美食直达小红书、交通自动导航 |
| v3.0 | 2026-07 | 自包含HTML攻略，双击即用 |
| v2.0 | 2026-07 | JSON 配置化、多人团队支持、网页版攻略 |
| v1.0 | 2026-06 | 初版：Word 攻略导出 |
