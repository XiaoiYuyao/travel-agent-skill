"""
============================================
  私人旅行管家 · 终极攻略生成器
============================================
  一键生成完整HTML攻略，保存到桌面
  无需服务器、无需登录、双击运行
============================================
"""
import os, json, subprocess, webbrowser

# ===== 行程数据（可从这里修改，也可由Claude Code自动填入） =====
TRIP = {
    "title": "贵阳3天2晚 · 家庭避暑之旅",
    "from_city": "广州",
    "to_city": "贵阳",
    "from_station": "广州南",
    "to_station": "贵阳北",
    "days": 3,
    "total_budget": 2000,
    "weather": "23°C 避暑胜地",
    "style": "休闲+美食",
    "travelers": 3
}

# === 交通 ===
TRAIN_GO = {"train": "G2942", "depart": "07:44", "arrive": "11:10", "duration": "3h26min", "cost": 406}
TRAIN_BACK = {"train": "G2922", "depart": "16:43", "arrive": "20:32", "duration": "3h49min", "cost": 422}

# === 每日行程 ===
DAYS = [
    {
        "day": 1, "theme": "抵达贵阳 · 老城烟火", "color": "#FF6B35",
        "items": [
            {"time": "07:00-07:30", "icon": "🚄", "title": "广州南站出发", "desc": "地铁/打车到广州南站", "cost": 30, "type": "交通"},
            {"time": "07:44-11:10", "icon": "🚄", "title": "高铁G2942", "desc": "广州南→贵阳北 3h26min", "cost": 406, "type": "交通", "link": "12306", "kw": "广州南-贵阳北"},
            {"time": "11:10-11:40", "icon": "🚕", "title": "贵阳北站→酒店", "desc": "打车到喷水池区域 约6km 15min", "cost": 25, "type": "交通"},
            {"time": "11:40-12:00", "icon": "🏨", "title": "入住酒店", "desc": "喷水池/大十字区域 舒适型酒店", "cost": 300, "type": "住宿", "link": "携程", "kw": "贵阳喷水池酒店"},
            {"time": "12:00-13:00", "icon": "🍜", "title": "午餐：酸汤鱼", "desc": "亮欢寨酸汤鱼(飞山街店) 贵阳灵魂美食", "cost": 80, "type": "美食", "link": "大众点评", "kw": "亮欢寨酸汤鱼"},
            {"time": "13:30-17:00", "icon": "🐒", "title": "黔灵山公园", "desc": "门票¥5 看野生猕猴+熊猫+弘福寺", "cost": 5, "type": "景点", "link": "高德", "kw": "黔灵山公园"},
            {"time": "18:00-19:30", "icon": "🍢", "title": "民生路扫街", "desc": "肠旺面+豆腐圆子+香酥鸭+冰粉", "cost": 62, "type": "美食", "link": "大众点评", "kw": "贵阳民生路美食"},
            {"time": "20:00-21:00", "icon": "🌃", "title": "甲秀楼夜景", "desc": "免费 贵阳地标 南明河畔散步", "cost": 0, "type": "景点", "link": "高德", "kw": "甲秀楼"},
            {"time": "21:00", "icon": "🏨", "title": "回酒店休息", "desc": "打车回酒店 约10min ¥15", "cost": 15, "type": "交通"},
        ]
    },
    {
        "day": 2, "theme": "山水古镇 · 文艺探索", "color": "#4ECDC4",
        "items": [
            {"time": "08:00-08:30", "icon": "🍜", "title": "早餐：牛肉粉", "desc": "花溪王记牛肉粉(民生路店)", "cost": 18, "type": "美食", "link": "大众点评", "kw": "花溪王记牛肉粉"},
            {"time": "09:00-11:00", "icon": "🏛️", "title": "贵州省博物馆", "desc": "免费(需预约) 苗族银饰+民族服饰", "cost": 0, "type": "景点", "link": "高德", "kw": "贵州省博物馆"},
            {"time": "11:00-12:00", "icon": "🚕", "title": "博物馆→花溪区", "desc": "打车到花溪方向 约20min ¥30", "cost": 30, "type": "交通"},
            {"time": "12:00-13:00", "icon": "🍲", "title": "午餐", "desc": "花溪区当地餐厅 地道黔菜", "cost": 60, "type": "美食", "link": "大众点评", "kw": "花溪美食"},
            {"time": "13:30-16:00", "icon": "🗿", "title": "花溪夜郎谷", "desc": "门票¥20 石头城堡超出片", "cost": 20, "type": "景点", "link": "高德", "kw": "花溪夜郎谷"},
            {"time": "16:00-17:00", "icon": "🚕", "title": "夜郎谷→青云市集", "desc": "打车到市区 约30min ¥40", "cost": 40, "type": "交通"},
            {"time": "18:00-20:00", "icon": "🌮", "title": "青云市集夜市", "desc": "烙锅+烤串 老厂房夜市", "cost": 60, "type": "美食", "link": "大众点评", "kw": "青云市集"},
            {"time": "20:00", "icon": "🏨", "title": "回酒店休息", "desc": "步行回酒店 约10min", "cost": 0, "type": "交通"},
        ]
    },
    {
        "day": 3, "theme": "古镇收尾 · 满载而归", "color": "#FFD93D",
        "items": [
            {"time": "08:00-08:30", "icon": "🍜", "title": "早餐退房", "desc": "酒店早餐+办理退房", "cost": 0, "type": "住宿"},
            {"time": "08:30-09:10", "icon": "🚕", "title": "市区→青岩古镇", "desc": "打车到青岩古镇 约35min ¥50", "cost": 50, "type": "交通"},
            {"time": "09:30-12:00", "icon": "🏯", "title": "青岩古镇", "desc": "门票¥10 卤猪脚必吃(金必轩)", "cost": 10, "type": "景点", "link": "高德", "kw": "青岩古镇"},
            {"time": "12:00-13:00", "icon": "🥟", "title": "午餐：丝娃娃", "desc": "古镇内午餐 丝娃娃+卤猪脚", "cost": 45, "type": "美食", "link": "大众点评", "kw": "青岩古镇美食"},
            {"time": "13:00-13:40", "icon": "🚕", "title": "青岩古镇→贵阳北站", "desc": "打车到高铁站 约35min ¥50", "cost": 50, "type": "交通"},
            {"time": "14:00-14:30", "icon": "⏳", "title": "贵阳北站候车", "desc": "提前到站取票/刷身份证进站", "cost": 0, "type": "交通"},
            {"time": "14:30-18:30", "icon": "🚄", "title": "高铁G2922回程", "desc": "贵阳北→广州南 3h49min", "cost": 422, "type": "交通", "link": "12306", "kw": "贵阳北-广州南"},
        ]
    }
]

# === 美食推荐 ===
FOODS = [
    ("肠旺面", "金牌罗记肠旺面", "¥12"),
    ("豆腐圆子", "雷家豆腐圆子", "¥10"),
    ("但家香酥鸭", "小十字总店", "¥30"),
    ("恋爱豆腐果", "路边摊", "¥5"),
    ("冰粉", "随便一家", "¥5"),
    ("卤猪脚", "金必轩(青岩)", "¥40"),
]

# === 预算明细 ===
BUDGET_ITEMS = [
    ("🚄 高铁往返", 828, "#667eea"),
    ("🏨 住宿2晚", 600, "#9B59B6"),
    ("🍜 餐饮美食", 325, "#E74C3C"),
    ("🚕 市内交通", 250, "#1ABC9C"),
    ("🎫 门票", 35, "#FFB347"),
    ("📦 其他", 50, "#95A5A6"),
]

# ===== 计算总计 =====
TOTAL = sum(c for _,c,_ in BUDGET_ITEMS)
REMAINING = TRIP["total_budget"] - TOTAL

# ===== 生成HTML =====
def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&#39;")

def build_html():
    # 构建每日行程HTML
    days_html = ""
    for d in DAYS:
        items_html = ""
        for it in d["items"]:
            cost_str = "免费" if it["cost"] == 0 else f"¥{it['cost']}"

            # 自动给交通项加上高德导航链接
            if not it.get("link"):
                it["link"] = "高德"
                if not it.get("kw"):
                    it["kw"] = it["title"]

            urls = {"12306":"https://www.12306.cn/","携程":"https://hotels.ctrip.com/","大众点评":"https://www.dianping.com/","高德":"https://ditu.amap.com/search?query="}
            url = urls.get(it["link"],"#")
            if it["link"] == "高德": url += esc(it.get("kw",""))
            cls_map = {"12306":"l1","携程":"l2","大众点评":"l3","高德":"l4"}
            link_html = f'<a class="ll {cls_map.get(it["link"],"l1")}" href="{url}" target="_blank">{it["link"]}</a>'

            # 根据类型分配大小类名：交通=sm，住宿/美食/景点=lg
            size_cls = "itm-sm" if it["type"] == "交通" else "itm-lg"

            items_html += f'''<div class="itm {size_cls}">
<div class="itm-time">{it["time"]}</div>
<div class="itm-icon">{it["icon"]}</div>
<div class="itm-body">
<div class="itm-title">{esc(it["title"])}</div>
<div class="itm-desc">{esc(it["desc"])}</div>
</div>
<div class="itm-actions">
<div class="itm-cost">{cost_str}</div>
<span class="itm-sep">|</span>
{link_html}
</div>
</div>'''

        days_html += f'''<div class="dc">
<div class="dh" style="--c:{d["color"]}">
<div class="dn" style="color:{d["color"]}">第{d["day"]}天</div>
<div class="dt">{esc(d["theme"])}</div>
</div>
<div class="di">{items_html}</div>
<div class="dd" style="--c:{d["color"]}">📊 本日合计 ¥{sum(it["cost"] for it in d["items"])}</div>
</div>'''

    # 美食HTML
    food_html = ""
    for f in FOODS:
        food_html += f'<div class="fi"><div><div class="fn">{esc(f[0])}</div><div class="fs">{esc(f[1])}</div></div><div class="fp">{esc(f[2])}</div></div>'

    # 预算HTML
    budget_html = ""
    mx = max(c for _,c,_ in BUDGET_ITEMS)
    for i,(label,cost,color) in enumerate(BUDGET_ITEMS):
        pct = round(cost/mx*100)
        budget_html += f'<div class="bi"><div class="bl">{esc(label)}</div><div class="bt"><div class="bf" style="width:{pct}%;background:{color}"></div></div><div class="ba">¥{cost}</div></div>'

    H = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(TRIP['title'])}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter','Noto Sans SC',sans-serif;background:#f5f0eb;color:#2c2c2c;font-size:18px;line-height:1.8}}

/* Hero */
.hero{{background:linear-gradient(160deg,#FF6B35,#FF8F65,#FF6B35);padding:48px 24px 36px;text-align:center;color:#fff}}
.hero h1{{font-size:34px;font-weight:900;letter-spacing:-1px;margin-bottom:8px}}
.hero .sub{{font-size:17px;opacity:.85;margin-bottom:16px}}
.hero-stats{{display:flex;justify-content:center;gap:12px;flex-wrap:wrap}}
.hero-stats span{{background:rgba(255,255,255,.2);padding:8px 20px;border-radius:20px;font-size:14px;font-weight:500}}
.hero .tags{{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:14px}}
.hero .tags span{{background:rgba(255,255,255,.15);padding:6px 18px;border-radius:14px;font-size:13px}}

.ct{{max-width:860px;margin:0 auto;padding:20px 16px 0}}

.sl{{font-size:15px;color:#FF6B35;font-weight:600;letter-spacing:3px;margin-bottom:6px;margin-top:32px}}
.st{{font-size:26px;font-weight:900;margin-bottom:20px;display:flex;align-items:center;gap:8px}}
.st span{{font-weight:300;color:#bbb;font-size:19px}}

/* Day Cards */
.dc{{background:#fff;border-radius:18px;padding:24px;margin-bottom:16px;box-shadow:0 2px 20px rgba(0,0,0,.04)}}
.dh{{display:flex;align-items:center;gap:10px;margin-bottom:14px;padding-bottom:14px;border-bottom:2px solid var(--c)}}
.dn{{font-size:30px;font-weight:900;letter-spacing:-1px}}
.dt{{font-size:17px;color:#888;font-weight:500}}
.di{{display:grid;gap:6px}}
.itm{{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #f5f0eb;transition:.25s cubic-bezier(.22,1,.36,1);cursor:default;border-radius:10px}}
.itm:hover{{transform:scale(1.02);background:#faf6f2;box-shadow:0 4px 16px rgba(0,0,0,.06)}}
.itm-sm{{padding:8px 10px;margin:2px 0}}
.itm-sm .itm-time{{font-size:14px}}
.itm-sm .itm-icon{{font-size:16px}}
.itm-sm .itm-title{{font-size:14px;color:#888}}
.itm-sm .itm-desc{{font-size:13px}}
.itm-sm .itm-cost{{font-size:14px}}
.itm-lg{{padding:14px 12px;margin:4px 0}}
.itm-lg .itm-time{{font-size:14px;font-weight:600;color:#888}}
.itm-lg .itm-icon{{font-size:26px}}
.itm-lg .itm-title{{font-size:18px}}
.itm-lg .itm-desc{{font-size:15px}}
.itm-lg .itm-cost{{font-size:17px}}
.itm:last-child{{border:none}}
.itm-time{{font-size:13px;color:#aaa;min-width:72px;flex-shrink:0;font-weight:500}}
.itm-icon{{font-size:22px;width:30px;text-align:center;flex-shrink:0}}
.itm-body{{flex:1;min-width:0}}
.itm-title{{font-size:14px;font-weight:600;color:#2c2c2c}}
.itm-desc{{font-size:14px;color:#999;margin-top:1px}}
.itm-actions{{display:flex;align-items:center;gap:6px;flex-shrink:0;min-width:150px}}
.itm-sep{{color:#ddd;font-size:14px;font-weight:300;margin:0 4px;user-select:none}}
.itm-cost{{font-size:14px;font-weight:700;min-width:60px;text-align:right}}
.ll{{display:inline-flex;padding:7px 0;border-radius:8px;font-size:14px;text-decoration:none;color:#fff;font-weight:500;transition:.2s;width:76px;justify-content:center;text-align:center}}
.ll:hover{{transform:translateY(-1px)}}
.l1{{background:#EE4D2D}}.l2{{background:#1E90D7}}.l3{{background:#FFC300;color:#333!important}}.l4{{background:#29A1FF}}
.dd{{text-align:right;font-size:16px;font-weight:700;padding-top:16px;margin-top:12px;border-top:1px solid #eee;color:var(--c)}}

/* Food Grid */
.fg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px}}
.fi{{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:#fff;border-radius:12px;box-shadow:0 1px 8px rgba(0,0,0,.04);transition:.2s}}
.fi:hover{{transform:translateY(-2px);box-shadow:0 4px 16px rgba(255,107,53,.1)}}
.fn{{font-size:16px;font-weight:600}}
.fs{{font-size:13px;color:#999;margin-top:1px}}
.fp{{font-size:16px;font-weight:700;color:#FF6B35}}

/* Budget */
.bc{{background:linear-gradient(135deg,#FF8F65,#FF6B35);border-radius:18px;padding:28px;display:grid;gap:12px;box-shadow:0 4px 20px rgba(255,107,53,.2)}}
.bi{{display:flex;align-items:center;gap:12px}}
.bl{{font-size:15px;color:rgba(255,255,255,.95);min-width:80px;font-weight:500}}
.bt{{flex:1;height:8px;background:rgba(255,255,255,.08);border-radius:4px;overflow:hidden}}
.bf{{height:100%;border-radius:4px;transition:width 1s ease}}
.ba{{font-size:15px;font-weight:700;color:#fff;min-width:52px;text-align:right}}
.bdv{{height:1px;background:rgba(255,255,255,.08);margin:8px 0}}
.bto{{display:flex;justify-content:space-between;align-items:center;padding-top:4px}}
.btl{{font-size:20px;font-weight:700;color:#fff}}
.bta{{font-size:26px;font-weight:900;color:#FFD93D}}
.blf{{font-size:15px;color:rgba(255,255,255,.75)}}

/* Platforms */
.pb{{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;padding:24px 0 8px}}
.pb a{{text-decoration:none;display:flex;flex-direction:column;align-items:center;gap:4px;color:#999;transition:.3s;padding:8px}}
.pb a:hover{{color:#FF6B35}}
.pb .pi{{font-size:20px;width:44px;height:44px;display:flex;align-items:center;justify-content:center;background:#fff;border-radius:12px;transition:.3s;box-shadow:0 2px 8px rgba(0,0,0,.04)}}
.pb a:hover .pi{{background:#FF6B35;color:#fff;transform:translateY(-3px);box-shadow:0 6px 16px rgba(255,107,53,.2)}}
.pb span{{font-size:13px;font-weight:500}}

/* Tips */
.tps{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}}
.tp{{background:#fff;border-radius:14px;padding:20px;box-shadow:0 1px 8px rgba(0,0,0,.04)}}
.tp h3{{font-size:17px;font-weight:700;margin-bottom:12px;display:flex;align-items:center;gap:6px}}
.tp li{{list-style:none;font-size:15px;color:#666;padding:6px 0;display:flex;align-items:center;gap:6px}}
.tp li::before{{content:"✦";color:#FF6B35;font-size:14px}}

.ft{{text-align:center;padding:32px;font-size:14px;color:#bbb}}

@media(max-width:640px){{
.tps{{grid-template-columns:1fr}}
.itm{{flex-wrap:wrap;padding:10px 0}}
.itm-time{{min-width:50px}}
.itm-body{{width:calc(100% - 50px)}}
.itm-actions{{width:100%;padding-left:12px;margin-top:6px;justify-content:flex-start}}
}}

@media print{{
.ll{{display:none}}
.hero{{background:#FF6B35!important;padding:24px}}
body{{background:#fff}}
.ct{{max-width:100%}}
}}
</style>
</head>
<body>

<div class="hero">
<h1>✈ {esc(TRIP['title'])}</h1>
<p class="sub">{esc(TRIP['from_city'])}出发 · {esc(TRIP['to_city'])} · {esc(TRIP['style'])}</p>
<div class="hero-stats">
<span>🚄 {esc(TRIP['from_city'])}→{esc(TRIP['to_city'])}</span>
<span>📅 {TRIP['days']}天{TRIP['days']-1}晚</span>
<span>💰 ¥{TRIP['total_budget']}/人</span>
<span>🌡 {esc(TRIP['weather'])}</span>
</div>
<div class="tags">
<span>{esc(TRIP['from_station'])}→{esc(TRIP['to_station'])}</span>
<span>去程 {TRAIN_GO['train']} {TRAIN_GO['depart']}-{TRAIN_GO['arrive']}</span>
<span>返程 {TRAIN_BACK['train']} {TRAIN_BACK['depart']}-{TRAIN_BACK['arrive']}</span>
</div>
</div>

<div class="ct">

<!-- 每日行程 -->
<div class="sl">ITINERARY</div>
<div class="st">每日<span>行程</span></div>
{days_html}

<!-- 美食推荐 -->
<div class="sl">FOOD</div>
<div class="st">美食<span>推荐</span></div>
<div class="fg">{food_html}</div>

<!-- 预算 -->
<div style="margin-top:28px">
<div class="sl">BUDGET</div>
<div class="st">预算<span>透明</span></div>
<div class="bc">{budget_html}<div class="bdv"></div><div class="bto"><div class="btl">💰 总计</div><div><span class="bta">¥{TOTAL}</span><span class="blf">/ 预算¥{TRIP['total_budget']} {'✅ 剩余¥'+str(REMAINING) if REMAINING>=0 else '⚠️ 超支¥'+str(abs(REMAINING))}</span></div></div></div>
</div>

<!-- Tips -->
<div style="margin-top:28px">
<div class="sl">TIPS</div>
<div class="st">贴士<span>与清单</span></div>
<div class="tps">
<div class="tp"><h3>💡 省钱建议</h3><ul>
<li>选D字头动车可省¥116</li>
<li>3人出行住宿分摊人均¥200</li>
<li>博物馆/甲秀楼免费</li>
<li>7月多雨记得带伞</li>
</ul></div>
<div class="tp"><h3>✅ 出发清单</h3><ul>
<li>身份证、学生证</li>
<li>晴雨伞、薄外套(23°C)</li>
<li>充电宝、数据线</li>
<li>下载12306/携程/高德</li>
<li>少量现金（门票用）</li>
</ul></div>
</div>
</div>

<!-- Platform links -->
<div style="margin-top:12px">
<div class="sl">PLATFORMS</div>
<div class="st">一键<span>跳转</span></div>
<div class="pb">
<a href="https://www.12306.cn/" target="_blank"><div class="pi">🚄</div><span>12306</span></a>
<a href="https://hotels.ctrip.com/" target="_blank"><div class="pi">🏨</div><span>携程</span></a>
<a href="https://www.dianping.com/" target="_blank"><div class="pi">🍜</div><span>大众点评</span></a>
<a href="https://www.xiaohongshu.com/search_result?keyword=贵阳美食" target="_blank"><div class="pi">📕</div><span>小红书</span></a>
<a href="https://ditu.amap.com/" target="_blank"><div class="pi">🗺️</div><span>高德</span></a>
</div>
</div>

</div>

<div class="ft">🧳 私人旅行管家 · Travel Agent Skill 生成 · {TRIP['days']}天{TRIP['days']-1}晚完整攻略</div>

<script>
// 预算条动画
setTimeout(function(){{
document.querySelectorAll('.bf').forEach(function(el,i){{
setTimeout(function(){{el.style.width=el.style.width}},i*120)
}})
}},300)
</script>
</body>
</html>"""
    return H

# ===== 保存到桌面 =====
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
filename = f"旅行攻略_{TRIP['to_city']}.html"
output = os.path.join(desktop, filename)

html = build_html()
with open(output, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ 攻略已生成！")
print(f"📄 桌面文件: {filename}")
print(f"📏 大小: {len(html)//1024}KB")
print(f"📅 {TRIP['days']}天{TRIP['days']-1}晚 | 💰 ¥{TOTAL}/人 {'✅ 预算内' if REMAINING>=0 else '⚠️ 超支'}")

try:
    webbrowser.open(output)
    print(f"🖥️ 已自动打开")
except:
    print(f"📂 双击桌面文件打开")

subprocess.run(["start", output], shell=True)
