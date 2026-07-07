# 🧳 私人旅行管家 · Travel Agent Skill

> **一个 Claude Code Skill + 攻略文档生成器**
> 输入出发地、目的地、预算，自动输出完整行程并生成Word攻略

---

## ✨ 功能

| 功能 | 说明 |
|:---|:---|
| 🗺️ **行程规划** | AI 自动生成每日行程，含交通/住宿/美食/景点 |
| 💰 **预算透明** | 每日花费小计 + 总预算 + 省钱方案 |
| 📄 **导出Word** | 一键生成带路线地图的攻略文档，可直接编辑/打印 |
| 🗺️ **交互地图** | 可选生成 Folium 交互式地图（可缩放点景点） |
| 🚄 **实时车次** | Skill 运行时可联网查询真实车次和票价 |

---

## 🎬 效果预览

```
📋 行程总览
├── 路线：广州 → 贵阳
├── 天数：3天2晚
├── 预算：¥2,000/人
├── 预估总花费：¥1,568/人 ✅ 预算内
└── 风格：休闲+美食

Day 1 · 老城烟火
├── 🚄 G2942 广州南07:44→贵阳北11:10  ¥406
├── 🏨 喷水池区域 舒适型酒店  ¥150
├── 🍜 亮欢寨酸汤鱼  ¥80
├── 🐒 黔灵山公园 门票¥5
├── 🍢 民生路扫街  ¥62
└── 🌃 甲秀楼夜景  免费
```

---

## 📦 安装

```bash
# 1. 克隆到 Claude Code skills 目录
git clone https://github.com/你的用户名/travel-agent-skill.git ~/.claude/skills/travel-agent-skill

# 2. 安装依赖（用于导出Word文档）
pip install python-docx folium Pillow matplotlib

# 3. 在 Claude Code 中说：
#    「帮我规划一下从XX到XX的旅行」
#    或「/travel-agent 生成攻略」
```

---

## 🚀 使用方法

### 方法一：通过 Claude Code（推荐）

说一句话就能用：

> 「帮我规划一下从广州去贵阳的旅行，3天，预算2000」
> 「暑假想去成都玩，4天，一个人」
> 「帮我生成一份西安攻略并导出Word」

Claude Code 会：
1. 问你几个问题确认细节
2. 联网查实时车次/景点信息
3. 输出完整行程
4. 如果你说「导出Word」→ 运行脚本生成文档

### 方法二：直接使用 Python 脚本

```bash
# 修改 scripts/generate_travel_doc.py 顶部的行程数据
# 然后运行：
python scripts/generate_travel_doc.py
```

输出：
- `攻略.docx` — 带路线地图的 Word 文档
- `route_map.html` — 交互式地图

---

## 📁 目录结构

```
travel-agent-skill/
├── SKILL.md                          # Claude Code Skill 入口
├── README.md                         # 本文件
├── LICENSE
├── scripts/
│   └── generate_travel_doc.py        # Word 攻略生成器
└── examples/
    └── sample_output.docx            # 示例输出
```

---

## 🛠️ 自定义行程数据

修改 `scripts/generate_travel_doc.py` 顶部的数据部分即可：

```python
TITLE = "成都 4 天 3 晚"
SUB_TITLE = "重庆出发 · 美食文化之旅"
TOTAL_BUDGET = 3000

DAYS = [
    {
        "day": 1,
        "color": "FF7B54",
        "theme": "市区经典 · 美食初探",
        "items": [
            ("🚄 高铁出发", "GXXX 重庆北→成都东  ¥XXX", 150, "#667eea"),
            ...
        ],
    },
]
```

---

## 📋 依赖

| 依赖 | 版本 | 用途 |
|:---|:---:|:---|
| python-docx | ≥1.0 | Word 文档生成 |
| folium | ≥0.15 | 交互式地图 |
| Pillow | ≥10.0 | 图片处理 |
| matplotlib | ≥3.8 | 地图绘制 |

---

## 📄 License

MIT — 随便用，随便改，随便分享。

---

## 💡 灵感来源

由 [Claude Code](https://claude.ai/code) + [女娲 Skill](https://github.com/alchaincyf/nuwa-skill) 生成。
实际旅行体验中发现「做攻略→订票→导航」的链条太割裂，于是做了这个从规划到导出的闭环工具。
