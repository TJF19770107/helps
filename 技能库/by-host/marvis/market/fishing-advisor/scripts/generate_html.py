#!/usr/bin/env python3
"""HTML报告生成器 - 深色星空主题，类钓鱼天气App风格
v4.1: 平滑曲线+点击选中/反选+hover tooltip+24h/7d切换+条形鱼口图
"""

import json
import time
from pathlib import Path


def generate_html(data: dict, three_elements: list, output_dir: str = None) -> str:
    if output_dir is None:
        output_dir = str(Path.home() / "fishing_advisor_output")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    city = data.get("city", "未知")
    ts = time.strftime("%Y%m%d_%H%M%S")
    filepath = Path(output_dir) / f"fishing_report_{city}_{ts}.html"

    fi = data.get("fishing_index", {})
    weather = data.get("weather", {})
    water = data.get("water", {})
    pressure_trend = data.get("pressure_trend", {})
    moon = data.get("moon", {})
    best_time = data.get("best_time", "")
    gear = data.get("gear_advice", {})
    fish_species = data.get("fish_species", [])
    weekly_index = data.get("weekly_index", [])
    today_advice = data.get("today_advice", "")
    summary = data.get("summary", "")

    current_index = fi.get("current") or 0
    rating = fi.get("rating", "")
    gauge_color = _index_to_color(current_index)

    # 三要素数据 JSON
    te_hours = json.dumps([f"{r['hour']:02d}" for r in three_elements])
    te_do = json.dumps([r["do"] for r in three_elements])
    te_temp = json.dumps([r["water_temp"] for r in three_elements])
    te_pressure = json.dumps([r["pressure"] for r in three_elements])
    te_colors = json.dumps([r["color"] for r in three_elements])
    te_labels = json.dumps([r["overall"] for r in three_elements])
    te_stars = json.dumps([r["stars"] for r in three_elements])

    # 本周钓鱼指数 JSON (用于图表)
    f7d_dates = json.dumps([d.get("day", "") for d in weekly_index[:7]])
    f7d_indices = json.dumps([d.get("index", 0) for d in weekly_index[:7]])
    f7d_ratings = json.dumps([d.get("rating", "") for d in weekly_index[:7]])
    f7d_temps = json.dumps([d.get("temp_range", "") for d in weekly_index[:7]])

    # 鱼种 HTML
    fish_html = ""
    medals = ["🥇", "🥈", "🥉"]
    for i, f in enumerate(fish_species[:10]):
        medal = medals[i] if i < 3 else f"#{i+1}"
        act = f.get("activity", "")
        src = f.get("source", "")
        src_badge = ""
        if src == "search":
            src_badge = '<span class="src-tag search">搜索</span>'
        elif src == "both":
            src_badge = '<span class="src-tag both">综合</span>'
        act_cls = "high" if "非常" in act else "med" if "活跃" in act else ""
        fish_html += f'''<div class="fish-item {act_cls}">
            <span class="medal">{medal}</span>
            <span class="fish-name">{f["name"]}</span>
            {src_badge}
            <span class="fish-activity">{act}</span>
        </div>\n'''

    # 附近钓点
    nearby = data.get("nearby_spots", [])
    spots_html = "".join(f'<div class="spot-item"><span class="spot-name">{s.get("name","")}</span><span class="spot-dist">{s.get("distance","")}</span></div>' for s in nearby[:5])

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0">
<title>🎣 钓鱼天气预报 — {city}</title>
<style>
:root {{
  --bg0:#0a1628;--bg1:#1a2744;--bg-card:rgba(26,39,68,0.85);
  --c1:#fff;--c2:#8b9cc0;--c3:#5a6b8a;
  --green:#4ade80;--yellow:#fbbf24;--red:#f87171;--blue:#60a5fa;--purple:#a78bfa;
  --bdr:rgba(255,255,255,0.08);
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg0);color:var(--c1);min-height:100vh;overflow-x:hidden}}
body::before{{content:'';position:fixed;inset:0;background:radial-gradient(1px 1px at 10% 20%,rgba(255,255,255,.6) 0%,transparent 100%),radial-gradient(1.5px 1.5px at 50% 10%,rgba(255,255,255,.7) 0%,transparent 100%),radial-gradient(1px 1px at 70% 30%,rgba(255,255,255,.5) 0%,transparent 100%),radial-gradient(1px 1px at 85% 60%,rgba(255,255,255,.3) 0%,transparent 100%),radial-gradient(1.5px 1.5px at 15% 70%,rgba(255,255,255,.5) 0%,transparent 100%),radial-gradient(1px 1px at 40% 80%,rgba(255,255,255,.4) 0%,transparent 100%),radial-gradient(ellipse at 50% 0%,rgba(26,39,68,1) 0%,var(--bg0) 70%);pointer-events:none;z-index:0}}
.ctn{{max-width:480px;margin:0 auto;padding:0 16px 80px;position:relative;z-index:1}}
.header{{text-align:center;padding:20px 0 10px}}
.header h1{{font-size:18px;font-weight:500}}.header .loc{{font-size:14px;color:var(--c2);margin-top:4px}}
.card{{background:var(--bg-card);backdrop-filter:blur(20px);border-radius:16px;padding:20px;margin-bottom:16px;border:1px solid var(--bdr)}}
.card-t{{font-size:14px;color:var(--c2);margin-bottom:12px;display:flex;align-items:center;gap:6px}}

/* 仪表盘 */
.idx-sec{{text-align:center;padding:16px 0}}
.idx-date{{font-size:13px;color:var(--c2)}}
.idx-main{{display:flex;align-items:center;justify-content:space-around;margin:16px 0}}
.idx-left{{text-align:left}}
.idx-rating{{font-size:32px;font-weight:bold;margin:6px 0}}
.fish-ic{{font-size:22px;letter-spacing:6px}}
.gauge-w{{position:relative;width:150px;height:150px}}
.gauge-w canvas{{width:100%;height:100%}}
.gauge-c{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}}
.gauge-s{{font-size:34px;font-weight:bold;color:{gauge_color}}}
.gauge-s span{{font-size:14px}}
.gauge-r{{font-size:11px;color:var(--c3);margin-top:2px}}
.best-t{{background:linear-gradient(135deg,rgba(251,191,36,.15),rgba(251,191,36,.05));border-radius:12px;padding:10px 16px;text-align:center;margin-top:10px;border:1px solid rgba(251,191,36,.2)}}
.best-t .lb{{color:var(--yellow);font-size:13px}}.best-t .tm{{color:var(--yellow);font-size:18px;font-weight:bold;margin-left:8px}}

/* 天气横排 */
.wx-row{{display:flex;gap:8px;overflow-x:auto;padding:4px 0;scrollbar-width:none}}.wx-row::-webkit-scrollbar{{display:none}}
.wx-it{{flex:0 0 auto;min-width:76px;background:var(--bg-card);border-radius:12px;padding:10px 8px;text-align:center;border:1px solid var(--bdr)}}
.wx-it .ic{{font-size:20px}}.wx-it .vl{{font-size:15px;font-weight:600;margin:3px 0}}.wx-it .lb{{font-size:10px;color:var(--c3)}}
.tag{{display:inline-block;font-size:9px;padding:1px 6px;border-radius:8px;margin-bottom:3px}}
.tag-g{{background:rgba(74,222,128,.2);color:var(--green)}}.tag-y{{background:rgba(251,191,36,.2);color:var(--yellow)}}.tag-r{{background:rgba(248,113,113,.2);color:var(--red)}}

/* 趋势图区域 */
.chart-tabs{{display:flex;gap:0;margin-bottom:12px;background:rgba(255,255,255,.06);border-radius:10px;padding:3px}}
.chart-tab{{flex:1;text-align:center;padding:6px 0;font-size:13px;color:var(--c3);border-radius:8px;cursor:pointer;transition:.2s}}
.chart-tab.on{{background:rgba(96,165,250,.2);color:var(--blue)}}
.legend-row{{display:flex;justify-content:center;gap:14px;margin-bottom:10px;flex-wrap:wrap}}
.leg-it{{display:flex;align-items:center;gap:4px;font-size:11px;color:var(--c2);cursor:pointer;user-select:none;transition:.2s}}
.leg-it.off{{opacity:.3}}.leg-it .dot{{width:8px;height:8px;border-radius:50%}}
.chart-wrap{{position:relative;width:100%;height:200px}}
.tooltip{{position:absolute;background:rgba(10,22,40,.95);border:1px solid var(--bdr);border-radius:8px;padding:8px 12px;font-size:11px;color:var(--c1);pointer-events:none;opacity:0;transition:opacity .15s;z-index:10;white-space:nowrap}}
/* 底部渐变色带 */
.color-strip{{position:relative;height:48px;margin:8px 0 0;border-radius:8px;overflow:hidden}}
.color-strip canvas{{width:100%;height:28px;border-radius:6px}}
.strip-labels{{display:flex;justify-content:space-between;padding:2px 0 0;font-size:9px;color:var(--c3)}}

/* 7天预报条形 */
.f7-row{{display:flex;gap:6px;justify-content:space-between}}
.f7-card{{flex:1;text-align:center;padding:10px 4px;background:rgba(255,255,255,.04);border-radius:10px}}
.f7-card .f7-dt{{font-size:11px;color:var(--c3)}}.f7-card .f7-ix{{font-size:20px;font-weight:bold;margin:4px 0}}

/* 鱼种 */
.fish-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.fish-item{{background:rgba(255,255,255,.04);border-radius:10px;padding:8px 10px;display:flex;align-items:center;gap:5px;font-size:12px}}
.fish-item.high{{background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.2)}}
.fish-item.med{{background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.15)}}
.medal{{font-size:14px}}.fish-name{{font-weight:500}}
.fish-activity{{color:var(--green);font-size:10px;margin-left:auto}}
.src-tag{{font-size:8px;padding:1px 4px;border-radius:4px}}
.src-tag.search{{background:rgba(96,165,250,.15);color:var(--blue)}}
.src-tag.both{{background:rgba(167,139,250,.15);color:var(--purple)}}

/* 装备 */
.gear-grid{{display:grid;gap:10px}}
.gear-it{{display:flex;gap:10px;align-items:flex-start}}
.gear-ic{{width:34px;height:34px;border-radius:10px;background:rgba(96,165,250,.1);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}}
.gear-lb{{font-size:11px;color:var(--c3)}}.gear-vl{{font-size:13px;margin-top:1px}}

/* 月相 */
.moon-row{{display:flex;gap:16px;font-size:13px}}
.moon-row>div{{flex:1;text-align:center}}.moon-row .ml{{font-size:11px;color:var(--c3);margin-bottom:4px}}

/* 折叠 */
.acc-h{{cursor:pointer;user-select:none;display:flex;justify-content:space-between;align-items:center}}
.acc-h::after{{content:'▸';color:var(--c3);transition:transform .2s}}.acc-h.open::after{{transform:rotate(90deg)}}
.acc-b{{max-height:0;overflow:hidden;transition:max-height .3s}}.acc-b.open{{max-height:2000px}}
.spot-item{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bdr);font-size:13px}}
.spot-name{{color:var(--c1)}}.spot-dist{{color:var(--c3);font-size:11px}}
.footer{{text-align:center;padding:28px 0;font-size:11px;color:var(--c3)}}
.sum-txt{{font-size:13px;line-height:1.8;color:var(--c2)}}
</style>
</head>
<body>
<div class="ctn">
  <div class="header"><h1>🎣 钓鱼天气预报</h1><div class="loc">📍 {city} · {time.strftime("%m/%d %A")}</div></div>

  <!-- 钓鱼指数 -->
  <div class="card idx-sec">
    <div class="idx-date">{time.strftime("%Y年%m月%d日")} · 今日钓鱼指数</div>
    <div class="idx-main">
      <div class="idx-left">
        <div class="idx-rating" style="color:{gauge_color}">{rating or '—'}</div>
        <div class="fish-ic">🐟🐟🐟</div>
      </div>
      <div class="gauge-w">
        <canvas id="gaugeC" width="300" height="300"></canvas>
        <div class="gauge-c"><div class="gauge-s">{current_index}<span>分</span></div><div class="gauge-r">⏱ 实时:{fi.get("realtime", current_index)}</div></div>
      </div>
    </div>
    {f'<div class="best-t"><span class="lb">⚡ 黄金垂钓时段:</span><span class="tm">{best_time}</span></div>' if best_time else ''}
  </div>

  {f'<div class="card"><div class="card-t">📝 今日建议</div><div class="sum-txt">{today_advice}</div></div>' if today_advice else (f'<div class="card"><div class="card-t">📝 今日分析</div><div class="sum-txt">{summary}</div></div>' if summary else '')}

  <!-- 天气横排 -->
  <div class="wx-row">
    <div class="wx-it"><div class="ic">{'☀️' if '晴' in weather.get('condition','') else '☁️' if '云' in weather.get('condition','') else '🌧️' if '雨' in weather.get('condition','') else '⛅'}</div><div class="vl">{weather.get('condition','—')}</div><div class="lb">当前天气</div></div>
    <div class="wx-it"><div class="tag tag-g">气温</div><div class="vl">{weather.get('temp','—')}°C</div><div class="lb">{weather.get('temp_min','') or ''}° ~ {weather.get('temp_max','') or ''}°</div></div>
    <div class="wx-it"><div class="ic">🌊</div><div class="vl">{water.get('water_temp','—')}°C</div><div class="lb">水温 {water.get('water_temp_eval','')}</div></div>
    <div class="wx-it"><div class="tag {'tag-g' if (water.get('do') or 0)>=6 else 'tag-y' if (water.get('do') or 0)>=4.5 else 'tag-r' if water.get('do') else 'tag-y'}">溶氧</div><div class="vl">{water.get('do') or 'N/A'}<span style="font-size:10px">{'mg/L' if water.get('do') else ''}</span></div><div class="lb">{water.get('do_eval','') or '数据获取中'}</div></div>
    <div class="wx-it"><div class="tag {'tag-g' if pressure_trend.get('change_24h',0)>0 else 'tag-r' if pressure_trend.get('change_24h',0)<0 else 'tag-y'}">气压</div><div class="vl">{weather.get('pressure','—')}<span style="font-size:9px">hPa</span></div><div class="lb">{weather.get('pressure_eval','')} {'↑' if pressure_trend.get('change_24h',0)>0 else '↓' if pressure_trend.get('change_24h',0)<0 else ''}{abs(pressure_trend.get('change_24h',0)) if pressure_trend.get('change_24h') else ''}</div></div>
  </div>

  <!-- 趋势图（24h / 7天 切换） -->
  <div class="card">
    <div class="card-t">📈 趋势分析</div>
    <div class="chart-tabs">
      <div class="chart-tab on" onclick="switchTab('24h',this)">24小时</div>
      <div class="chart-tab" onclick="switchTab('7d',this)">7天预报</div>
    </div>
    <!-- 24h 视图 -->
    <div id="view24h">
      <div class="legend-row">
        <div class="leg-it" data-line="do" onclick="toggleLine('do',this)"><span class="dot" style="background:#38a169"></span>溶氧(mg/L)</div>
        <div class="leg-it" data-line="temp" onclick="toggleLine('temp',this)"><span class="dot" style="background:#e53e3e"></span>水温(°C)</div>
        <div class="leg-it" data-line="press" onclick="toggleLine('press',this)"><span class="dot" style="background:#805ad5"></span>气压(hPa)</div>
      </div>
      <div class="chart-wrap" id="chartWrap24">
        <canvas id="chart24"></canvas>
        <div class="tooltip" id="tip24"></div>
      </div>
      <div class="color-strip" id="strip24">
        <canvas id="stripCanvas"></canvas>
        <div class="strip-labels" id="stripLabels"></div>
      </div>
    </div>
    <!-- 7天 视图 -->
    <div id="view7d" style="display:none">
      <div class="chart-wrap" id="chartWrap7d">
        <canvas id="chart7d"></canvas>
        <div class="tooltip" id="tip7d"></div>
      </div>
      <div class="f7-row" id="f7Row"></div>
    </div>
  </div>

  <!-- 7天预报卡片 -->
  <!-- (已集成到趋势图Tab) -->

  <!-- 活跃鱼种 -->
  {'<div class="card"><div class="card-t">🐟 活跃鱼种</div><div class="fish-grid">' + fish_html + '</div></div>' if fish_html else ''}

  <!-- 出钓建议 -->
  <div class="card">
    <div class="card-t">🎣 出钓建议</div>
    <div class="gear-grid">
      {f'<div class="gear-it"><div class="gear-ic">📍</div><div><div class="gear-lb">推荐钓位</div><div class="gear-vl">{gear.get("position","—")}</div></div></div>' if gear.get("position") else ''}
      {f'<div class="gear-it"><div class="gear-ic">🪱</div><div><div class="gear-lb">饵料选择</div><div class="gear-vl">{gear.get("bait","—")}</div></div></div>' if gear.get("bait") else ''}
      {f'<div class="gear-it"><div class="gear-ic">🎣</div><div><div class="gear-lb">线组参考</div><div class="gear-vl">{gear.get("line_group","—")}</div></div></div>' if gear.get("line_group") else ''}
    </div>
  </div>

  <!-- 月相 -->
  <div class="card">
    <div class="card-t">🌙 月相信息</div>
    <div class="moon-row">
      <div><div class="ml">月相</div>{moon.get('name','—')}</div>
      <div><div class="ml">垂钓</div>{moon.get('fishing_eval','—')}</div>
      <div><div class="ml">评分</div>{moon.get('score','—')}</div>
      <div><div class="ml">照明度</div>{moon.get('illumination','—')}</div>
      <div><div class="ml">月龄</div>{moon.get('age','—')}天</div>
    </div>
    {f'<div style="margin-top:10px;font-size:12px;color:var(--c2)">{moon.get("description","")}</div>' if moon.get("description") else ''}
  </div>

  {'<div class="card"><div class="acc-h card-t" onclick="toggleAcc(this)">🎯 附近钓点</div><div class="acc-b">' + spots_html + '</div></div>' if spots_html else ''}

  <div class="footer">🎣 钓鱼天气顾问 v4.1 | 数据源: fishweather.cn<br>{time.strftime("%Y-%m-%d %H:%M:%S")}</div>
</div>

<script>
const TE_H={te_hours},TE_DO={te_do},TE_T={te_temp},TE_P={te_pressure},TE_CL={te_colors},TE_LB={te_labels},TE_ST={te_stars};
const F7_D={f7d_dates},F7_I={f7d_indices},F7_R={f7d_ratings},F7_T={f7d_temps};
const lineVis={{do:true,temp:true,press:true}};

function switchTab(tab,el){{
  document.querySelectorAll('.chart-tab').forEach(t=>t.classList.remove('on'));
  el.classList.add('on');
  document.getElementById('view24h').style.display=tab==='24h'?'':'none';
  document.getElementById('view7d').style.display=tab==='7d'?'':'none';
  if(tab==='7d')draw7d();
}}
function toggleLine(key,el){{lineVis[key]=!lineVis[key];el.classList.toggle('off');draw24h()}}
function toggleAcc(h){{h.classList.toggle('open');h.nextElementSibling.classList.toggle('open')}}

function drawSmooth(ctx,pts,color,lw){{
  if(pts.length<2)return;
  ctx.save();ctx.strokeStyle=color;ctx.lineWidth=lw||2;
  ctx.lineJoin='round';ctx.lineCap='round';
  ctx.shadowColor=color;ctx.shadowBlur=8;
  ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);
  for(let i=0;i<pts.length-1;i++){{
    const p=pts[Math.max(i-1,0)],c=pts[i],n=pts[i+1],nn=pts[Math.min(i+2,pts.length-1)];
    const t=0.3;
    ctx.bezierCurveTo(c[0]+(n[0]-p[0])*t,c[1]+(n[1]-p[1])*t,n[0]-(nn[0]-c[0])*t,n[1]-(nn[1]-c[1])*t,n[0],n[1]);
  }}
  ctx.stroke();ctx.restore();
}}
function rng(a){{const mn=Math.min(...a),mx=Math.max(...a),m=(mx-mn)*.18||1;return[mn-m,mx+m]}}
function ic(v){{return v>=80?'#60a5fa':v>=65?'#4ade80':v>=50?'#fbbf24':v>=35?'#fb923c':'#f87171'}}

function draw24h(){{
  const cvs=document.getElementById('chart24'),wrap=document.getElementById('chartWrap24');
  if(!cvs||!wrap)return;
  const W=wrap.clientWidth||448,H=200;
  cvs.width=W*2;cvs.height=H*2;cvs.style.width=W+'px';cvs.style.height=H+'px';
  const ctx=cvs.getContext('2d');ctx.scale(2,2);
  const pad={{t:15,r:42,b:28,l:38}},cw=W-pad.l-pad.r,ch=H-pad.t-pad.b,n=TE_H.length;
  const xp=i=>pad.l+i/(n-1)*cw;
  ctx.strokeStyle='rgba(255,255,255,.05)';ctx.lineWidth=.5;
  for(let i=0;i<5;i++){{const y=pad.t+i/4*ch;ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke()}}
  const ds=[{{key:'do',d:TE_DO,c:'#38a169'}},{{key:'temp',d:TE_T,c:'#e53e3e'}},{{key:'press',d:TE_P,c:'#805ad5'}}];
  ds.forEach(s=>{{
    if(!lineVis[s.key])return;
    const[mn,mx]=rng(s.d);const yF=v=>pad.t+(1-(v-mn)/(mx-mn))*ch;
    const pts=s.d.map((v,i)=>[xp(i),yF(v)]);
    drawSmooth(ctx,pts,s.c,2);
    ctx.font='9px sans-serif';ctx.fillStyle=s.c+'aa';
    if(s.key==='do'){{ctx.textAlign='right';for(let i=0;i<=3;i++){{const v=mn+(mx-mn)*(1-i/3);ctx.fillText(v.toFixed(1),pad.l-3,pad.t+i/3*ch+3)}}}}
    if(s.key==='temp'){{ctx.textAlign='left';for(let i=0;i<=3;i++){{const v=mn+(mx-mn)*(1-i/3);ctx.fillText(v.toFixed(0)+'\u00b0',W-pad.r+3,pad.t+i/3*ch+3)}}}}
  }});
  ctx.fillStyle='rgba(255,255,255,.35)';ctx.font='9px sans-serif';ctx.textAlign='center';
  for(let i=0;i<n;i+=3)ctx.fillText(TE_H[i],xp(i),H-pad.b+14);
  cvs._meta={{pad,cw,ch,n,W,H}};
}}

document.getElementById('chart24').addEventListener('mousemove',function(e){{
  const r=this.getBoundingClientRect(),mx=e.clientX-r.left,m=this._meta;if(!m)return;
  const idx=Math.round((mx-m.pad.l)/m.cw*(m.n-1));
  if(idx<0||idx>=m.n){{document.getElementById('tip24').style.opacity=0;return}}
  const tip=document.getElementById('tip24');
  tip.innerHTML='<b>'+TE_H[idx]+':00</b><br>\u6eb6\u6c27: '+TE_DO[idx]+'mg/L<br>\u6c34\u6e29: '+TE_T[idx]+'\u00b0C<br>\u6c14\u538b: '+TE_P[idx]+'hPa<br>'+TE_LB[idx]+' '+TE_ST[idx];
  tip.style.opacity=1;tip.style.left=Math.min(mx+10,m.W-130)+'px';tip.style.top='10px';
}});
document.getElementById('chart24').addEventListener('mouseleave',function(){{document.getElementById('tip24').style.opacity=0}});

function drawStrip(){{
  const cvs=document.getElementById('stripCanvas'),wrap=document.getElementById('strip24');
  if(!cvs||!wrap)return;
  const W=wrap.clientWidth||448;cvs.width=W*2;cvs.height=56;cvs.style.width=W+'px';cvs.style.height='28px';
  const ctx=cvs.getContext('2d');ctx.scale(2,2);
  const pad={{l:38,r:42}},n=TE_CL.length,cw=W-pad.l-pad.r;
  const sxp=i=>pad.l+i/(n-1)*cw;
  for(let i=0;i<n-1;i++){{
    const x1=sxp(i),x2=sxp(i+1);
    const g=ctx.createLinearGradient(x1,0,x2,0);g.addColorStop(0,TE_CL[i]);g.addColorStop(1,TE_CL[i+1]);
    ctx.fillStyle=g;ctx.fillRect(x1,0,x2-x1+1,28);
  }}
  const lb=document.getElementById('stripLabels');lb.innerHTML='';
  const lblPad=pad.l+'px';const lblPadR=pad.r+'px';
  lb.style.paddingLeft=lblPad;lb.style.paddingRight=lblPadR;
  for(let i=0;i<n;i+=3){{const sp=document.createElement('span');sp.textContent=TE_H[i];lb.appendChild(sp)}}
}}

function draw7d(){{
  if(F7_D.length===0)return;
  const cvs=document.getElementById('chart7d'),wrap=document.getElementById('chartWrap7d');
  if(!cvs||!wrap)return;
  const W=wrap.clientWidth||448,H=200;cvs.width=W*2;cvs.height=H*2;cvs.style.width=W+'px';cvs.style.height=H+'px';
  const ctx=cvs.getContext('2d');ctx.scale(2,2);
  const pad={{t:20,r:20,b:40,l:20}},cw=W-pad.l-pad.r,ch=H-pad.t-pad.b,n=F7_I.length,gap=cw/n,barW=gap*.6;
  const mx=Math.max(...F7_I,70),mn=Math.min(...F7_I,30);
  F7_I.forEach((v,i)=>{{
    const bh=Math.max((v-mn)/(mx-mn)*ch,8),bx=pad.l+i*gap+(gap-barW)/2,by=pad.t+ch-bh,cl=ic(v);
    const g=ctx.createLinearGradient(0,by,0,by+bh);g.addColorStop(0,cl);g.addColorStop(1,cl+'40');ctx.fillStyle=g;
    const r=4;ctx.beginPath();ctx.moveTo(bx+r,by);ctx.lineTo(bx+barW-r,by);ctx.quadraticCurveTo(bx+barW,by,bx+barW,by+r);ctx.lineTo(bx+barW,by+bh-r);ctx.quadraticCurveTo(bx+barW,by+bh,bx+barW-r,by+bh);ctx.lineTo(bx+r,by+bh);ctx.quadraticCurveTo(bx,by+bh,bx,by+bh-r);ctx.lineTo(bx,by+r);ctx.quadraticCurveTo(bx,by,bx+r,by);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='bold 13px sans-serif';ctx.textAlign='center';ctx.fillText(v,bx+barW/2,by-6);
    ctx.fillStyle='rgba(255,255,255,.45)';ctx.font='10px sans-serif';ctx.fillText(F7_D[i],bx+barW/2,H-pad.b+14);
  }});
  cvs._meta7={{pad,gap,barW,n,W,H}};
}}
document.getElementById('chart7d').addEventListener('mousemove',function(e){{
  const r=this.getBoundingClientRect(),mx=e.clientX-r.left,m=this._meta7;if(!m)return;
  const idx=Math.floor((mx-m.pad.l)/m.gap);
  if(idx<0||idx>=m.n){{document.getElementById('tip7d').style.opacity=0;return}}
  const tip=document.getElementById('tip7d');
  tip.innerHTML='<b>'+F7_D[idx]+'</b><br>\u9493\u9c7c\u6307\u6570: '+F7_I[idx]+'\u5206 '+F7_R[idx]+'<br>\u6e29\u5ea6: '+F7_T[idx];
  tip.style.opacity=1;tip.style.left=Math.min(mx+10,m.W-100)+'px';tip.style.top='10px';
}});
document.getElementById('chart7d').addEventListener('mouseleave',function(){{document.getElementById('tip7d').style.opacity=0}});

function initCharts(){{
  try{{
    const c=document.getElementById('gaugeC');if(c){{
      const ctx=c.getContext('2d'),W=c.width,H=c.height,cx=W/2,cy=H/2,r=W/2-16,score={current_index};
      ctx.beginPath();ctx.arc(cx,cy,r,.75*Math.PI,.25*Math.PI);ctx.strokeStyle='rgba(255,255,255,.06)';ctx.lineWidth=12;ctx.lineCap='round';ctx.stroke();
      const sa=.75*Math.PI,ea=sa+(score/100)*1.5*Math.PI;
      const segs=[{{s:0,e:.2,c:'#f87171'}},{{s:.2,e:.35,c:'#fb923c'}},{{s:.35,e:.5,c:'#fbbf24'}},{{s:.5,e:.7,c:'#4ade80'}},{{s:.7,e:.85,c:'#60a5fa'}},{{s:.85,e:1,c:'#818cf8'}}];
      segs.forEach(seg=>{{
        const a1=sa+seg.s*1.5*Math.PI,a2=sa+seg.e*1.5*Math.PI;
        if(a1<ea){{
          ctx.beginPath();ctx.arc(cx,cy,r,a1,Math.min(a2,ea));ctx.strokeStyle=seg.c;ctx.lineWidth=12;ctx.lineCap='butt';ctx.stroke();
        }}
      }});
      ctx.shadowColor='{gauge_color}';ctx.shadowBlur=12;ctx.beginPath();ctx.arc(cx,cy,r,ea-.05,ea);ctx.strokeStyle='{gauge_color}';ctx.lineWidth=12;ctx.lineCap='round';ctx.stroke();ctx.shadowBlur=0;
    }}
  }}catch(e){{console.warn('gauge error',e)}}
  try{{draw24h()}}catch(e){{console.warn('draw24h error',e)}}
  try{{drawStrip()}}catch(e){{console.warn('drawStrip error',e)}}
  try{{
    const c=document.getElementById('f7Row');
    F7_D.forEach((d,i)=>{{
      const v=F7_I[i],cl=ic(v);
      c.innerHTML+='<div class="f7-card"><div class="f7-dt">'+d+'</div><div class="f7-ix" style="color:'+cl+'">'+v+'</div><div style="font-size:10px;color:rgba(255,255,255,.4)">'+F7_R[i]+'</div><div style="font-size:9px;color:rgba(255,255,255,.3);margin-top:2px">'+F7_T[i]+'</div></div>';
    }});
  }}catch(e){{console.warn('f7row error',e)}}
}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>requestAnimationFrame(initCharts));
else requestAnimationFrame(initCharts);
</script>
</body>
</html>'''

    filepath.write_text(html, encoding="utf-8")
    return str(filepath)


def _index_to_color(index: int) -> str:
    if index >= 80: return "#60a5fa"
    elif index >= 65: return "#4ade80"
    elif index >= 50: return "#fbbf24"
    elif index >= 35: return "#fb923c"
    else: return "#f87171"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-file", required=True)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()
    data = json.loads(Path(args.data_file).read_text(encoding="utf-8"))
    from three_elements import analyze_three_elements
    te = analyze_three_elements(data)
    print(f"HTML: {generate_html(data, te, args.output_dir)}")
