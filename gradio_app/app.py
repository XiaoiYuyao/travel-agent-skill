"""
私人旅行管家 · Gradio 网页版
任何人都能用，不需要Claude Code，不需要技术基础
打开网页填表，一键下载攻略
"""
import gradio as gr
import json, os, base64, re

# ===== 景点和美食知识库 =====
ATTRACTIONS = {
    "贵阳": [
        ("🐒", "黔灵山公园", "门票5元，看野生猕猴+熊猫", 5, "高德"),
        ("🌃", "甲秀楼夜景", "免费 贵阳地标 南明河畔", 0, "高德"),
        ("🏛️", "贵州省博物馆", "免费 苗族银饰+民族服饰", 0, "高德"),
        ("🗿", "花溪夜郎谷", "门票20元 石头城堡超出片", 20, "高德"),
        ("🏯", "青岩古镇", "门票10元 卤猪脚必吃", 10, "高德"),
    ],
    "成都": [
        ("🐼", "大熊猫基地", "门票55元 看国宝 建议早上去", 55, "高德"),
        ("🏛️", "武侯祠+锦里", "门票50元 三国文化圣地", 50, "高德"),
        ("🏘️", "宽窄巷子", "免费 成都文化地标", 0, "高德"),
        ("🏔️", "青城山", "门票80元 问道青城山", 80, "高德"),
        ("🏔️", "金沙遗址博物馆", "门票70元 太阳神鸟", 70, "高德"),
    ],
    "重庆": [
        ("🌃", "洪崖洞夜景", "免费 千与千寻同款夜景", 0, "高德"),
        ("🚠", "长江索道", "门票20元 跨江空中巴士", 20, "高德"),
        ("🏛️", "磁器口古镇", "免费 千年古镇+美食", 0, "高德"),
        ("🏘️", "山城步道", "免费 感受8D魔幻地形", 0, "高德"),
        ("🎨", "鹅岭二厂", "免费 文艺打卡地", 0, "高德"),
    ],
    "西安": [
        ("🏛️", "兵马俑", "门票120元 世界第八大奇迹", 120, "高德"),
        ("🏯", "西安城墙", "门票54元 骑自行车游城墙", 54, "高德"),
        ("⛩️", "大雁塔", "门票40元 大唐盛世地标", 40, "高德"),
        ("🌃", "大唐不夜城", "免费 夜景超震撼", 0, "高德"),
        ("🍜", "回民街", "免费 西安美食聚集地", 0, "大众点评"),
    ],
    "北京": [
        ("🏛️", "故宫博物院", "门票60元 需提前预约", 60, "高德"),
        ("🏯", "颐和园", "门票30元 皇家园林", 30, "高德"),
        ("🏔️", "八达岭长城", "门票40元 不到长城非好汉", 40, "高德"),
        ("⛩️", "天坛公园", "门票15元 明清祭天场所", 15, "高德"),
        ("🏙️", "南锣鼓巷", "免费 老北京胡同", 0, "高德"),
    ],
    "广州": [
        ("🏯", "广州塔", "门票150元 俯瞰广州", 150, "高德"),
        ("🏛️", "陈家祠", "门票10元 岭南建筑明珠", 10, "高德"),
        ("🌳", "越秀公园", "免费 五羊石像", 0, "高德"),
        ("🍜", "上下九步行街", "免费 广州美食老街", 0, "大众点评"),
        ("🚢", "珠江夜游", "票价68元 广州夜景", 68, "高德"),
    ]
}

FOOD_DB = {
    "贵阳": [("肠旺面","金牌罗记","12元"),("豆腐圆子","雷家豆腐圆子","10元"),("但家香酥鸭","小十字总店","30元"),("冰粉","随便一家","5元")],
    "成都": [("火锅","小龙坎","80元"),("串串香","钢管厂五区","50元"),("担担面","陈麻婆豆腐","12元"),("钟水饺","龙抄手","15元")],
    "重庆": [("重庆火锅","佩姐/周师兄","80元"),("重庆小面","花市豌杂面","15元"),("毛血旺","磁器口","60元"),("江湖菜","曾老幺鱼庄","70元")],
    "西安": [("肉夹馍","子午路张记","12元"),("凉皮","魏家凉皮","8元"),("羊肉泡馍","老孙家","35元"),("biangbiang面","大嘻咹","20元")],
    "北京": [("烤鸭","全聚德","198元"),("炸酱面","海碗居","25元"),("涮羊肉","东来顺","120元"),("卤煮","门框胡同","30元")],
    "广州": [("肠粉","银记肠粉","12元"),("虾饺","点都德","28元"),("烧鹅","炳胜品味","68元"),("云吞面","宝华面店","15元")],
}

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def generate_html(from_city, to_city, days, budget, pace):
    """生成完整的旅行攻略HTML"""
    spots = ATTRACTIONS.get(to_city, ATTRACTIONS["贵阳"])
    foods = FOOD_DB.get(to_city, FOOD_DB["贵阳"])

    if pace == "紧凑": per_day = 3
    elif pace == "松弛": per_day = 1
    else: per_day = 2

    colors = ['#FF6B35','#4ECDC4','#FFD93D','#667eea','#9B59B6','#E74C3C','#1ABC9C','#3498DB']
    days_h = ""

    for d in range(1, days+1):
        color = colors[(d-1) % len(colors)]
        themes = ["抵达+市区探索","深度体验","自然人文","自由探索","周边游","休闲收尾"]
        theme = themes[(d-1) % len(themes)]
        if d == 1: theme = f"抵达{to_city}"
        if d == days: theme = f"{to_city}·收尾返程"

        its = ""
        day_cost = 0

        if d == 1:
            its += f'''<div class="itm itm-lg"><div class="itm-time">上午</div><div class="itm-icon">🚄</div><div class="itm-body"><div class="itm-title">出发前往{to_city}</div><div class="itm-desc">高铁/飞机 建议上午出发</div></div><div class="itm-actions"><div class="itm-cost">¥400</div><span class="itm-sep">|</span><a class="ll l1" href="https://www.12306.cn/" target="_blank">12306</a></div></div>'''
            day_cost += 400
            its += f'''<div class="itm itm-lg"><div class="itm-time">中午</div><div class="itm-icon">🏨</div><div class="itm-body"><div class="itm-title">入住酒店</div><div class="itm-desc">{to_city}市中心 舒适型酒店</div></div><div class="itm-actions"><div class="itm-cost">¥200</div><span class="itm-sep">|</span><a class="ll l2" href="https://hotels.ctrip.com/" target="_blank">携程</a></div></div>'''
            day_cost += 200

        start = (d-1) * per_day
        for i in range(per_day):
            idx = (start + i) % len(spots)
            icon, name, desc, cost, plat = spots[idx]
            cls = {"高德":"l4","大众点评":"l3","12306":"l1","携程":"l2"}.get(plat,"l4")
            url = {"高德":"https://ditu.amap.com/search?query=","大众点评":"https://www.dianping.com/"}.get(plat,"#")
            if plat == "高德": url += esc(name)
            day_cost += cost
            its += f'''<div class="itm itm-lg"><div class="itm-time">景点</div><div class="itm-icon">{icon}</div><div class="itm-body"><div class="itm-title">{name}</div><div class="itm-desc">{desc}</div></div><div class="itm-actions"><div class="itm-cost">{"免费" if cost==0 else "¥"+str(cost)}</div><span class="itm-sep">|</span><a class="ll {cls}" href="{url}" target="_blank">{plat}</a></div></div>'''

        if d < len(foods):
            f = foods[d-1]
            kw = esc(f[0])
            day_cost += int(re.sub(r'[^0-9]','',f[2]) or "30")
            its += f'''<div class="itm itm-lg"><div class="itm-time">美食</div><div class="itm-icon">🍜</div><div class="itm-body"><div class="itm-title">品尝{f[0]}</div><div class="itm-desc">{f[1]}  {f[2]}</div></div><div class="itm-actions"><div class="itm-cost">{f[2]}</div><span class="itm-sep">|</span><a class="ll l3" href="https://www.xiaohongshu.com/search_result?keyword={kw}" target="_blank">小红书</a></div></div>'''

        if d == days:
            its += f'''<div class="itm itm-lg"><div class="itm-time">返程</div><div class="itm-icon">🚄</div><div class="itm-body"><div class="itm-title">返回出发地</div><div class="itm-desc">结束{to_city}之旅</div></div><div class="itm-actions"><div class="itm-cost">¥400</div><span class="itm-sep">|</span><a class="ll l1" href="https://www.12306.cn/" target="_blank">12306</a></div></div>'''
            day_cost += 400

        days_h += f'''<div class="dc"><div class="dh" style="--c:{color}"><div class="dn" style="color:{color}">第{d}天</div><div class="dt">{theme}</div></div><div class="di">{its}</div><div class="dd" style="--c:{color}">本日合计 ¥{day_cost}</div></div>'''

    food_h = ""
    for f in foods:
        kw = esc(f[0])
        food_h += f'<a class="fl" href="https://www.xiaohongshu.com/search_result?keyword={kw}" target="_blank"><div class="fi"><div><div class="fn">{f[0]}</div><div class="fs">{f[1]}</div></div><div class="fp">{f[2]}</div></div></a>'

    budget_items = [("跨城交通",800,"#667eea"),("住宿",200*days,"#9B59B6"),("餐饮",500,"#E74C3C"),("市内交通",300,"#1ABC9C"),("门票",200,"#FFB347")]
    mx = max(c for _,c,_ in budget_items)
    bud_h = ""
    for label,cost,color in budget_items:
        pct = round(cost/mx*100)
        bud_h += f'<div class="bi"><div class="bl">{label}</div><div class="bt"><div class="bf" style="width:{pct}%;background:{color}"></div></div><div class="ba">¥{cost}</div></div>'

    total = sum(c for _,c,_ in budget_items)
    left = budget - total

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(to_city)}旅行攻略 · 私人旅行管家</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter','Noto Sans SC',sans-serif;background:#f5f0eb;color:#2c2c2c;font-size:18px;line-height:1.8}}
.hero{{background:linear-gradient(160deg,#FF6B35,#FF8F65);padding:48px 24px 36px;text-align:center;color:#fff}}
.hero h1{{font-size:34px;font-weight:900;letter-spacing:-1px;margin-bottom:8px}}
.hero .sub{{font-size:17px;opacity:.85;margin-bottom:16px}}
.hero-stats{{display:flex;justify-content:center;gap:12px;flex-wrap:wrap}}
.hero-stats span{{background:rgba(255,255,255,.2);padding:8px 20px;border-radius:20px;font-size:14px;font-weight:500}}
.ct{{max-width:860px;margin:0 auto;padding:20px 16px 40px}}
.sl{{font-size:15px;color:#FF6B35;font-weight:600;letter-spacing:3px;margin-bottom:6px;margin-top:32px}}
.st{{font-size:26px;font-weight:900;margin-bottom:20px}}
.st span{{font-weight:300;color:#bbb;font-size:19px}}
.dc{{background:#fff;border-radius:18px;padding:24px;margin-bottom:16px;box-shadow:0 2px 20px rgba(0,0,0,.04)}}
.dh{{display:flex;align-items:center;gap:10px;margin-bottom:14px;padding-bottom:14px;border-bottom:2px solid var(--c)}}
.dn{{font-size:30px;font-weight:900;letter-spacing:-1px}}
.dt{{font-size:17px;color:#888;font-weight:500}}
.di{{display:grid;gap:6px}}
.itm{{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #f5f0eb;transition:.25s;border-radius:10px}}
.itm:hover{{transform:scale(1.02);background:#faf6f2;box-shadow:0 4px 16px rgba(0,0,0,.06)}}
.itm-lg{{padding:14px 12px;margin:4px 0}}
.itm-lg .itm-icon{{font-size:26px}}
.itm-lg .itm-title{{font-size:18px}}
.itm-lg .itm-desc{{font-size:15px}}
.itm-time{{font-size:13px;color:#aaa;min-width:50px;flex-shrink:0;font-weight:500}}
.itm-icon{{font-size:22px;width:30px;text-align:center;flex-shrink:0}}
.itm-body{{flex:1;min-width:0}}
.itm-title{{font-size:16px;font-weight:600;color:#2c2c2c}}
.itm-desc{{font-size:14px;color:#999}}
.itm-actions{{display:flex;align-items:center;gap:0;flex-shrink:0;width:170px;justify-content:flex-end}}
.itm-cost{{font-size:15px;font-weight:700;width:72px;text-align:right}}
.itm-sep{{color:#ddd;margin:0;width:16px;text-align:center}}
.ll{{display:inline-flex;padding:6px 0;border-radius:8px;font-size:13px;text-decoration:none;color:#fff;font-weight:500;width:76px;justify-content:center}}
.l1{{background:#EE4D2D}}.l2{{background:#1E90D7}}.l3{{background:#FFC300;color:#333!important}}.l4{{background:#29A1FF}}
.dd{{text-align:right;font-size:16px;font-weight:700;padding-top:16px;margin-top:12px;border-top:1px solid #eee;color:var(--c)}}
.fl{{text-decoration:none;color:inherit;display:block}}
.fg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px}}
.fi{{display:flex;justify-content:space-between;padding:14px 18px;background:#fff;border-radius:12px;box-shadow:0 1px 8px rgba(0,0,0,.04);transition:.2s}}
.fi:hover{{transform:translateY(-3px);box-shadow:0 8px 28px rgba(255,107,53,.1)}}
.fn{{font-size:16px;font-weight:600}}
.fs{{font-size:13px;color:#999}}
.fp{{font-size:16px;font-weight:700;color:#FF6B35}}
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
.pb{{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;padding:24px 0 8px}}
.pb a{{text-decoration:none;display:flex;flex-direction:column;align-items:center;gap:4px;color:#999;transition:.3s;padding:8px}}
.pb a:hover{{color:#FF6B35}}
.pb .pi{{font-size:20px;width:44px;height:44px;display:flex;align-items:center;justify-content:center;background:#fff;border-radius:12px;transition:.3s;box-shadow:0 2px 8px rgba(0,0,0,.04)}}
.pb a:hover .pi{{background:#FF6B35;color:#fff;transform:translateY(-3px);box-shadow:0 6px 16px rgba(255,107,53,.2)}}
.pb span{{font-size:11px;font-weight:500}}
.ft{{text-align:center;padding:32px;font-size:14px;color:#bbb}}
@media(max-width:640px){{.itm{{flex-wrap:wrap}}.itm-time{{min-width:50px}}.itm-body{{width:calc(100% - 50px)}}.itm-actions{{width:100%;padding-left:12px;margin-top:6px;justify-content:flex-start}}.ll{{width:60px}}}}
</style></head>
<body>
<div class="hero"><h1>✈ {esc(to_city)} 旅行攻略</h1><p class="sub">{esc(from_city)}出发 · {days}天 · ¥{budget}预算</p>
<div class="hero-stats"><span>{esc(from_city)}→{esc(to_city)}</span><span>{days}天</span><span>¥{budget}</span><span>{pace}</span></div></div>
<div class="ct">
<div class="sl">ITINERARY</div><div class="st">每日<span>行程</span></div>{days_h}
<div class="sl">FOOD</div><div class="st">美食<span>推荐</span></div><div class="fg">{food_h}</div>
<div style="margin-top:28px"><div class="sl">BUDGET</div><div class="st">预算<span>透明</span></div>
<div class="bc">{bud_h}<div class="bdv"></div><div class="bto"><div class="btl">总计</div><div><span class="bta">¥{total}</span><span class="blf">/ ¥{budget} {"剩余¥"+str(left) if left>=0 else "超支¥"+str(abs(left))}</span></div></div></div></div>
<div style="margin-top:28px"><div class="sl">PLATFORMS</div><div class="st">一键<span>跳转</span></div>
<div class="pb">
<a href="https://www.12306.cn/" target="_blank"><div class="pi">🚄</div><span>12306</span></a>
<a href="https://hotels.ctrip.com/" target="_blank"><div class="pi">🏨</div><span>携程</span></a>
<a href="https://www.dianping.com/" target="_blank"><div class="pi">🍜</div><span>大众点评</span></a>
<a href="https://www.xiaohongshu.com/" target="_blank"><div class="pi">📕</div><span>小红书</span></a>
<a href="https://ditu.amap.com/" target="_blank"><div class="pi">🗺️</div><span>高德</span></a>
</div></div></div>
<div class="ft">私人旅行管家 · 一键生成旅行攻略</div>
</body></html>'''

def generate_trip(from_city, to_city, days, budget, pace):
    """生成攻略并返回HTML文件"""
    html = generate_html(from_city, to_city, days, budget, pace)
    # Save to temp file
    import tempfile
    out = os.path.join(tempfile.gettempdir(), f"旅行攻略_{to_city}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out

# ===== Gradio界面 =====
with gr.Blocks(title="私人旅行管家") as demo:
    gr.Markdown("""
    # 🧳 私人旅行管家

    输入出发地和目的地，一键生成完整旅行攻略！
    不需要注册、不需要安装、完全免费。
    """)

    with gr.Row():
        from_city = gr.Dropdown(
            choices=["广州","深圳","北京","上海","杭州","武汉","长沙","南京","成都","重庆"],
            value="广州", label="🚩 出发城市"
        )
        to_city = gr.Dropdown(
            choices=["贵阳","成都","重庆","西安","北京","广州"],
            value="贵阳", label="📍 目的地"
        )

    with gr.Row():
        days = gr.Slider(minimum=1, maximum=7, value=3, step=1, label="📅 天数")
        budget = gr.Slider(minimum=500, maximum=10000, value=2000, step=100, label="💰 预算(元)")

    pace = gr.Radio(
        choices=["紧凑", "适中", "松弛"],
        value="适中",
        label="🏃 行程节奏",
        info="紧凑=每天多景点 / 松弛=休闲放松"
    )

    btn = gr.Button("🚀 一键生成攻略", variant="primary", size="lg")

    with gr.Row():
        output = gr.File(label="📄 攻略文件（双击打开）", show_label=True)

    status = gr.Markdown("")

    btn.click(
        fn=generate_trip,
        inputs=[from_city, to_city, days, budget, pace],
        outputs=[output],
        api_name="generate"
    ).then(
        fn=lambda: "✅ 攻略已生成！点击上方文件下载，双击即可查看",
        outputs=[status]
    )

    gr.Markdown("""
    ---
    ### ✨ 功能
    - 自动安排每日景点、美食、住宿
    - 一键跳转12306/携程/大众点评/高德/小红书
    - 预算透明汇总
    - 手机电脑都能看

    ### 👩‍💻 作者
    XiaoiYuyao · [GitHub](https://github.com/XiaoiYuyao/travel-agent-skill)
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft(), css="""
    .gradio-container {max-width: 700px !important; margin: 0 auto !important}
    footer {display: none !important}
""")
