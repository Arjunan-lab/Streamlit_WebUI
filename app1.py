import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="BMW Analytics | Used Car Intelligence",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GLOBAL STYLE — glassmorphism + BMW brand palette
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── root variables ────────────────────────────── */
:root {
    --bmw-blue:    #1C69D4;
    --bmw-dark:    #0A0E17;
    --card-bg:     rgba(17, 25, 40, 0.75);
    --card-border: rgba(255, 255, 255, 0.08);
    --text-primary:#E2E8F0;
    --text-muted:  #94A3B8;
    --accent-cyan: #22D3EE;
    --accent-green:#34D399;
    --accent-amber:#FBBF24;
    --accent-rose: #FB7185;
    --glass:       rgba(255,255,255,0.03);
}

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif !important;
}

/* ── main area ─────────────────────────────────── */
.stApp {
    background: radial-gradient(ellipse at 20% 0%, #0d1b2a 0%, #0A0E17 70%);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(195deg, #0f172a 0%, #0A0E17 100%);
    border-right: 1px solid var(--card-border);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label {
    color: var(--text-muted) !important;
    font-size: 0.85rem;
}

.block-container { padding: 1.5rem 2rem 2rem !important; max-width: 1440px; }

/* ── header banner ─────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #1C69D4 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(28,105,212,0.3);
    box-shadow: 0 4px 30px rgba(28,105,212,0.15);
}
.hero-banner h1 {
    color: #fff; font-weight: 700; font-size: 1.8rem; margin: 0 0 .3rem 0;
}
.hero-banner p {
    color: rgba(255,255,255,0.7); font-size: .95rem; margin: 0;
}

/* ── glass card wrapper ────────────────────────── */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: transform .2s, box-shadow .2s;
}
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

/* ── KPI chips ─────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.5rem; }
@media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2,1fr); } }
.kpi-chip {
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: left;
    position: relative;
    overflow: hidden;
    transition: transform .2s;
}
.kpi-chip:hover { transform: translateY(-3px); }
.kpi-chip .kpi-icon {
    width: 38px; height: 38px; border-radius: 10px; display: flex;
    align-items: center; justify-content: center; font-size: 1.1rem;
    margin-bottom: .6rem;
}
.kpi-chip .kpi-value { color: #fff; font-size: 1.65rem; font-weight: 700; line-height: 1.1; }
.kpi-chip .kpi-label { color: var(--text-muted); font-size: .78rem; font-weight: 500;
    text-transform: uppercase; letter-spacing: .6px; margin-top: .25rem; }
.kpi-chip .kpi-bar {
    position: absolute; bottom: 0; left: 0; height: 3px; border-radius: 0 0 14px 14px;
}

/* color accents per chip */
.kpi-blue  .kpi-icon { background: rgba(28,105,212,0.2); color: var(--bmw-blue); }
.kpi-blue  .kpi-bar  { background: var(--bmw-blue); width: 100%; }
.kpi-cyan  .kpi-icon { background: rgba(34,211,238,0.15); color: var(--accent-cyan); }
.kpi-cyan  .kpi-bar  { background: var(--accent-cyan); width: 100%; }
.kpi-green .kpi-icon { background: rgba(52,211,153,0.15); color: var(--accent-green); }
.kpi-green .kpi-bar  { background: var(--accent-green); width: 100%; }
.kpi-amber .kpi-icon { background: rgba(251,191,36,0.15); color: var(--accent-amber); }
.kpi-amber .kpi-bar  { background: var(--accent-amber); width: 100%; }

/* ── chart titles inside glass ─────────────────── */
.chart-title {
    color: var(--text-primary); font-size: 1rem; font-weight: 600;
    margin: 0 0 .15rem 0; letter-spacing: -.01em;
}
.chart-subtitle {
    color: var(--text-muted); font-size: .78rem; margin: 0 0 .8rem 0;
}

/* ── tab overrides ─────────────────────────────── */
button[data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    font-size: .88rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent-cyan) !important;
    border-bottom-color: var(--accent-cyan) !important;
}

/* ── hide default streamlit branding ───────────── */
#MainMenu, footer, header { visibility: hidden; }

/* ── dataframe styling ─────────────────────────── */
.stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data
def load_data():
    df = pd.read_csv("bmw.csv")
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    return df

df = load_data()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SHARED CHART THEME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHART_LAYOUT = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#CBD5E1", size=12),
    margin=dict(l=20, r=20, t=30, b=20),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font_size=12,
        font_family="Inter",
        bordercolor="rgba(255,255,255,0.1)",
    ),
)

PALETTE = ["#1C69D4", "#22D3EE", "#34D399", "#FBBF24", "#FB7185", "#A78BFA", "#F472B6"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 .5rem">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/600px-BMW.svg.png"
             width="72" style="filter:drop-shadow(0 0 12px rgba(28,105,212,.5))"/>
        <p style="color:#fff;font-weight:600;font-size:1rem;margin:.6rem 0 0">BMW Intelligence</p>
        <p style="color:#64748b;font-size:.72rem;margin:0">Used Car Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("##### 🎯 Refine Data")

    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    year_range = st.slider("Model Year", min_year, max_year, (min_year, max_year))

    fuel_options = sorted(df["fuelType"].unique().tolist())
    selected_fuels = st.multiselect("Fuel Type", fuel_options, default=fuel_options)

    trans_options = sorted(df["transmission"].unique().tolist())
    selected_trans = st.multiselect("Transmission", trans_options, default=trans_options)

    min_price, max_price = int(df["price"].min()), int(df["price"].max())
    price_range = st.slider("Price Range (£)", min_price, max_price, (min_price, max_price), step=500)

    model_options = sorted(df["model"].unique().tolist())
    selected_models = st.multiselect("Model (leave blank for all)", model_options, default=[])

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#475569;font-size:.7rem'>v2.0 · Streamlit + Plotly</p>",
        unsafe_allow_html=True,
    )

# Apply filters
mask = (
    df["year"].between(*year_range)
    & df["fuelType"].isin(selected_fuels)
    & df["transmission"].isin(selected_trans)
    & df["price"].between(*price_range)
)
if selected_models:
    mask &= df["model"].isin(selected_models)
filtered = df[mask]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HERO BANNER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"""
<div class="hero-banner">
    <h1>🏎️ BMW Used Car Intelligence</h1>
    <p>Real-time analytics across <strong>{len(filtered):,}</strong> listings
       from a universe of <strong>{len(df):,}</strong> vehicles</p>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KPI ROW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
avg_price   = filtered["price"].mean()      if len(filtered) else 0
avg_mileage = filtered["mileage"].mean()    if len(filtered) else 0
avg_mpg     = filtered["mpg"].mean()        if len(filtered) else 0
avg_engine  = filtered["engineSize"].mean() if len(filtered) else 0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-chip kpi-blue">
        <div class="kpi-icon">💷</div>
        <div class="kpi-value">£{avg_price:,.0f}</div>
        <div class="kpi-label">Avg Price</div>
        <div class="kpi-bar"></div>
    </div>
    <div class="kpi-chip kpi-cyan">
        <div class="kpi-icon">🛣️</div>
        <div class="kpi-value">{avg_mileage:,.0f}</div>
        <div class="kpi-label">Avg Mileage</div>
        <div class="kpi-bar"></div>
    </div>
    <div class="kpi-chip kpi-green">
        <div class="kpi-icon">⛽</div>
        <div class="kpi-value">{avg_mpg:.1f}</div>
        <div class="kpi-label">Avg MPG</div>
        <div class="kpi-bar"></div>
    </div>
    <div class="kpi-chip kpi-amber">
        <div class="kpi-icon">🔧</div>
        <div class="kpi-value">{avg_engine:.1f}L</div>
        <div class="kpi-label">Avg Engine</div>
        <div class="kpi-bar"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TABBED LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_overview, tab_pricing, tab_inventory, tab_data = st.tabs(
    ["📊  Overview", "💰  Pricing Deep-Dive", "🏗️  Inventory Mix", "📋  Data Explorer"]
)

# ──────────────────────── TAB 1 — OVERVIEW ────────────────────
with tab_overview:
    r1c1, r1c2 = st.columns(2)

    # — Fuel type bar —
    with r1c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Fuel Type Breakdown</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Number of listings per fuel category</p>', unsafe_allow_html=True)
        fuel_counts = filtered["fuelType"].value_counts().reset_index()
        fuel_counts.columns = ["Fuel Type", "Count"]
        fig = px.bar(
            fuel_counts, x="Fuel Type", y="Count", color="Fuel Type",
            color_discrete_sequence=PALETTE, text_auto=True,
        )
        fig.update_layout(**CHART_LAYOUT, showlegend=False, height=370)
        fig.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # — Transmission donut —
    with r1c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Transmission Split</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Proportion by gearbox type</p>', unsafe_allow_html=True)
        trans_counts = filtered["transmission"].value_counts().reset_index()
        trans_counts.columns = ["Transmission", "Count"]
        fig = px.pie(
            trans_counts, names="Transmission", values="Count",
            hole=0.55, color_discrete_sequence=PALETTE,
        )
        fig.update_layout(**CHART_LAYOUT, height=370, showlegend=True,
                          legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"))
        fig.update_traces(textinfo="percent+label", textfont_size=12,
                          pull=[0.02] * len(trans_counts))
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # — Price trend line (full width) —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="chart-title">Average Price Trajectory</p>', unsafe_allow_html=True)
    st.markdown('<p class="chart-subtitle">Year-over-year average listing price with area fill</p>', unsafe_allow_html=True)
    avg_by_year = filtered.groupby("year").agg(
        avg_price=("price", "mean"), count=("price", "count")
    ).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=avg_by_year["year"], y=avg_by_year["avg_price"],
        mode="lines+markers",
        line=dict(color="#22D3EE", width=3, shape="spline"),
        marker=dict(size=8, color="#22D3EE", line=dict(width=2, color="#0A0E17")),
        fill="tozeroy", fillcolor="rgba(34,211,238,0.08)",
        hovertemplate="<b>%{x}</b><br>Avg Price: £%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT, height=380,
                      xaxis=dict(title="Year", dtick=1),
                      yaxis=dict(title="Average Price (£)", tickprefix="£", separatethousands=True))
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────── TAB 2 — PRICING ─────────────────────
with tab_pricing:
    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Price vs Mileage</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Each dot = one listing · sized by engine capacity</p>', unsafe_allow_html=True)
        fig = px.scatter(
            filtered, x="mileage", y="price", color="fuelType",
            size="engineSize", opacity=0.65,
            hover_data=["model", "year", "transmission"],
            color_discrete_sequence=PALETTE,
        )
        fig.update_layout(**CHART_LAYOUT, height=440,
                          xaxis_title="Mileage", yaxis_title="Price (£)",
                          legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"))
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with r2c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Mileage Distribution</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Histogram with marginal box plot</p>', unsafe_allow_html=True)
        fig = px.histogram(
            filtered, x="mileage", nbins=40,
            color_discrete_sequence=["#1C69D4"],
            marginal="box",
        )
        fig.update_layout(**CHART_LAYOUT, height=440,
                          xaxis_title="Mileage", yaxis_title="Frequency", bargap=0.03)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # — Price distribution violin (full width) —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="chart-title">Price Distribution by Fuel Type</p>', unsafe_allow_html=True)
    st.markdown('<p class="chart-subtitle">Violin plot showing density + quartiles</p>', unsafe_allow_html=True)
    fig = px.violin(
        filtered, x="fuelType", y="price", color="fuelType", box=True, points=False,
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(**CHART_LAYOUT, height=420, showlegend=False,
                      xaxis_title="Fuel Type", yaxis_title="Price (£)")
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # — Year × Fuel Price Heatmap —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="chart-title">Year × Fuel Type — Average Price Matrix</p>', unsafe_allow_html=True)
    st.markdown('<p class="chart-subtitle">Spot value pockets across year and fuel combinations</p>', unsafe_allow_html=True)
    heat_data = filtered.pivot_table(values="price", index="fuelType", columns="year", aggfunc="mean")
    fig = px.imshow(
        heat_data, text_auto=",.0f", color_continuous_scale="Blues", aspect="auto",
    )
    fig.update_layout(**CHART_LAYOUT, height=350,
                      xaxis_title="Year", yaxis_title="Fuel Type",
                      coloraxis_colorbar=dict(title="Avg £", tickprefix="£"))
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────── TAB 3 — INVENTORY ──────────────────
with tab_inventory:
    r3c1, r3c2 = st.columns([3, 2])

    with r3c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Top 12 Models by Volume</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Horizontal ranking of most-listed models</p>', unsafe_allow_html=True)
        top = filtered["model"].value_counts().head(12).reset_index()
        top.columns = ["Model", "Count"]
        fig = px.bar(
            top, x="Count", y="Model", orientation="h",
            color="Count", color_continuous_scale=["#0f172a", "#1C69D4", "#22D3EE"],
            text_auto=True,
        )
        fig.update_layout(**CHART_LAYOUT, height=480,
                          yaxis=dict(autorange="reversed"),
                          coloraxis_showscale=False)
        fig.update_traces(marker_line_width=0, textposition="outside")
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with r3c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Engine Size Split</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Distribution of engine capacities</p>', unsafe_allow_html=True)
        eng_counts = filtered["engineSize"].value_counts().sort_index().reset_index()
        eng_counts.columns = ["Engine (L)", "Count"]
        eng_counts["Engine (L)"] = eng_counts["Engine (L)"].astype(str) + "L"
        fig = px.pie(
            eng_counts, names="Engine (L)", values="Count",
            hole=0.5, color_discrete_sequence=PALETTE,
        )
        fig.update_layout(**CHART_LAYOUT, height=480,
                          legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"))
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # — Treemap (full width) —
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="chart-title">Model × Transmission Treemap</p>', unsafe_allow_html=True)
    st.markdown('<p class="chart-subtitle">Proportional area map — larger blocks = more listings</p>', unsafe_allow_html=True)
    tree_df = (
        filtered.groupby(["model", "transmission"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(40)
    )
    fig = px.treemap(
        tree_df, path=["model", "transmission"], values="count",
        color="count", color_continuous_scale=["#0f172a", "#1C69D4", "#22D3EE"],
    )
    fig.update_layout(**CHART_LAYOUT, height=460, coloraxis_showscale=False)
    fig.update_traces(
        marker_line_width=1,
        marker_line_color="rgba(255,255,255,0.06)",
        textfont_size=13,
    )
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # — Sunburst + Bubble Row —
    sb_cols = st.columns([1, 1])
    with sb_cols[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Fuel → Transmission → Engine Sunburst</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Hierarchical drill-down of inventory structure</p>', unsafe_allow_html=True)
        sun_df = (
            filtered.assign(engine_label=filtered["engineSize"].astype(str) + "L")
            .groupby(["fuelType", "transmission", "engine_label"])
            .size()
            .reset_index(name="count")
        )
        fig = px.sunburst(
            sun_df, path=["fuelType", "transmission", "engine_label"], values="count",
            color_discrete_sequence=PALETTE,
        )
        fig.update_layout(**CHART_LAYOUT, height=450)
        fig.update_traces(textfont_size=12)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with sb_cols[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">MPG vs Tax — Efficiency Matrix</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Bubble size = number of listings per fuel type</p>', unsafe_allow_html=True)
        eff_df = filtered.groupby(["fuelType"]).agg(
            mpg=("mpg", "mean"), tax=("tax", "mean"), count=("price", "count"),
            price=("price", "mean"),
        ).reset_index()
        fig = px.scatter(
            eff_df, x="mpg", y="tax", size="count", color="fuelType",
            hover_data=["price"], color_discrete_sequence=PALETTE,
            size_max=55,
        )
        fig.update_layout(**CHART_LAYOUT, height=450,
                          xaxis_title="Avg MPG", yaxis_title="Avg Tax (£)")
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────── TAB 4 — DATA EXPLORER ──────────────
with tab_data:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="chart-title">Filtered Dataset</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="chart-subtitle">Showing {len(filtered):,} records — use sidebar to refine</p>', unsafe_allow_html=True)

    col_order = ["model", "year", "price", "transmission", "mileage", "fuelType", "tax", "mpg", "engineSize"]
    st.dataframe(
        filtered[col_order].sort_values("price", ascending=False).reset_index(drop=True),
        width="stretch",
        height=520,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Download CSV
    csv_out = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download Filtered Data as CSV",
        data=csv_out,
        file_name="bmw_filtered_export.csv",
        mime="text/csv",
    )

    # Summary statistics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="chart-title">Quick Statistics</p>', unsafe_allow_html=True)
    st.markdown('<p class="chart-subtitle">Summary of numeric columns in current filter</p>', unsafe_allow_html=True)
    st.dataframe(
        filtered.describe().T.style.format("{:,.1f}"),
        width="stretch",
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("---")
st.markdown("""
<p style="text-align:center;color:#475569;font-size:.75rem">
    BMW Used Car Intelligence · Built with Streamlit & Plotly · Data for demonstration purposes
</p>
""", unsafe_allow_html=True)
