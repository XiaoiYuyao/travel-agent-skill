# -*- coding: utf-8 -*-
"""
旅行攻略网页生成器 — JSON 配置版
用法: 编辑 trip.json, 然后 python generate_travel_web.py
"""
import json, os, subprocess

DIR = os.path.dirname(__file__) or "."
with open(os.path.join(DIR, "trip.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

trip, team, days, foods, budget, platforms = data["trip"], data["team"], data["days"], data["foods"], data["budget"], data["platforms"]
tips, checklist = data["tips"], data["checklist"]
TOTAL = sum(sum(it["cost"] for it in d["items"]) for d in days)
BURL = {"12306": "https://www.12306.cn/", "携程": "https://hotels.ctrip.com/", "大众点评": "https://www.dianping.com/", "高德": "https://ditu.amap.com/search?query="}
BCLS = {"12306": "b1", "携程": "b2", "大众点评": "b3", "高德": "b4"}
ESC = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

# ----- Generate HTML parts -----
days_h = ""
for d in days:
    its = ""
    sub = 0
    for it in d["items"]:
        sub += it["cost"]
        url = BURL.get(it["platform"], "#")
        if it["platform"] == "高德": url += ESC(it["title"])
        cs = "FREE" if it["cost"] == 0 else ("¥" + str(it["cost"]))
        its += '<div class="it"><div class="ii">{icon}</div><div class="ib"><div class="itl">{title}</div><div class="idd">{desc}</div></div><div class="ia"><span class="ip" style="color:{color}">{cs}</span><a class="bl {bcls}" href="{url}" target="_blank">{plat}</a></div></div>'.format(
            icon=it["icon"], title=ESC(it["title"]), desc=ESC(it["desc"]),
            color=d["color"], cs=cs, bcls=BCLS.get(it["platform"],"b1"),
            url=ESC(url), plat=it["platform"])
    dn = ("0" + str(d["day"])) if d["day"] < 10 else str(d["day"])
    days_h += '<div class="dc"><div class="ds" style="background:{co}"></div><div class="dh"><span class="dn" style="color:{co}">{dn}</span><span class="dt2">{th}</span></div><div class="di">{it}</div><div class="dtol" style="color:{co}">📊 本日小计 ¥{sub}</div></div>'.format(co=d["color"], dn=dn, th=ESC(d["theme"]), it=its, sub=sub)

food_h = ""
for f in foods:
    food_h += '<a class="fl" href="https://www.xiaohongshu.com/search_result?keyword={kw}" target="_blank"><div class="fi"><div><div class="fn">{n}</div><div class="fs">{s}</div></div><div class="fp">{p}</div></div></a>'.format(
        kw=ESC(f["keyword"]), n=ESC(f["name"]), s=ESC(f["shop"]), p=ESC(f["price"]))

mx = max(b["cost"] for b in budget) or 1
cols = ["#667eea","#9B59B6","#E74C3C","#1ABC9C","#aaa"]
budget_h = ""
for i, b in enumerate(budget):
    pct = round(b["cost"]/mx*100)
    budget_h += '<div class="bi"><div class="bl2">{l}</div><div class="bt2"><div class="bf" style="background:{co};width:{p}%"></div></div><div class="ba">¥{c}</div></div>'.format(l=ESC(b["label"]), co=cols[i], p=pct, c=b["cost"])
budget_h += '<div class="bdv"></div><div class="bto"><span class="btl">💰 总计</span><span><span class="bta">¥{t}</span><span class="blf">/ 预算剩余 ¥{r}</span></span></div>'.format(t=TOTAL, r=trip["budget"]-TOTAL)

platform_h = ""
for p in platforms:
    platform_h += '<a href="{u}" target="_blank" class="fi2" style="--hc:{hc}"><div class="ficon">{i}</div><span>{n}</span></a>'.format(u=ESC(p["url"]), hc=p["hover_color"], i=p["icon"], n=ESC(p["name"]))

team_bar = ""
if team:
    ts = []
    for m in team:
        tag = "👤 " + ESC(m.get("name",""))
        if m.get("age"): tag += " (" + str(m["age"]) + "岁)"
        if m.get("notes"): tag += " " + ESC(m["notes"])
        ts.append('<span class="team-tag">{t}</span>'.format(t=tag))
    team_bar = '<div class="team-bar">{t}</div>'.format(t="".join(ts))

tips_h = "".join("<li>{t}</li>".format(t=ESC(t)) for t in tips)
check_h = "".join("<li>{c}</li>".format(c=ESC(c)) for c in checklist)

hero_desc = "<br>".join(filter(None, [
    trip.get("subtitle"),
    trip.get("weather") and (trip["weather"] + "的避暑天堂")
]))

# ----- Assemble HTML -----
CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter','Noto Sans SC',system-ui,sans-serif;background:#f0ebe5;color:#2c2c2c;font-size:16px;line-height:1.6}
nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:18px 48px;display:flex;justify-content:space-between;align-items:center;background:#fff;box-shadow:0 2px 20px rgba(0,0,0,.04)}
.nm{font-weight:700;font-size:20px;letter-spacing:3px;color:#FF6B35}
.nl{display:flex;gap:32px;list-style:none}
.nl a{text-decoration:none;font-size:15px;font-weight:500;color:#666;letter-spacing:1px;padding:8px 20px;border:2px solid #bbb;border-radius:10px;transition:.3s}
.nl a:hover{border-color:#FF6B35;color:#FF6B35;background:#FFF5F0}
.hr{min-height:92vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:60px 20px 40px;background:linear-gradient(160deg,#FFF5EE,#FFF0E6,#FFE8D6);position:relative;overflow:hidden}
.hr::before{content:'';position:absolute;top:-80px;right:-80px;width:320px;height:320px;border-radius:50%;background:linear-gradient(135deg,rgba(255,107,53,.12),rgba(255,217,61,.08))}
.hr::after{content:'';position:absolute;bottom:-60px;left:-60px;width:260px;height:260px;border-radius:50%;background:linear-gradient(135deg,rgba(78,205,196,.12),rgba(255,107,53,.08))}
.hs{font-size:16px;letter-spacing:8px;color:#FF6B35;font-weight:500;margin-bottom:16px;position:relative;z-index:1}
.hr h1{font-size:clamp(52px,9vw,100px);font-weight:900;letter-spacing:-3px;color:#2c2c2c;position:relative;z-index:1;line-height:1.08}
.hr h1 .g{background:linear-gradient(135deg,#FF6B35,#FF8F65);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hd{font-size:22px;color:#888;margin-top:20px;max-width:540px;z-index:1;position:relative;font-weight:400;line-height:1.8}
.hst{display:flex;gap:40px;margin-top:44px;z-index:1;position:relative;flex-wrap:wrap;justify-content:center}
.hsn{font-size:32px;font-weight:700;color:#2c2c2c}
.hsl{font-size:15px;color:#aaa;letter-spacing:1px;margin-top:4px;font-weight:500}
.sec{max-width:960px;margin:0 auto;padding:64px 24px}
.sl{font-size:15px;letter-spacing:4px;color:#FF6B35;font-weight:500;margin-bottom:6px}
.st{font-size:32px;font-weight:700;color:#2c2c2c;margin-bottom:36px}
.st .lt{font-weight:300;color:#bbb}
.team-bar{display:flex;gap:12px;margin-bottom:36px;flex-wrap:wrap}
.team-tag{padding:6px 16px;background:#fff;border-radius:20px;font-size:14px;color:#666;border:1px solid #eee}
.dc{margin-bottom:52px;background:#fff;border-radius:18px;padding:32px;box-shadow:0 4px 24px rgba(0,0,0,.04);opacity:0;transform:translateY(24px);transition:.7s cubic-bezier(.22,1,.36,1)}
.dc.v{opacity:1;transform:translateY(0)}
.ds{height:5px;border-radius:3px;margin-bottom:22px;width:70px}
.dh{display:flex;align-items:baseline;gap:14px;margin-bottom:22px}
.dn{font-size:52px;font-weight:900;letter-spacing:-2px}
.dt2{font-size:22px;font-weight:500;color:#888;letter-spacing:1px}
.di{display:grid;gap:6px}
.it{display:flex;align-items:center;gap:16px;padding:14px 18px;background:#faf8f6;border-radius:12px;transition:.2s;cursor:default}
.it:hover{background:#f0e8e0;box-shadow:0 6px 24px rgba(0,0,0,.1);transform:scale(1.02)}
.ii{font-size:22px;width:38px;text-align:center;flex-shrink:0}
.ib{flex:1;min-width:0}
.itl{font-size:18px;font-weight:600;color:#2c2c2c}
.idd{font-size:16px;color:#999;margin-top:1px}
.ia{display:flex;align-items:center;gap:12px;flex-shrink:0}
.ip{font-size:20px;font-weight:700;min-width:64px;text-align:right}
.bl{display:inline-flex;padding:9px 20px;border-radius:8px;font-size:15px;font-weight:500;text-decoration:none;color:#fff;transition:.2s}
.bl:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.1)}
.b1{background:#EE4D2D}.b2{background:#1E90D7}.b3{background:#FFC300;color:#2c2c2c!important}.b4{background:#29A1FF}
.dtol{text-align:right;font-size:16px;font-weight:700;padding:14px 0 0;margin-top:14px;border-top:1px solid #f0ebe6}
.fl{text-decoration:none;color:inherit;display:block}
.fg{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.fi{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);transition:.2s}
.fi:hover{transform:translateY(-3px);box-shadow:0 8px 28px rgba(255,107,53,.1)}
.fn{font-size:17px;font-weight:600;color:#2c2c2c}
.fs{font-size:14px;color:#999;margin-top:2px}
.fp{font-size:18px;font-weight:700;color:#FF6B35}
.bc{background:#FF6B35;border-radius:18px;padding:36px;display:grid;gap:14px;box-shadow:0 4px 24px rgba(255,107,53,.2)}
.bi{display:flex;align-items:center;gap:16px}
.bl2{font-size:17px;color:rgba(255,255,255,.85);min-width:90px;font-weight:500}
.bt2{flex:1;height:8px;background:rgba(255,255,255,.2);border-radius:4px;overflow:hidden}
.bf{height:100%;border-radius:4px;transition:width 1.2s cubic-bezier(.22,1,.36,1);width:0}
.ba{font-size:17px;font-weight:700;color:#fff;min-width:56px;text-align:right}
.bdv{height:1px;background:rgba(255,255,255,.15);margin:4px 0}
.bto{display:flex;justify-content:space-between;align-items:center;padding-top:6px}
.btl{font-size:20px;font-weight:700;color:#fff}
.bta{font-size:28px;font-weight:900;color:#FFD93D}
.blf{font-size:14px;color:rgba(255,255,255,.6);margin-left:10px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.tc,.cc{background:#fff;border-radius:14px;padding:28px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.tc h3,.cc h3{font-size:18px;font-weight:700;margin-bottom:14px;color:#2c2c2c}
.tl li,.cl li{list-style:none;font-size:16px;color:#666;padding:8px 0}
.tl li::before{content:"\\2726";color:#FF6B35;margin-right:10px}
.fi2{text-decoration:none;color:#999;display:flex;flex-direction:column;align-items:center;gap:4px;transition:.3s;padding:8px}
.fi2:hover{color:var(--hc)}
.fi2 .ficon{font-size:22px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;background:#f5f0eb;border-radius:12px;transition:.3s}
.fi2:hover .ficon{background:var(--hc);color:#fff;transform:translateY(-3px);box-shadow:0 4px 12px rgba(0,0,0,.2)}
.fi2 span{font-size:11px;font-weight:500}
.ft{text-align:center;padding:40px;font-size:14px;color:#bbb;border-top:1px solid #eee;margin-top:20px}
@media(max-width:640px){.sec{padding:40px 16px}nav{padding:14px 20px}.nl{gap:16px}.hr h1{font-size:40px}.hst{gap:20px}.hd{font-size:17px}.it{flex-wrap:wrap;padding:12px 14px}.ib{width:calc(100% - 52px)}.ia{width:100%;padding-left:52px;margin-top:8px}.g2{grid-template-columns:1fr}.dc{padding:20px}.bc{padding:24px}}"""

html = ""
html += '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
html += '<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
html += '<title>' + ESC(trip.get("name","旅行攻略")) + ' · 私人旅行攻略</title>\n'
html += '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">\n'
html += '<style>' + CSS + '</style>\n</head>\n<body>\n'
# Nav
html += '<nav><div class="nm">TRAVEL</div><ul class="nl"><li><a href="#d">行程</a></li><li><a href="#f">美食</a></li><li><a href="#b">预算</a></li></ul></nav>\n'
# Hero
html += '<section class="hr">\n'
html += '<div class="hs">PRIVATE TRAVEL GUIDE</div>\n'
html += '<h1>' + ESC(trip.get("name","旅行攻略")) + '</h1>\n'
html += '<p class="hd">' + hero_desc + '</p>\n'
html += '<div class="hst">\n'
html += '<div><div class="hsn">' + ESC(trip.get("from_to","")) + '</div><div class="hsl">交通</div></div>\n'
html += '<div><div class="hsn">' + str(trip.get("days",3)) + '天</div><div class="hsl">行程</div></div>\n'
html += '<div><div class="hsn">¥' + str(trip.get("budget",2000)) + '</div><div class="hsl">预算</div></div>\n'
html += '<div><div class="hsn">' + ESC(trip.get("weather","")) + '</div><div class="hsl">天气</div></div>\n'
html += '</div>\n<div class="si"><span></span></div>\n</section>\n'
# Itinerary
html += '<section class="sec" id="d">\n'
html += '<div class="sl">ITINERARY</div>\n<h2 class="st">每日<span class="lt">行程</span></h2>\n'
html += team_bar + days_h
html += '</section>\n'
# Food
html += '<section class="sec" id="f">\n'
html += '<div class="sl">FOOD</div>\n<h2 class="st">必吃<span class="lt">美食 📕</span></h2>\n'
html += '<div style="font-size:13px;color:#999;margin-top:-28px;margin-bottom:36px">点击美食卡片直达小红书搜索攻略</div>\n'
html += '<div class="fg">' + food_h + '</div>\n</section>\n'
# Budget
html += '<section class="sec" id="b">\n'
html += '<div class="sl">BUDGET</div><h2 class="st">预算<span class="lt">透明</span></h2>\n'
html += '<div class="bc">' + budget_h + '</div>\n'
html += '<div style="height:24px"></div>\n'
html += '<div class="g2">\n'
html += '<div class="tc"><h3>💡 省钱小贴士</h3><ul class="tl">' + tips_h + '</ul></div>\n'
html += '<div class="cc"><h3>✅ 出发清单</h3><ul class="cl">' + check_h + '</ul></div>\n'
html += '</div>\n</section>\n'
# Footer
html += '<div class="ft">\n'
html += '<div style="display:flex;justify-content:center;gap:18px;margin-bottom:18px;flex-wrap:wrap">' + platform_h + '</div>\n'
html += '由 私人旅行管家 · Travel Agent Skill 生成\n</div>\n'
# Script
html += '<script>\n'
html += 'var ob=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)e.target.classList.add("v")})});\n'
html += 'document.querySelectorAll(".dc").forEach(function(e){ob.observe(e)});\n'
html += 'setTimeout(function(){document.querySelectorAll(".bf").forEach(function(e,i){setTimeout(function(){var w=e.style.width;e.style.width=w||"0%"},i*120)})},400);\n'
html += '</script>\n</body>\n</html>'

with open(os.path.join(DIR, "travel_guide.html"), "w", encoding="utf-8") as f:
    f.write(html)

p = os.path.join(DIR, "travel_guide.html")
print("Done! -> travel_guide.html (" + str(os.path.getsize(p)//1024) + "KB)")
print("Team: " + str(len(team)) + " people, " + str(trip["days"]) + " days, budget: " + str(trip["budget"]))
subprocess.run(["start", p], shell=True)
