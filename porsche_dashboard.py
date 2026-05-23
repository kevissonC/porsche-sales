import pandas as pd
import json
import sys
import os

def load_data(filepath):
    df = pd.read_excel(filepath)
    df.columns = ['sale_id', 'sale_date', 'customer_name', 'model', 'model_year',
                  'sale_price', 'mileage', 'pay_method', 'city', 'state',
                  'salesperson', 'delivery_status']
    df['model_year'] = df['model_year'].astype(str)
    df['sale_price'] = pd.to_numeric(df['sale_price'], errors='coerce').fillna(0)
    return df

def build_dashboard(df, output_path):
    # Prepare filter options
    models = sorted(df['model'].dropna().unique().tolist())
    years = sorted(df['model_year'].dropna().unique().tolist())
    cities = sorted(df['city'].dropna().unique().tolist())
    pay_methods = sorted(df['pay_method'].dropna().unique().tolist())

    # Serialize all records to JSON for JS filtering
    records = df.fillna('').to_dict(orient='records')
    records_json = json.dumps(records, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Porsche Sales Intelligence</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Neue+Haas+Grotesk+Display+Pro:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  :root {{
    --black: #0a0a0a;
    --dark: #111111;
    --dark2: #1a1a1a;
    --dark3: #242424;
    --gold: #c9a84c;
    --gold-light: #e2c47a;
    --gold-dim: rgba(201,168,76,0.15);
    --white: #f5f0e8;
    --white-dim: rgba(245,240,232,0.55);
    --white-faint: rgba(245,240,232,0.08);
    --red: #d4393b;
    --border: rgba(201,168,76,0.18);
    --border-subtle: rgba(245,240,232,0.07);
  }}

  * {{ margin:0; padding:0; box-sizing:border-box; }}

  body {{
    background: var(--black);
    color: var(--white);
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    min-height: 100vh;
    overflow-x: hidden;
  }}

  /* ── Header ── */
  header {{
    position: sticky; top: 0; z-index: 100;
    background: rgba(10,10,10,0.96);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border);
    padding: 0 48px;
    display: flex; align-items: center; justify-content: space-between;
    height: 72px;
  }}
  .logo {{
    display: flex; align-items: center; gap: 16px;
  }}
  .logo-crest {{
    width: 38px; height: 38px;
    background: var(--gold);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: var(--black);
    letter-spacing: 0.05em;
  }}
  .logo-text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px; font-weight: 600;
    letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--white);
  }}
  .logo-sub {{
    font-size: 9px; letter-spacing: 0.35em; text-transform: uppercase;
    color: var(--gold); opacity: 0.8;
    margin-top: 1px;
  }}
  .header-right {{
    font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--white-dim);
  }}

  /* ── Hero strip ── */
  .hero-strip {{
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1208 50%, #0a0a0a 100%);
    border-bottom: 1px solid var(--border);
    padding: 40px 48px 36px;
    position: relative; overflow: hidden;
  }}
  .hero-strip::before {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
  }}
  .hero-strip::after {{
    content: 'PORSCHE';
    position: absolute; right: -20px; top: 50%; transform: translateY(-50%);
    font-family: 'Cormorant Garamond', serif;
    font-size: 120px; font-weight: 700; letter-spacing: 0.08em;
    color: rgba(201,168,76,0.04); pointer-events: none;
    white-space: nowrap;
  }}
  .hero-title {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 13px; font-weight: 400; letter-spacing: 0.3em;
    text-transform: uppercase; color: var(--gold);
    margin-bottom: 10px;
  }}
  .hero-h1 {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 48px; font-weight: 300; line-height: 1.1;
    color: var(--white); letter-spacing: 0.02em;
  }}
  .hero-h1 span {{ color: var(--gold); font-weight: 600; }}

  /* ── KPI row ── */
  .kpi-row {{
    display: grid; grid-template-columns: repeat(4, 1fr);
    border-bottom: 1px solid var(--border-subtle);
  }}
  .kpi {{
    padding: 28px 32px;
    border-right: 1px solid var(--border-subtle);
    position: relative; transition: background .25s;
  }}
  .kpi:last-child {{ border-right: none; }}
  .kpi:hover {{ background: var(--white-faint); }}
  .kpi-label {{
    font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase;
    color: var(--gold); margin-bottom: 10px;
  }}
  .kpi-value {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 38px; font-weight: 600; color: var(--white);
    line-height: 1;
  }}
  .kpi-sub {{
    font-size: 11px; color: var(--white-dim); margin-top: 6px;
  }}

  /* ── Filters ── */
  .filters-section {{
    background: var(--dark);
    border-bottom: 1px solid var(--border);
    padding: 24px 48px;
  }}
  .filters-label {{
    font-size: 10px; letter-spacing: 0.3em; text-transform: uppercase;
    color: var(--gold); margin-bottom: 14px;
  }}
  .filters-grid {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
  }}
  .filter-wrap {{ position: relative; }}
  .filter-wrap select {{
    width: 100%;
    background: var(--dark2);
    border: 1px solid var(--border);
    color: var(--white);
    padding: 11px 36px 11px 14px;
    font-family: 'DM Sans', sans-serif;
    font-size: 12px; letter-spacing: 0.06em;
    border-radius: 0;
    appearance: none; cursor: pointer;
    transition: border-color .2s, background .2s;
    outline: none;
  }}
  .filter-wrap select:hover, .filter-wrap select:focus {{
    border-color: var(--gold); background: var(--dark3);
  }}
  .filter-wrap::after {{
    content: '▾';
    position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
    color: var(--gold); pointer-events: none; font-size: 12px;
  }}
  .filter-wrap label {{
    display: block; font-size: 10px; letter-spacing: 0.2em;
    text-transform: uppercase; color: var(--white-dim); margin-bottom: 7px;
  }}
  .btn-reset {{
    align-self: flex-end;
    background: transparent; border: 1px solid var(--border);
    color: var(--white-dim); padding: 11px 24px;
    font-family: 'DM Sans', sans-serif; font-size: 11px;
    letter-spacing: 0.18em; text-transform: uppercase;
    cursor: pointer; transition: all .2s;
  }}
  .btn-reset:hover {{ border-color: var(--gold); color: var(--gold); }}

  /* ── Main grid ── */
  .main-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 1px;
    background: var(--border-subtle);
    border-top: 1px solid var(--border-subtle);
  }}
  .chart-panel {{
    background: var(--dark);
    padding: 32px 36px;
    position: relative;
  }}
  .chart-panel.full-width {{ grid-column: 1 / -1; }}
  .panel-label {{
    font-size: 10px; letter-spacing: 0.28em; text-transform: uppercase;
    color: var(--gold); margin-bottom: 6px;
  }}
  .panel-title {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px; font-weight: 400; color: var(--white);
    margin-bottom: 28px; letter-spacing: 0.02em;
  }}
  .chart-wrap {{ position: relative; height: 280px; }}

  /* ── Insight cards ── */
  .insights-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 1px; background: var(--border-subtle);
  }}
  .insight-card {{
    background: var(--dark2);
    padding: 28px 32px;
    border-top: 2px solid transparent;
    transition: border-color .25s, background .25s;
  }}
  .insight-card:hover {{ border-top-color: var(--gold); background: var(--dark3); }}
  .insight-rank {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px; font-weight: 700;
    color: var(--gold-dim); line-height: 1;
    margin-bottom: 12px;
    background: linear-gradient(180deg, var(--gold) 0%, rgba(201,168,76,0.2) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .insight-model {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px; font-weight: 600;
    color: var(--white); margin-bottom: 6px;
  }}
  .insight-city {{
    font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--gold); margin-bottom: 12px;
  }}
  .insight-stat {{
    font-size: 12px; color: var(--white-dim); line-height: 1.8;
  }}
  .insight-stat span {{ color: var(--white); }}

  /* ── Table ── */
  .table-section {{
    background: var(--dark); padding: 32px 36px;
    border-top: 1px solid var(--border-subtle);
  }}
  .table-header {{
    display: flex; justify-content: space-between; align-items: flex-end;
    margin-bottom: 20px;
  }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; }}
  thead th {{
    text-align: left;
    font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--gold); padding: 0 16px 12px 0;
    border-bottom: 1px solid var(--border);
    font-weight: 400;
  }}
  tbody tr {{
    border-bottom: 1px solid var(--border-subtle);
    transition: background .15s;
  }}
  tbody tr:hover {{ background: var(--white-faint); }}
  tbody td {{
    padding: 13px 16px 13px 0;
    color: var(--white-dim);
  }}
  tbody td:first-child {{ color: var(--white); font-weight: 400; }}
  .badge {{
    display: inline-block;
    padding: 3px 10px;
    font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;
    border: 1px solid;
  }}
  .badge-delivered {{ border-color: #3d7a4f; color: #5cad72; background: rgba(92,173,114,0.08); }}
  .badge-transit {{ border-color: var(--gold); color: var(--gold); background: var(--gold-dim); }}
  .badge-pending {{ border-color: #888; color: #aaa; background: rgba(150,150,150,0.07); }}

  footer {{
    background: var(--black);
    border-top: 1px solid var(--border);
    padding: 24px 48px;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--white-dim);
  }}
  footer span {{ color: var(--gold); }}

  #count-label {{
    font-size: 11px; color: var(--white-dim);
    letter-spacing: 0.1em;
  }}
  #count-label b {{ color: var(--gold); }}
</style>
</head>
<body>

<header>
  <div class="logo">
    <div class="logo-crest">P</div>
    <div>
      <div class="logo-text">Porsche</div>
      <div class="logo-sub">Sales Intelligence</div>
    </div>
  </div>
  <div class="header-right">Dashboard Comercial &nbsp;·&nbsp; <span style="color:var(--gold)">Analytics</span></div>
</header>

<div class="hero-strip">
  <div class="hero-title">Visão Executiva de Vendas</div>
  <div class="hero-h1">Performance &amp; <span>Insights</span></div>
</div>

<!-- KPIs -->
<div class="kpi-row" id="kpi-row">
  <div class="kpi"><div class="kpi-label">Total de Vendas</div><div class="kpi-value" id="kpi-total">—</div><div class="kpi-sub">registros filtrados</div></div>
  <div class="kpi"><div class="kpi-label">Receita Total</div><div class="kpi-value" id="kpi-revenue">—</div><div class="kpi-sub">USD acumulado</div></div>
  <div class="kpi"><div class="kpi-label">Ticket Médio</div><div class="kpi-value" id="kpi-avg">—</div><div class="kpi-sub">por veículo</div></div>
  <div class="kpi"><div class="kpi-label">Cidades Ativas</div><div class="kpi-value" id="kpi-cities">—</div><div class="kpi-sub">mercados atendidos</div></div>
</div>

<!-- Filters -->
<div class="filters-section">
  <div class="filters-label">Filtros de Análise</div>
  <div class="filters-grid">
    <div class="filter-wrap">
      <label>Modelo</label>
      <select id="f-model">
        <option value="">Todos os Modelos</option>
        {''.join(f'<option value="{m}">{m}</option>' for m in models)}
      </select>
    </div>
    <div class="filter-wrap">
      <label>Model Year</label>
      <select id="f-year">
        <option value="">Todos os Anos</option>
        {''.join(f'<option value="{y}">{y}</option>' for y in years)}
      </select>
    </div>
    <div class="filter-wrap">
      <label>Cidade</label>
      <select id="f-city">
        <option value="">Todas as Cidades</option>
        {''.join(f'<option value="{c}">{c}</option>' for c in cities)}
      </select>
    </div>
    <div class="filter-wrap">
      <label>Forma de Pagamento</label>
      <select id="f-pay">
        <option value="">Todas as Formas</option>
        {''.join(f'<option value="{p}">{p}</option>' for p in pay_methods)}
      </select>
    </div>
  </div>
  <div style="margin-top:14px; display:flex; justify-content:space-between; align-items:center;">
    <span id="count-label"><b>—</b> registros encontrados</span>
    <button class="btn-reset" onclick="resetFilters()">↺ &nbsp;Limpar Filtros</button>
  </div>
</div>

<!-- Charts -->
<div class="main-grid">
  <div class="chart-panel">
    <div class="panel-label">Análise por Cidade</div>
    <div class="panel-title">Modelos Mais Vendidos por Cidade</div>
    <div class="chart-wrap"><canvas id="chart-city"></canvas></div>
  </div>
  <div class="chart-panel">
    <div class="panel-label">Tendência Temporal</div>
    <div class="panel-title">Distribuição por Ano de Modelo</div>
    <div class="chart-wrap"><canvas id="chart-year"></canvas></div>
  </div>
  <div class="chart-panel">
    <div class="panel-label">Forma de Pagamento</div>
    <div class="panel-title">Mix de Pagamentos</div>
    <div class="chart-wrap"><canvas id="chart-pay"></canvas></div>
  </div>
  <div class="chart-panel">
    <div class="panel-label">Receita</div>
    <div class="panel-title">Receita por Modelo</div>
    <div class="chart-wrap"><canvas id="chart-revenue"></canvas></div>
  </div>
</div>

<!-- Insights -->
<div style="background:var(--dark);padding:32px 36px 20px;border-top:1px solid var(--border-subtle);">
  <div class="panel-label">Inteligência de Mercado</div>
  <div class="panel-title">Modelos Mais Populares por Cidade</div>
</div>
<div class="insights-grid" id="insights-container"></div>

<!-- Table -->
<div class="table-section">
  <div class="table-header">
    <div>
      <div class="panel-label">Registros</div>
      <div class="panel-title" style="margin-bottom:0">Transações Filtradas</div>
    </div>
  </div>
  <table>
    <thead>
      <tr>
        <th>Modelo</th><th>Ano</th><th>Cidade</th><th>Estado</th>
        <th>Pagamento</th><th>Preço</th><th>Status</th>
      </tr>
    </thead>
    <tbody id="table-body"></tbody>
  </table>
</div>

<footer>
  <div>© 2024 <span>Porsche</span> — Confidencial</div>
  <div>Sales Intelligence Platform &nbsp;·&nbsp; <span>v2.0</span></div>
</footer>

<script>
const ALL_DATA = {records_json};

const GOLD = '#c9a84c';
const GOLD2 = 'rgba(201,168,76,0.55)';
const WHITE = 'rgba(245,240,232,0.75)';
const palette = ['#c9a84c','#e2c47a','#a07830','#f0dda0','#7a5c20','#d4b060','#8a6828','#b89040'];

Chart.defaults.color = 'rgba(245,240,232,0.5)';
Chart.defaults.font.family = "'DM Sans', sans-serif";

let charts = {{}};

function fmt(n) {{
  if(n >= 1000000) return '$' + (n/1000000).toFixed(1) + 'M';
  if(n >= 1000) return '$' + Math.round(n/1000) + 'K';
  return '$' + n;
}}

function badgeClass(status) {{
  const s = (status||'').toLowerCase();
  if(s.includes('delivered')) return 'badge-delivered';
  if(s.includes('transit')) return 'badge-transit';
  return 'badge-pending';
}}

function getFiltered() {{
  const m = document.getElementById('f-model').value;
  const y = document.getElementById('f-year').value;
  const c = document.getElementById('f-city').value;
  const p = document.getElementById('f-pay').value;
  return ALL_DATA.filter(r =>
    (!m || r.model === m) &&
    (!y || String(r.model_year) === y) &&
    (!c || r.city === c) &&
    (!p || r.pay_method === p)
  );
}}

function count(arr, key) {{
  return arr.reduce((acc,r) => {{ acc[r[key]] = (acc[r[key]]||0)+1; return acc; }}, {{}});
}}

function sum(arr, key) {{
  return arr.reduce((acc,r) => {{ acc[r[key]] = (acc[r[key]]||0) + (r.sale_price||0); return acc; }}, {{}});
}}

function destroyChart(id) {{
  if(charts[id]) {{ charts[id].destroy(); delete charts[id]; }}
}}

function render() {{
  const data = getFiltered();

  // KPIs
  const total = data.length;
  const revenue = data.reduce((s,r) => s + (r.sale_price||0), 0);
  const avg = total ? Math.round(revenue/total) : 0;
  const cities = new Set(data.map(r=>r.city)).size;
  document.getElementById('kpi-total').textContent = total.toLocaleString('pt-BR');
  document.getElementById('kpi-revenue').textContent = fmt(revenue);
  document.getElementById('kpi-avg').textContent = fmt(avg);
  document.getElementById('kpi-cities').textContent = cities;
  document.getElementById('count-label').innerHTML = `<b>${{total}}</b> registros encontrados`;

  // Chart: models by city
  const cityModel = {{}};
  data.forEach(r => {{
    if(!cityModel[r.city]) cityModel[r.city] = {{}};
    cityModel[r.city][r.model] = (cityModel[r.city][r.model]||0)+1;
  }});
  const cityLabels = Object.keys(cityModel);
  const allModels = [...new Set(data.map(r=>r.model))];
  const cityDatasets = allModels.map((m,i) => ({{
    label: m, backgroundColor: palette[i % palette.length],
    data: cityLabels.map(c => cityModel[c][m]||0),
    borderRadius: 2, borderSkipped: false
  }}));
  destroyChart('city');
  charts['city'] = new Chart(document.getElementById('chart-city'), {{
    type: 'bar',
    data: {{ labels: cityLabels, datasets: cityDatasets }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{ legend: {{ labels: {{ boxWidth: 10, font: {{ size:10 }} }} }} }},
      scales: {{
        x: {{ stacked: true, grid: {{ color: 'rgba(255,255,255,0.04)' }}, ticks: {{ font: {{ size:10 }} }} }},
        y: {{ stacked: true, grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ stepSize:1, font: {{ size:10 }} }} }}
      }}
    }}
  }});

  // Chart: by year
  const yearCnt = count(data, 'model_year');
  const yrLabels = Object.keys(yearCnt).sort();
  destroyChart('year');
  charts['year'] = new Chart(document.getElementById('chart-year'), {{
    type: 'bar',
    data: {{
      labels: yrLabels,
      datasets: [{{ label: 'Unidades', data: yrLabels.map(y=>yearCnt[y]),
        backgroundColor: palette, borderRadius: 3 }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{ legend: {{ display: false }} }},
      scales: {{
        x: {{ grid: {{ color: 'rgba(255,255,255,0.04)' }} }},
        y: {{ grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ stepSize:1 }} }}
      }}
    }}
  }});

  // Chart: pay method
  const payCnt = count(data, 'pay_method');
  destroyChart('pay');
  charts['pay'] = new Chart(document.getElementById('chart-pay'), {{
    type: 'doughnut',
    data: {{ labels: Object.keys(payCnt), datasets: [{{ data: Object.values(payCnt), backgroundColor: palette, borderWidth: 0, hoverOffset: 8 }}] }},
    options: {{
      responsive: true, maintainAspectRatio: false, cutout: '68%',
      plugins: {{ legend: {{ position: 'right', labels: {{ boxWidth: 10, font: {{ size:10 }} }} }} }}
    }}
  }});

  // Chart: revenue by model
  const revModel = sum(data, 'model');
  const revKeys = Object.keys(revModel).sort((a,b)=>revModel[b]-revModel[a]);
  destroyChart('revenue');
  charts['revenue'] = new Chart(document.getElementById('chart-revenue'), {{
    type: 'bar', indexAxis: 'y',
    data: {{
      labels: revKeys,
      datasets: [{{ label: 'Receita (USD)', data: revKeys.map(k=>revModel[k]),
        backgroundColor: palette, borderRadius: 3 }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{ legend: {{ display: false }} }},
      scales: {{
        x: {{ grid: {{ color: 'rgba(255,255,255,0.06)' }}, ticks: {{ callback: v => fmt(v), font: {{ size:10 }} }} }},
        y: {{ grid: {{ display: false }} }}
      }}
    }}
  }});

  // Insights
  const container = document.getElementById('insights-container');
  container.innerHTML = '';
  const byCityModel = {{}};
  data.forEach(r => {{
    const key = r.city;
    if(!byCityModel[key]) byCityModel[key] = {{}};
    byCityModel[key][r.model] = (byCityModel[key][r.model]||0)+1;
  }});
  const topEntries = Object.entries(byCityModel)
    .map(([city, models]) => {{
      const top = Object.entries(models).sort((a,b)=>b[1]-a[1])[0];
      return {{ city, model: top[0], qty: top[1], total: Object.values(models).reduce((s,v)=>s+v,0) }};
    }})
    .sort((a,b) => b.qty - a.qty)
    .slice(0, 6);

  topEntries.forEach((e, i) => {{
    const div = document.createElement('div');
    div.className = 'insight-card';
    const avgPrice = data.filter(r=>r.city===e.city&&r.model===e.model).reduce((s,r)=>s+(r.sale_price||0),0) / e.qty;
    div.innerHTML = `
      <div class="insight-rank">0${{i+1}}</div>
      <div class="insight-model">${{e.model}}</div>
      <div class="insight-city">${{e.city}}</div>
      <div class="insight-stat">
        Vendas nesta cidade: <span>${{e.qty}}</span><br>
        Total de modelos: <span>${{e.total}}</span><br>
        Ticket médio: <span>${{fmt(Math.round(avgPrice))}}</span>
      </div>`;
    container.appendChild(div);
  }});
  if(topEntries.length === 0) container.innerHTML = '<div style="padding:32px;color:var(--white-dim);font-size:13px;grid-column:1/-1">Nenhum dado encontrado para os filtros selecionados.</div>';

  // Table
  const tbody = document.getElementById('table-body');
  tbody.innerHTML = '';
  const display = data.slice(0, 50);
  display.forEach(r => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${{r.model||'—'}}</td>
      <td>${{r.model_year||'—'}}</td>
      <td>${{r.city||'—'}}</td>
      <td>${{r.state||'—'}}</td>
      <td>${{r.pay_method||'—'}}</td>
      <td style="color:var(--gold)">${{r.sale_price ? fmt(r.sale_price) : '—'}}</td>
      <td><span class="badge ${{badgeClass(r.delivery_status)}}">${{r.delivery_status||'—'}}</span></td>`;
    tbody.appendChild(tr);
  }});
}}

function resetFilters() {{
  ['f-model','f-year','f-city','f-pay'].forEach(id => document.getElementById(id).value = '');
  render();
}}

['f-model','f-year','f-city','f-pay'].forEach(id =>
  document.getElementById(id).addEventListener('change', render)
);

render();
</script>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Dashboard gerado: {output_path}")

if __name__ == '__main__':
    xlsx = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/porsche_database_v2.xlsx'
    out  = sys.argv[2] if len(sys.argv) > 2 else '/mnt/user-data/outputs/porsche_dashboard.html'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df = load_data(xlsx)
    build_dashboard(df, out)
