"""Step 3 - Build a self-contained interactive HTML dashboard (filters: Category, Region, Month)."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "cleaned_sales_data.csv")
cols = ["Category", "Region", "Month", "Month Number", "Product Name", "Sales", "Profit", "Order ID"]
data = json.dumps(df[cols].to_dict("records"))

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sales Performance Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{--bg:#f4f6fb;--card:#fff;--text:#1e293b;--muted:#64748b;--line:#e2e8f0;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#0f172a;--card:#1e293b;--text:#e2e8f0;--muted:#94a3b8;--line:#334155;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;background:var(--bg);color:var(--text);padding:20px}
h1{margin:0 0 4px;font-size:24px}.sub{color:var(--muted);margin-bottom:16px}
.filters{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.filters label{font-size:12px;color:var(--muted);display:flex;flex-direction:column;gap:4px}
select,button{padding:8px 10px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--text);font-size:14px}
button{cursor:pointer;align-self:flex-end}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.kpi .l{font-size:12px;color:var(--muted)}.kpi .v{font-size:26px;font-weight:700;margin-top:4px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:12px}
.card h3{margin:0 0 8px;font-size:15px}.box{position:relative;height:290px}
@media(max-width:480px){.grid{grid-template-columns:1fr}}
</style></head><body>
<h1>Sales Performance Dashboard</h1><div class="sub">Retail sales, 2025 - Cognevance Technologies project</div>
<div class="filters">
<label>Category<select id="fCat"></select></label>
<label>Region<select id="fReg"></select></label>
<label>Month<select id="fMon"></select></label>
<button onclick="resetF()">Reset filters</button></div>
<div class="kpis">
<div class="card kpi"><div class="l">Total Sales</div><div class="v" id="kS"></div></div>
<div class="card kpi"><div class="l">Total Profit</div><div class="v" id="kP"></div></div>
<div class="card kpi"><div class="l">Profit Margin</div><div class="v" id="kM"></div></div>
<div class="card kpi"><div class="l">Orders</div><div class="v" id="kO"></div></div></div>
<div class="grid">
<div class="card"><h3>Monthly Sales and Profit</h3><div class="box"><canvas id="c1"></canvas></div></div>
<div class="card"><h3>Sales by Category</h3><div class="box"><canvas id="c2"></canvas></div></div>
<div class="card"><h3>Sales and Profit by Region</h3><div class="box"><canvas id="c3"></canvas></div></div>
<div class="card"><h3>Top 10 Products by Sales</h3><div class="box"><canvas id="c4"></canvas></div></div></div>
<script>
const DATA=__DATA__;
const MONTHS=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const uniq=k=>[...new Set(DATA.map(d=>d[k]))].sort();
const fill=(id,vals)=>{const s=document.getElementById(id);s.innerHTML='<option>All</option>'+vals.map(v=>`<option>${v}</option>`).join('');s.onchange=update};
fill('fCat',uniq('Category'));fill('fReg',uniq('Region'));fill('fMon',MONTHS);
const fmt=n=>Math.round(n).toLocaleString('en-IN');
const COL=['#2563eb','#16a34a','#f59e0b','#dc2626','#7c3aed'];
const mk=(id,cfg)=>new Chart(document.getElementById(id),cfg);
const base={responsive:true,maintainAspectRatio:false};
const ch={
 c1:mk('c1',{type:'line',data:{labels:MONTHS,datasets:[{label:'Sales',borderColor:COL[0],tension:.3},{label:'Profit',borderColor:COL[1],tension:.3}]},options:base}),
 c2:mk('c2',{type:'doughnut',data:{labels:[],datasets:[{backgroundColor:COL}]},options:base}),
 c3:mk('c3',{type:'bar',data:{labels:[],datasets:[{label:'Sales',backgroundColor:COL[0]},{label:'Profit',backgroundColor:COL[1]}]},options:base}),
 c4:mk('c4',{type:'bar',data:{labels:[],datasets:[{label:'Sales',backgroundColor:COL[0]}]},options:{...base,indexAxis:'y',plugins:{legend:{display:false}}}})};
const grp=(rows,k)=>{const m={};rows.forEach(r=>{m[r[k]]=m[r[k]]||{s:0,p:0};m[r[k]].s+=r.Sales;m[r[k]].p+=r.Profit});return m};
function update(){
 const c=fCat.value,r=fReg.value,m=fMon.value;
 const rows=DATA.filter(d=>(c=='All'||d.Category==c)&&(r=='All'||d.Region==r)&&(m=='All'||d.Month==m));
 const S=rows.reduce((a,d)=>a+d.Sales,0),P=rows.reduce((a,d)=>a+d.Profit,0);
 kS.textContent=fmt(S);kP.textContent=fmt(P);kM.textContent=(S?P/S*100:0).toFixed(1)+'%';kO.textContent=new Set(rows.map(d=>d['Order ID'])).size.toLocaleString();
 const mo=grp(rows,'Month');
 ch.c1.data.datasets[0].data=MONTHS.map(x=>mo[x]?mo[x].s:0);ch.c1.data.datasets[1].data=MONTHS.map(x=>mo[x]?mo[x].p:0);
 const ca=grp(rows,'Category');ch.c2.data.labels=Object.keys(ca);ch.c2.data.datasets[0].data=Object.values(ca).map(v=>v.s);
 const rg=grp(rows,'Region');ch.c3.data.labels=Object.keys(rg);ch.c3.data.datasets[0].data=Object.values(rg).map(v=>v.s);ch.c3.data.datasets[1].data=Object.values(rg).map(v=>v.p);
 const pr=Object.entries(grp(rows,'Product Name')).sort((a,b)=>b[1].s-a[1].s).slice(0,10);
 ch.c4.data.labels=pr.map(x=>x[0]);ch.c4.data.datasets[0].data=pr.map(x=>x[1].s);
 Object.values(ch).forEach(x=>x.update());
}
function resetF(){fCat.value=fReg.value=fMon.value='All';update()}
update();
</script></body></html>"""
(ROOT / "dashboard" / "sales_dashboard.html").write_text(HTML.replace("__DATA__", data), encoding="utf-8")
print("Dashboard saved to dashboard/sales_dashboard.html")
