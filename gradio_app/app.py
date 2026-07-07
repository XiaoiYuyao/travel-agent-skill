"""
私人旅行管家 · Gradio 网页版
数据驱动，加城市只需编辑 cities.json
"""
import gradio as gr, json, os, tempfile, re

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "cities.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    CITIES = json.load(f)

COLORS = ["#FF6B35","#4ECDC4","#FFD93D","#667eea","#9B59B6","#E74C3C"]

def esc(s):
    s = str(s)
    for a, b in [("&","&amp;"),("<","&lt;"),(">","&gt;"),('"',"&quot;")]:
        s = s.replace(a, b)
    return s

def gen_html(from_city, to_city, days, budget, pace):
    city = CITIES.get(to_city)
    if not city: return "暂无数据"
    days = min(int(days), 7)
    budget = int(budget)
    pace_data = city["pace_compact"]
    attrs = pace_data["attractions"]
    foods = pace_data["foods"]
    tips = pace_data.get("tips", [])
    per_day = min(4, max(1, len(attrs) // days + 1))

    # 构建每日行程
    days_h = ""
    for d in range(1, days + 1):
        co = COLORS[(d-1) % len(COLORS)]
        its = ""
        dt = 0
        if d == 1:
            tin = city.get("transport_in", 400)
            dt += tin
            its += '<div class="itm itm-sm"><div class="tm">上午</div><div class="ic">🚄</div><div class="bd"><div class="tl">'+esc(from_city)+'→'+esc(to_city)+'</div><div class="de">高铁 <span class="tr">高铁</span></div></div><div class="co">¥'+str(tin)+'</div></div>'
            hotel = city.get("hotel", 250)
            dt += hotel
            its += '<div class="itm itm-lg"><div class="tm">中午</div><div class="ic">🏨</div><div class="bd"><div class="tl">入住酒店</div><div class="de">市中心 <span class="tr">打车</span></div></div><div class="co">¥'+str(hotel)+'</div></div>'
        start = (d-1) * per_day
        for i in range(per_day):
            idx = (start + i) % len(attrs)
            a = attrs[idx]
            parts = a.split("~")
            np = parts[0]
            tr = parts[1] if len(parts) > 1 else "步行"
            m = re.search(r"\d+", np)
            p = int(m.group()) if m else 0
            n = np.replace("¥","").replace(str(p) if p else "","").strip()
            if "免费" in np: p = 0
            tr_ic = "🚕" if "打车" in tr else "🚇" if "地铁" in tr else "🚶"
            dt += p
            tag = "免费" if p == 0 else "¥"+str(p)
            its += '<div class="itm itm-lg"><div class="tm">景点</div><div class="ic">📍</div><div class="bd"><div class="tl">'+esc(n)+'</div><div class="de">'+tag+' <span class="tr">'+tr_ic+' '+esc(tr)+'</span></div></div><div class="co">'+tag+'</div></div>'
        if d <= len(foods):
            f = foods[d-1]
            m = re.search(r"\d+", f)
            fp = int(m.group()) if m else 0
            fn = f.replace("¥","").replace(str(fp),"") if fp else f
            dt += fp
            its += '<div class="itm itm-lg"><div class="tm">晚餐</div><div class="ic">🍜</div><div class="bd"><div class="tl">'+esc(fn)+'</div><div class="de">当地美食 <span class="tr">🚶 步行</span></div></div><div class="co">¥'+str(fp)+'</div></div>'
        if d == days:
            tout = city.get("transport_out", 400)
            dt += tout
            its += '<div class="itm itm-sm"><div class="tm">返程</div><div class="ic">🚄</div><div class="bd"><div class="tl">返回'+esc(from_city)+'</div><div class="de">高铁 <span class="tr">高铁</span></div></div><div class="co">¥'+str(tout)+'</div></div>'
        days_h += '<div class="dc"><div class="dh" style="--c:'+co+'"><div class="dn" style="color:'+co+'">第'+str(d)+'天</div><div class="dt">'+esc(to_city)+'之旅</div></div><div class="di">'+its+'</div><div class="dd" style="color:'+co+'">本日 ¥'+str(dt)+'</div></div>'

    # 美食
    food_h = ""
    for f in foods:
        fn = f.split("¥")[0].strip()
        fp = "¥"+f.split("¥")[1] if "¥" in f else ""
        kw = esc(fn)
        food_h += '<a class="fl" href="https://www.xiaohongshu.com/search_result?keyword='+kw+'" target="_blank"><div class="fi"><div><div class="fn">'+esc(fn)+'</div><div class="fs">'+esc(to_city)+'必吃</div></div><div class="fp">'+fp+'</div></div></a>'

    # 预算
    total_est = city.get("transport_in", 400) + city.get("transport_out", 400) + city.get("hotel", 250) * days + 400
    left = budget - total_est
    mx = max(city.get("transport_in", 400) + city.get("transport_out", 400), city.get("hotel", 250) * days, 1)
    bud = '<div class="bi"><div class="bl">交通</div><div class="bt"><div class="bf" style="width:'+str(round((city.get("transport_in",400)+city.get("transport_out",400))/mx*100))+'%;background:#667eea"></div></div><div class="ba">¥'+str(city.get("transport_in",400)+city.get("transport_out",400))+'</div></div>'
    bud += '<div class="bi"><div class="bl">住宿</div><div class="bt"><div class="bf" style="width:'+str(round(city.get("hotel",250)*days/mx*100))+'%;background:#9B59B6"></div></div><div class="ba">¥'+str(city.get("hotel",250)*days)+'</div></div>'
    bud += '<div class="bi"><div class="bl">餐饮</div><div class="bt"><div class="bf" style="width:50%;background:#E74C3C"></div></div><div class="ba">¥400</div></div>'
    bud += '<div class="bdv"></div><div class="bto"><div class="btl">预计</div><div><span class="bta">¥'+str(total_est)+'</span><span class="blf">/ ¥'+str(budget)+' '+("剩余¥"+str(left) if left>=0 else "超支¥"+str(abs(left)))+'</span></div></div>'

    # 提示
    tps = ""
    for t in tips[:3]:
        tps += "<li>"+esc(t)+"</li>"

    # HTML
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>"""+esc(to_city)+"""攻略</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans SC',sans-serif;background:#f5f0eb;color:#2c2c2c;font-size:17px;line-height:1.7}
.hero{background:linear-gradient(160deg,#FF6B35,#FF8F65);padding:36px 20px 24px;text-align:center;color:#fff}
.hero h1{font-size:28px;font-weight:900;margin-bottom:6px}
.hero-stats{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:10px}
.hero-stats span{background:rgba(255,255,255,.2);padding:5px 14px;border-radius:16px;font-size:12px}
.ct{max-width:800px;margin:0 auto;padding:16px}
.sl{font-size:13px;color:#FF6B35;font-weight:600;letter-spacing:3px;margin-bottom:4px;margin-top:24px}
.st{font-size:22px;font-weight:900;margin-bottom:14px}
.dc{background:#fff;border-radius:16px;padding:18px;margin-bottom:12px;box-shadow:0 2px 16px rgba(0,0,0,.04)}
.dh{display:flex;align-items:center;gap:8px;margin-bottom:10px;padding-bottom:10px;border-bottom:2px solid var(--c)}
.dn{font-size:24px;font-weight:900;letter-spacing:-1px}
.dt{font-size:15px;color:#888}
.di{display:grid;gap:2px}
.itm{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid #f5f0eb;transition:.2s;border-radius:8px}
.itm:hover{background:#faf6f2;transform:scale(1.01)}
.itm-sm{padding:4px 6px}
.itm-sm .tl{font-size:13px;color:#888}
.itm-lg{padding:8px 6px}
.itm-lg .tl{font-size:15px;font-weight:600}
.tm{font-size:11px;color:#aaa;min-width:36px;flex-shrink:0}
.ic{font-size:18px;width:24px;text-align:center;flex-shrink:0}
.bd{flex:1}
.tl{font-size:14px;color:#2c2c2c}
.de{font-size:12px;color:#888;display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.tr{padding:1px 6px;border-radius:8px;background:#f0ebe6;font-size:10px;color:#888}
.co{font-size:13px;font-weight:700;min-width:48px;text-align:right;flex-shrink:0}
.dd{text-align:right;font-size:13px;font-weight:700;padding-top:8px;margin-top:6px;border-top:1px solid #eee;color:var(--c)}
.fl{text-decoration:none;color:inherit;display:block}
.fg{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:6px}
.fi{display:flex;justify-content:space-between;padding:10px 14px;background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.fi:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(255,107,53,.1)}
.fn{font-size:14px;font-weight:600}
.fs{font-size:11px;color:#999}
.fp{font-size:14px;font-weight:700;color:#FF6B35}
.bc{background:linear-gradient(135deg,#FF8F65,#FF6B35);border-radius:16px;padding:20px;display:grid;gap:8px}
.bi{display:flex;align-items:center;gap:10px}
.bl{font-size:13px;color:rgba(255,255,255,.95);min-width:60px}
.bt{flex:1;height:5px;background:rgba(255,255,255,.08);border-radius:3px;overflow:hidden}
.bf{height:100%;border-radius:3px;transition:width 1s ease}
.ba{font-size:13px;font-weight:700;color:#fff;min-width:44px;text-align:right}
.bdv{height:1px;background:rgba(255,255,255,.08);margin:4px 0}
.bto{display:flex;justify-content:space-between;align-items:center}
.btl{font-size:16px;font-weight:700;color:#fff}
.bta{font-size:22px;font-weight:900;color:#FFD93D}
.blf{font-size:13px;color:rgba(255,255,255,.7)}
.tc{background:#fff;border-radius:12px;padding:16px;margin-top:12px}
.tc li{list-style:none;font-size:13px;color:#666;padding:4px 0}
.tc li::before{content:"\\2726";color:#FF6B35;margin-right:6px;font-size:10px}
.pb{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;padding:16px 0}
.pb a{text-decoration:none;display:flex;flex-direction:column;align-items:center;gap:3px;color:#999;transition:.3s;padding:6px}
.pb a:hover{color:#FF6B35}
.pb .pi{font-size:16px;width:36px;height:36px;display:flex;align-items:center;justify-content:center;background:#fff;border-radius:8px}
.pb a:hover .pi{background:#FF6B35;color:#fff;transform:translateY(-2px)}
.ft{text-align:center;padding:20px;font-size:12px;color:#bbb}
</style></head>
<body>
<div class="hero"><h1>"""+esc(to_city)+" "+str(days)+"""天攻略</h1><div class="hero-stats"><span>"""+esc(from_city)+"→"+esc(to_city)+"""</span><span>"""+str(days)+"""天</span><span>¥"""+str(budget)+"""</span></div></div>
<div class="ct">
<div class="sl">ITINERARY</div><div class="st">行程安排</div>"""+days_h+"""
<div class="sl">FOOD</div><div class="st">美食推荐</div><div class="fg">"""+food_h+"""</div>
<div style="margin-top:20px"><div class="sl">BUDGET</div><div class="st">预算透明</div><div class="bc">"""+bud+"""</div></div>"""
    if tps:
        html += '<div class="tc"><h3 style="font-size:14px;margin-bottom:8px;color:#FF6B35;font-weight:600">💡 提示</h3><ul>'+tps+'</ul></div>'
    html += """<div class="sl">PLATFORMS</div><div class="st">一键跳转</div>
<div class="pb">
<a href="https://www.12306.cn/"><div class="pi">🚄</div><span>12306</span></a>
<a href="https://hotels.ctrip.com/"><div class="pi">🏨</div><span>携程</span></a>
<a href="https://www.dianping.com/"><div class="pi">🍜</div><span>点评</span></a>
<a href="https://www.xiaohongshu.com/"><div class="pi">📕</div><span>小红书</span></a>
<a href="https://ditu.amap.com/"><div class="pi">🗺</div><span>高德</span></a>
</div></div>
<div class="ft">加新城市只需编辑 data/cities.json</div>
</body></html>"""
    return html

def gen_trip(from_city, to_city, days, budget, pace):
    html = gen_html(from_city, to_city, int(days), int(budget), int(pace))
    out = os.path.join(tempfile.gettempdir(), "travel_"+to_city+".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out

city_list = list(CITIES.keys())

with gr.Blocks(title="私人旅行管家") as demo:
    gr.Markdown("# 🧳 私人旅行管家\n选城市一键生成攻略。加城市只需编辑 data/cities.json")
    with gr.Row():
        fc = gr.Dropdown(["广州","深圳","北京","上海","成都","重庆","杭州","武汉","长沙","南京"], "广州", label="出发")
        tc = gr.Dropdown(city_list, city_list[0], label="目的地")
    with gr.Row():
        dd = gr.Slider(1, 7, 3, 1, label="天数")
        bb = gr.Slider(500, 10000, 2500, 100, label="预算(元)")
    btn = gr.Button("生成攻略", variant="primary")
    out = gr.File(label="下载攻略")
    btn.click(fn=gen_trip, inputs=[fc, tc, dd, bb, gr.Number(3, visible=False)], outputs=[out])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7870)
