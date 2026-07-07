# 🧳 私人旅行管家 · Travel Agent Skill

> **一个 Claude Code Skill + 攻略网页生成器**
> 输入出发地、目的地、预算，自动输出完整行程并生成精美网页攻略
> 支持多成员团队、一键跳转订票/导航/美食搜索

---

## ✨ 功能

| 功能 | 说明 |
|:---|:---|
| 🗺️ **行程规划** | AI 自动生成每日行程，含交通/住宿/美食/景点 |
| 💰 **预算透明** | 每日花费小计 + 总预算 + 进度条显示 |
| 🌐 **网页攻略** | 生成精美响应式攻略网页，支持手机/电脑 |
| 🔗 **一键跳转** | 每个行程项都带 12306/携程/大众点评/高德 直达链接 |
| 📕 **小红书直达** | 美食卡片点击直达小红书搜索攻略 |
| 👥 **多人支持** | 支持团队行程，标注成员偏好（老人/小孩等） |
| 🔧 **JSON 配置** | 编辑 JSON 即可换目的地，无需改代码 |

---

## 🚀 v2.0 新特性

| 新功能 | 说明 |
|:---|:---|
| 📄 **JSON 配置化** | 行程数据从 `trip.json` 读取，换目的地只需改 JSON |
| 🧑‍🤝‍🧑 **多人团队** | 支持多成员，可标注年龄、偏好、注意事项 |
| 🖥️ **网页版攻略** | 从 Word 升级为精美网页，响应式适配手机/电脑 |
| 🌀 **滚动动画** | 卡片滚动入场，预算条自动填充动效 |
| 🎨 **高级设计** | 极简高级感设计，暖色调，清晰的信息层级 |
| 📕 **小红书搜索** | 美食卡片点击直达小红书搜索对应攻略 |
| 🔗 **底部平台栏** | 所有支持平台图标展示，悬停变色，点击跳转 |

---

## 🎬 效果预览

https://github.com/XiaoiYuyao/travel-agent-skill

---

## 📦 安装

```bash
# 克隆到本地
git clone https://github.com/XiaoiYuyao/travel-agent-skill.git
cd travel-agent-skill

# 安装依赖
pip install folium Pillow matplotlib

# 在 Claude Code 中说：
# 「帮我规划一下从XX到XX的旅行」
```

---

## 🚀 使用方法

### 方法一：通过 Claude Code

说一句话就能用：

> 「帮我规划一下从广州去贵阳的旅行，3天，预算2000」
> 「暑假想去成都玩，4天，一个人」
> 「帮我生成一份西安攻略」

Claude Code 会：
1. 问你几个问题确认细节
2. 联网查实时车次/景点信息
3. 输出完整行程并生成 `trip.json`
4. 运行脚本生成网页攻略

### 方法二：直接修改 JSON

```bash
# 1. 编辑 JSON 配置
edit scripts/trip.json

# 2. 运行生成器
python scripts/generate_travel_web.py

# 3. 打开输出的攻略
open scripts/travel_guide.html
```

---

## 📁 目录结构

```
travel-agent-skill/
├── SKILL.md                          # Claude Code Skill 入口
├── README.md                         # 本文件
├── LICENSE
├── scripts/
│   ├── generate_travel_web.py        # 网页攻略生成器 (v2.0)
│   ├── generate_travel_doc.py        # Word 攻略生成器 (v1.0)
│   ├── trip.json                     # 行程数据配置
│   └── travel_guide.html             # 生成的攻略网页
└── examples/
    └── travel_guide.html             # 示例输出
```

---

## 🛠️ 自定义行程

编辑 `scripts/trip.json` 即可：

```json
{
  "trip": {
    "name": "成都4天3晚",
    "subtitle": "重庆出发 · 美食文化之旅",
    "from_to": "广州南 - 成都东",
    "days": 4,
    "budget": 3000,
    "weather": "28°C"
  },
  "team": [
    {"name": "我", "age": 26},
    {"name": "妈妈", "age": 55, "notes": "不辣、少走路"}
  ],
  "days": [...],
  "foods": [...],
  "budget": [...]
}
```

然后运行：
```bash
python scripts/generate_travel_web.py
```

---

## 🌐 平台支持

| 平台 | 用途 | 按钮颜色 |
|:---|:---|:---:|
| 🚄 **12306** | 查高铁/火车票 | 🔴 |
| 🏨 **携程** | 订酒店 | 🔵 |
| 🍜 **大众点评** | 找餐厅 | 🟡 |
| 📕 **小红书** | 搜攻略 | 🟥 |
| 🗺️ **高德地图** | 导航/定位 | 🟦 |

---

## 📋 依赖

| 依赖 | 用途 |
|:---|:---|
| Python 3.8+ | 运行环境 |
| json (内置) | 读取配置 |

> 网页版攻略无需额外依赖，浏览器直接打开

---

## 📄 License

MIT — 随便用，随便改，随便分享。

---

## 💡 灵感来源

由 [Claude Code](https://claude.ai/code) + [女娲 Skill](https://github.com/alchaincyf/nuwa-skill) 生成。
实际旅行体验中发现「做攻略→订票→导航」的链条太割裂，于是做了这个从规划到导出的闭环工具。

## 📊 版本历史

| 版本 | 日期 | 更新内容 |
|:---|:---:|:---|
| v4.0 | 2026-07 | **Gradio 网页版** — 打开浏览器就能用，无需 Claude Code；城市数据 JSON 化，加城市不碰代码 |
| v3.1 | 2026-07 | 美食直达小红书、对齐优化、预算改色、交通自动导航 |
| v3.0 | 2026-07 | 终极攻略生成器 — 自包含HTML文件，双击即用 |
| v2.0 | 2026-07 | JSON 配置化、多人团队支持、网页版攻略、小红书直达 |
| v1.0 | 2026-06 | 初版：Word 攻略导出、基本行程规划 |
