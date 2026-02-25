import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="BMW · Used Car Analytics",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/600px-BMW.svg.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BMW DESIGN SYSTEM — CSS
#  Inspired by BMW iDrive / BMW.com dark theme
#  Palette: BMW Blue #1B69D1, Charcoal #1A1A1A, Slate #262626
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── BMW DESIGN TOKENS ────────────────────────── */
:root {
    --bmw-blue:      #1B69D1;
    --bmw-blue-light:#4A90E2;
    --bmw-blue-glow: rgba(27,105,209,0.25);
    --bmw-black:     #0D0D0D;
    --bmw-charcoal:  #1A1A1A;
    --bmw-card:      #1F1F1F;
    --bmw-surface:   #262626;
    --bmw-border:    #333333;
    --bmw-white:     #FFFFFF;
    --bmw-silver:    #E8E8E8;
    --bmw-grey:      #999999;
    --bmw-text:      #B8B8B8;
    --bmw-cyan:      #00B4D8;
    --bmw-green:     #2EC4B6;
    --bmw-amber:     #FFB703;
    --bmw-red:       #E63946;
    --radius-sm:     8px;
    --radius-md:     12px;
    --radius-lg:     16px;
    --transition:    all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ── APP BACKGROUND ─────────────────────────────── */
.stApp {
    background: var(--bmw-black);
    color: var(--bmw-text);
}

/* ── SIDEBAR — BMW iDrive style ─────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bmw-charcoal);
    border-right: 1px solid var(--bmw-border);
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label {
    color: var(--bmw-grey) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em;
}
section[data-testid="stSidebar"] hr {
    border-color: var(--bmw-border);
    margin: 0.8rem 0;
}

/* ── MAIN CONTENT ───────────────────────────────── */
.block-container {
    padding: 1.2rem 1.8rem 2rem !important;
    max-width: 1480px;
}

/* ── BMW HEADER BAR ─────────────────────────────── */
.bmw-header {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    padding: 1.4rem 2rem;
    margin-bottom: 1.6rem;
    background: linear-gradient(135deg, var(--bmw-charcoal) 0%, #111111 100%);
    border: 1px solid var(--bmw-border);
    border-left: 4px solid var(--bmw-blue);
    border-radius: var(--radius-lg);
    position: relative;
    overflow: hidden;
}
.bmw-header::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 300px; height: 100%;
    background: radial-gradient(circle at 100% 50%, var(--bmw-blue-glow), transparent 70%);
    pointer-events: none;
}
.bmw-header-logo { width: 52px; height: 52px; flex-shrink: 0; }
.bmw-header-text h1 {
    color: var(--bmw-white);
    font-size: 1.45rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
}
.bmw-header-text p {
    color: var(--bmw-grey);
    font-size: 0.82rem;
    margin: 0.15rem 0 0 0;
    font-weight: 400;
}

/* ── KPI CARDS ──────────────────────────────────── */
.kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.9rem; margin-bottom: 1.5rem; }
@media (max-width: 1024px) { .kpi-row { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 640px)  { .kpi-row { grid-template-columns: repeat(2, 1fr); } }

.kpi {
    background: var(--bmw-card);
    border: 1px solid var(--bmw-border);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: var(--transition);
}
.kpi:hover {
    border-color: var(--bmw-blue);
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.4);
}
.kpi-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; }
.kpi-badge {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem;
}
.kpi-change { font-size: 0.68rem; font-weight: 600; padding: 2px 7px; border-radius: 20px; }
.kpi-value { color: var(--bmw-white); font-size: 1.55rem; font-weight: 700; line-height: 1; margin-bottom: 0.2rem; }
.kpi-label { color: var(--bmw-grey); font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; }
.kpi-accent { position: absolute; bottom: 0; left: 0; width: 100%; height: 2px; }

/* accent variants */
.kpi-accent-blue   { background: var(--bmw-blue); }
.kpi-accent-cyan   { background: var(--bmw-cyan); }
.kpi-accent-green  { background: var(--bmw-green); }
.kpi-accent-amber  { background: var(--bmw-amber); }
.kpi-accent-red    { background: var(--bmw-red); }
.badge-blue  { background: rgba(27,105,209,0.15); color: var(--bmw-blue); }
.badge-cyan  { background: rgba(0,180,216,0.12); color: var(--bmw-cyan); }
.badge-green { background: rgba(46,196,182,0.12); color: var(--bmw-green); }
.badge-amber { background: rgba(255,183,3,0.12); color: var(--bmw-amber); }
.badge-red   { background: rgba(230,57,70,0.12); color: var(--bmw-red); }

/* ── CHART PANEL ────────────────────────────────── */
.panel {
    background: var(--bmw-card);
    border: 1px solid var(--bmw-border);
    border-radius: var(--radius-md);
    padding: 1.3rem 1.5rem 1rem;
    margin-bottom: 1rem;
    transition: var(--transition);
}
.panel:hover {
    border-color: #444;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.panel-header { display: flex; align-items: baseline; gap: 0.6rem; margin-bottom: 0.1rem; }
.panel-title {
    color: var(--bmw-silver);
    font-size: 0.92rem;
    font-weight: 600;
    margin: 0;
    letter-spacing: -0.01em;
}
.panel-tag {
    font-size: 0.62rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 2px 8px;
    border-radius: 20px;
    background: rgba(27,105,209,0.12);
    color: var(--bmw-blue-light);
}
.panel-subtitle {
    color: #666;
    font-size: 0.72rem;
    margin: 0 0 0.9rem 0;
    font-weight: 400;
}

/* ── SECTION DIVIDER ────────────────────────────── */
.section-label {
    display: flex; align-items: center; gap: 0.6rem;
    margin: 1.6rem 0 1rem;
}
.section-label span {
    color: var(--bmw-grey);
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    white-space: nowrap;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--bmw-border);
}

/* ── TAB OVERRIDES ──────────────────────────────── */
button[data-baseweb="tab"] {
    color: var(--bmw-grey) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.01em;
    padding: 0.6rem 1.2rem !important;
    border-radius: 8px 8px 0 0 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--bmw-white) !important;
    background: var(--bmw-card) !important;
    border-bottom: 2px solid var(--bmw-blue) !important;
}
div[data-baseweb="tab-list"] {
    gap: 0.3rem;
    border-bottom: 1px solid var(--bmw-border);
}

/* ── STREAMLIT OVERRIDES ────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDataFrame { border-radius: var(--radius-md); overflow: hidden; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.2rem; }
.stDownloadButton button {
    background: var(--bmw-blue) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 1.5rem !important;
    transition: var(--transition);
}
.stDownloadButton button:hover {
    background: var(--bmw-blue-light) !important;
    box-shadow: 0 4px 16px var(--bmw-blue-glow);
}

/* ── SCROLLBAR ──────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bmw-charcoal); }
::-webkit-scrollbar-thumb { background: #444; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--bmw-blue); }
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
#  BMW PLOTLY THEME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BMW_LAYOUT = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, -apple-system, sans-serif", color="#B8B8B8", size=11),
    margin=dict(l=16, r=16, t=28, b=16),
    hoverlabel=dict(
        bgcolor="#262626", font_size=12, font_family="Inter",
        bordercolor="#444",
    ),
)

def apply_bmw(fig):
    """Apply BMW grid styling to a figure after layout is set."""
    fig.update_xaxes(gridcolor="#2A2A2A", zerolinecolor="#2A2A2A")
    fig.update_yaxes(gridcolor="#2A2A2A", zerolinecolor="#2A2A2A")
    return fig

BMW_COLORS = ["#1B69D1", "#00B4D8", "#2EC4B6", "#FFB703", "#E63946", "#A78BFA", "#F472B6"]
BMW_SEQ = ["#0D0D0D", "#1B69D1", "#4A90E2", "#00B4D8"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    # BMW Logo + branding
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0 0.4rem">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/600px-BMW.svg.png"
             width="64" style="filter:drop-shadow(0 0 16px rgba(27,105,209,.4))"/>
        <p style="color:#FFF; font-weight:700; font-size:1.1rem; margin:0.7rem 0 0; letter-spacing:0.08em">BMW</p>
        <p style="color:#666; font-size:0.65rem; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; margin:0">
            Used Car Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<p style="color:#999;font-size:0.7rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem">FILTERS</p>', unsafe_allow_html=True)

    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    year_range = st.slider("Model Year", min_year, max_year, (min_year, max_year))

    fuel_options = sorted(df["fuelType"].unique().tolist())
    selected_fuels = st.multiselect("Fuel Type", fuel_options, default=fuel_options)

    trans_options = sorted(df["transmission"].unique().tolist())
    selected_trans = st.multiselect("Transmission", trans_options, default=trans_options)

    min_price, max_price = int(df["price"].min()), int(df["price"].max())
    price_range = st.slider("Price (£)", min_price, max_price, (min_price, max_price), step=500)

    model_options = sorted(df["model"].unique().tolist())
    selected_models = st.multiselect("Model", model_options, default=[])

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:0.3rem 0">
        <p style="color:#444; font-size:0.62rem; letter-spacing:0.08em">
            v3.0 · STREAMLIT + PLOTLY<br>© BMW Analytics Platform
        </p>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FILTERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
mask = (
    df["year"].between(*year_range)
    & df["fuelType"].isin(selected_fuels)
    & df["transmission"].isin(selected_trans)
    & df["price"].between(*price_range)
)
if selected_models:
    mask &= df["model"].isin(selected_models)
filtered = df[mask]
n = len(filtered)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HEADER BAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"""
<div class="bmw-header">
    <img class="bmw-header-logo"
         src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/600px-BMW.svg.png" />
    <div class="bmw-header-text">
        <h1>Used Car Analytics</h1>
        <p>Analysing <strong style="color:#FFF">{n:,}</strong> filtered listings
           from <strong style="color:#FFF">{len(df):,}</strong> total vehicles in the dataset</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KPI CARDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
avg_price   = filtered["price"].mean()      if n else 0
avg_mileage = filtered["mileage"].mean()    if n else 0
avg_mpg     = filtered["mpg"].mean()        if n else 0
avg_engine  = filtered["engineSize"].mean() if n else 0
median_tax  = filtered["tax"].median()      if n else 0

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi">
        <div class="kpi-top">
            <div class="kpi-badge badge-blue">💷</div>
        </div>
        <div class="kpi-value">£{avg_price:,.0f}</div>
        <div class="kpi-label">Average Price</div>
        <div class="kpi-accent kpi-accent-blue"></div>
    </div>
    <div class="kpi">
        <div class="kpi-top">
            <div class="kpi-badge badge-cyan">🛣️</div>
        </div>
        <div class="kpi-value">{avg_mileage:,.0f}</div>
        <div class="kpi-label">Average Mileage</div>
        <div class="kpi-accent kpi-accent-cyan"></div>
    </div>
    <div class="kpi">
        <div class="kpi-top">
            <div class="kpi-badge badge-green">⛽</div>
        </div>
        <div class="kpi-value">{avg_mpg:.1f}</div>
        <div class="kpi-label">Average MPG</div>
        <div class="kpi-accent kpi-accent-green"></div>
    </div>
    <div class="kpi">
        <div class="kpi-top">
            <div class="kpi-badge badge-amber">🔧</div>
        </div>
        <div class="kpi-value">{avg_engine:.1f}L</div>
        <div class="kpi-label">Avg Engine Size</div>
        <div class="kpi-accent kpi-accent-amber"></div>
    </div>
    <div class="kpi">
        <div class="kpi-top">
            <div class="kpi-badge badge-red">📋</div>
        </div>
        <div class="kpi-value">£{median_tax:.0f}</div>
        <div class="kpi-label">Median Road Tax</div>
        <div class="kpi-accent kpi-accent-red"></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TABS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview", "Price Analysis", "Inventory", "Data"
])


# ═══════════════════════ TAB 1 — OVERVIEW ════════════════════
with tab1:

    # ── Row 1: Fuel Bar + Transmission Donut ──
    c1, c2 = st.columns([1.15, 1])

    with c1:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Fuel Type Breakdown</p><span class="panel-tag">Bar</span></div>
            <p class="panel-subtitle">Number of listings per fuel category</p>""", unsafe_allow_html=True)
        fc = filtered["fuelType"].value_counts().reset_index()
        fc.columns = ["Fuel", "Count"]
        fig = px.bar(fc, x="Fuel", y="Count", color="Fuel", text_auto=True,
                     color_discrete_sequence=BMW_COLORS)
        fig.update_layout(**BMW_LAYOUT, showlegend=False, height=360)
        apply_bmw(fig)
        fig.update_traces(textposition="outside", marker_line_width=0,
                          marker_cornerradius=4)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Transmission Split</p><span class="panel-tag">Donut</span></div>
            <p class="panel-subtitle">Proportion by gearbox type</p>""", unsafe_allow_html=True)
        tc = filtered["transmission"].value_counts().reset_index()
        tc.columns = ["Trans", "Count"]
        fig = px.pie(tc, names="Trans", values="Count", hole=0.58,
                     color_discrete_sequence=BMW_COLORS)
        fig.update_layout(**BMW_LAYOUT, height=360, showlegend=True,
                          legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                                      font=dict(size=11)))
        apply_bmw(fig)
        fig.update_traces(textinfo="percent+label", textfont_size=11,
                          pull=[0.015]*len(tc), marker_line_width=0)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 2: Price Trend — Full Width ──
    st.markdown("""<div class="panel">
        <div class="panel-header"><p class="panel-title">Average Price Trajectory</p><span class="panel-tag">Trend</span></div>
        <p class="panel-subtitle">Year-over-year average price with volume overlay</p>""", unsafe_allow_html=True)

    agg = filtered.groupby("year").agg(avg=("price","mean"), cnt=("price","count")).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=agg["year"], y=agg["cnt"], name="Volume",
        marker_color="rgba(27,105,209,0.15)", marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Listings: %{y:,}<extra></extra>",
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=agg["year"], y=agg["avg"], name="Avg Price", mode="lines+markers",
        line=dict(color="#1B69D1", width=2.5, shape="spline"),
        marker=dict(size=7, color="#1B69D1", line=dict(width=2, color="#0D0D0D")),
        fill="tozeroy", fillcolor="rgba(27,105,209,0.06)",
        hovertemplate="<b>%{x}</b><br>Avg: £%{y:,.0f}<extra></extra>",
    ), secondary_y=False)
    fig.update_layout(**BMW_LAYOUT, height=370, showlegend=True,
                      legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center", font=dict(size=11)))
    fig.update_xaxes(dtick=1, title="Year", gridcolor="#2A2A2A")
    fig.update_yaxes(title="Avg Price (£)", tickprefix="£", separatethousands=True,
                     secondary_y=False, gridcolor="#2A2A2A")
    fig.update_yaxes(title="Listings", showgrid=False, secondary_y=True)
    apply_bmw(fig)
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3: MPG by Fuel + Engine Distribution ──
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">MPG by Fuel Type</p><span class="panel-tag">Box</span></div>
            <p class="panel-subtitle">Spread of fuel efficiency per category</p>""", unsafe_allow_html=True)
        fig = px.box(filtered, x="fuelType", y="mpg", color="fuelType",
                     color_discrete_sequence=BMW_COLORS)
        fig.update_layout(**BMW_LAYOUT, height=360, showlegend=False,
                          xaxis_title="Fuel Type", yaxis_title="MPG")
        apply_bmw(fig)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Engine Size Mix</p><span class="panel-tag">Donut</span></div>
            <p class="panel-subtitle">Share of each engine displacement</p>""", unsafe_allow_html=True)
        ec = filtered["engineSize"].value_counts().sort_index().reset_index()
        ec.columns = ["Size", "Count"]
        ec["Label"] = ec["Size"].astype(str) + "L"
        fig = px.pie(ec, names="Label", values="Count", hole=0.55,
                     color_discrete_sequence=BMW_COLORS)
        fig.update_layout(**BMW_LAYOUT, height=360,
                          legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(size=10)))
        apply_bmw(fig)
        fig.update_traces(textinfo="percent+label", textfont_size=10)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════ TAB 2 — PRICING ═════════════════════
with tab2:

    c5, c6 = st.columns(2)
    with c5:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Price vs Mileage</p><span class="panel-tag">Scatter</span></div>
            <p class="panel-subtitle">Each point = 1 listing · bubble size = engine capacity</p>""", unsafe_allow_html=True)
        fig = px.scatter(filtered, x="mileage", y="price", color="fuelType",
                         size="engineSize", opacity=0.6,
                         hover_data=["model","year","transmission"],
                         color_discrete_sequence=BMW_COLORS)
        fig.update_layout(**BMW_LAYOUT, height=440, xaxis_title="Mileage",
                          yaxis_title="Price (£)",
                          legend=dict(orientation="h", y=-0.16, x=0.5, xanchor="center", font=dict(size=10)))
        apply_bmw(fig)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Mileage Distribution</p><span class="panel-tag">Histogram</span></div>
            <p class="panel-subtitle">Frequency with marginal box plot</p>""", unsafe_allow_html=True)
        fig = px.histogram(filtered, x="mileage", nbins=40, marginal="box",
                           color_discrete_sequence=["#1B69D1"])
        fig.update_layout(**BMW_LAYOUT, height=440, xaxis_title="Mileage",
                          yaxis_title="Frequency", bargap=0.04)
        apply_bmw(fig)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # Violin
    st.markdown("""<div class="panel">
        <div class="panel-header"><p class="panel-title">Price Distribution by Fuel</p><span class="panel-tag">Violin</span></div>
        <p class="panel-subtitle">Density and quartile breakdown per fuel type</p>""", unsafe_allow_html=True)
    fig = px.violin(filtered, x="fuelType", y="price", color="fuelType",
                    box=True, points=False, color_discrete_sequence=BMW_COLORS)
    fig.update_layout(**BMW_LAYOUT, height=400, showlegend=False,
                      xaxis_title="Fuel Type", yaxis_title="Price (£)")
    apply_bmw(fig)
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # Heatmap
    st.markdown("""<div class="panel">
        <div class="panel-header"><p class="panel-title">Year × Fuel — Price Matrix</p><span class="panel-tag">Heatmap</span></div>
        <p class="panel-subtitle">Identify value pockets across year and fuel type</p>""", unsafe_allow_html=True)
    hd = filtered.pivot_table(values="price", index="fuelType", columns="year", aggfunc="mean")
    fig = px.imshow(hd, text_auto=",.0f", color_continuous_scale=["#0D0D0D","#1B69D1","#00B4D8"],
                    aspect="auto")
    fig.update_layout(**BMW_LAYOUT, height=320, xaxis_title="Year", yaxis_title="Fuel",
                      coloraxis_colorbar=dict(title="£", tickprefix="£"))
    apply_bmw(fig)
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════ TAB 3 — INVENTORY ═══════════════════
with tab3:

    c7, c8 = st.columns([3, 2])
    with c7:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Top 12 Models</p><span class="panel-tag">Ranking</span></div>
            <p class="panel-subtitle">Most listed models in current selection</p>""", unsafe_allow_html=True)
        top = filtered["model"].value_counts().head(12).reset_index()
        top.columns = ["Model", "Count"]
        fig = px.bar(top, x="Count", y="Model", orientation="h", text_auto=True,
                     color="Count", color_continuous_scale=BMW_SEQ)
        fig.update_layout(**BMW_LAYOUT, height=470, coloraxis_showscale=False)
        fig.update_yaxes(autorange="reversed")
        apply_bmw(fig)
        fig.update_traces(marker_line_width=0, textposition="outside",
                          marker_cornerradius=3)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with c8:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Avg Price by Model</p><span class="panel-tag">Ranking</span></div>
            <p class="panel-subtitle">Top 10 most expensive models (avg)</p>""", unsafe_allow_html=True)
        price_rank = (filtered.groupby("model")["price"].mean()
                      .sort_values(ascending=False).head(10).reset_index())
        price_rank.columns = ["Model", "Avg Price"]
        fig = px.bar(price_rank, x="Avg Price", y="Model", orientation="h",
                     text_auto=",.0f",
                     color="Avg Price", color_continuous_scale=["#0D0D0D","#FFB703","#E63946"])
        fig.update_layout(**BMW_LAYOUT, height=470, coloraxis_showscale=False)
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(title="Avg Price (£)", tickprefix="£")
        apply_bmw(fig)
        fig.update_traces(marker_line_width=0, textposition="outside",
                          texttemplate="£%{x:,.0f}", marker_cornerradius=3)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # Treemap
    st.markdown("""<div class="panel">
        <div class="panel-header"><p class="panel-title">Model × Transmission Treemap</p><span class="panel-tag">Proportional</span></div>
        <p class="panel-subtitle">Larger blocks = more listings in that segment</p>""", unsafe_allow_html=True)
    tree_df = (filtered.groupby(["model","transmission"]).size()
               .reset_index(name="count").sort_values("count", ascending=False).head(40))
    fig = px.treemap(tree_df, path=["model","transmission"], values="count",
                     color="count", color_continuous_scale=BMW_SEQ)
    fig.update_layout(**BMW_LAYOUT, height=450, coloraxis_showscale=False)
    apply_bmw(fig)
    fig.update_traces(marker_line_width=0.5, marker_line_color="#333", textfont_size=12)
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # Sunburst + Bubble
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Inventory Sunburst</p><span class="panel-tag">Hierarchy</span></div>
            <p class="panel-subtitle">Fuel → Transmission → Engine Size drill-down</p>""", unsafe_allow_html=True)
        sun = (filtered.assign(eng=filtered["engineSize"].astype(str)+"L")
               .groupby(["fuelType","transmission","eng"]).size().reset_index(name="count"))
        fig = px.sunburst(sun, path=["fuelType","transmission","eng"], values="count",
                          color_discrete_sequence=BMW_COLORS)
        fig.update_layout(**BMW_LAYOUT, height=430)
        apply_bmw(fig)
        fig.update_traces(textfont_size=11)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        st.markdown("""<div class="panel">
            <div class="panel-header"><p class="panel-title">Efficiency Matrix</p><span class="panel-tag">Bubble</span></div>
            <p class="panel-subtitle">MPG vs Tax — bubble = listing volume</p>""", unsafe_allow_html=True)
        eff = (filtered.groupby("fuelType")
               .agg(mpg=("mpg","mean"), tax=("tax","mean"),
                    count=("price","count"), price=("price","mean")).reset_index())
        fig = px.scatter(eff, x="mpg", y="tax", size="count", color="fuelType",
                         hover_data=["price"], color_discrete_sequence=BMW_COLORS,
                         size_max=55)
        fig.update_layout(**BMW_LAYOUT, height=430,
                          xaxis_title="Avg MPG", yaxis_title="Avg Tax (£)")
        apply_bmw(fig)
        st.plotly_chart(fig, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════ TAB 4 — DATA EXPLORER ═══════════════
with tab4:
    st.markdown(f"""<div class="panel">
        <div class="panel-header"><p class="panel-title">Filtered Dataset</p><span class="panel-tag">{n:,} rows</span></div>
        <p class="panel-subtitle">Full data view — sortable columns · use sidebar to refine</p>""", unsafe_allow_html=True)

    cols = ["model","year","price","transmission","mileage","fuelType","tax","mpg","engineSize"]
    st.dataframe(
        filtered[cols].sort_values("price", ascending=False).reset_index(drop=True),
        width="stretch", height=520,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Download
    csv_out = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇  Export Filtered CSV", csv_out, "bmw_filtered.csv", "text/csv")

    # Stats
    st.markdown("""<div class="panel">
        <div class="panel-header"><p class="panel-title">Descriptive Statistics</p><span class="panel-tag">Summary</span></div>
        <p class="panel-subtitle">Key statistical measures for all numeric fields</p>""", unsafe_allow_html=True)
    st.dataframe(filtered.describe().T.style.format("{:,.1f}"), width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:0.5rem 0 1rem">
    <p style="color:#444; font-size:0.68rem; letter-spacing:0.08em; margin:0">
        BMW USED CAR INTELLIGENCE · ANALYTICS DASHBOARD · V3.0
    </p>
    <p style="color:#333; font-size:0.6rem; margin:0.2rem 0 0">
        Built with Streamlit & Plotly · Data for demonstration purposes only
    </p>
</div>
""", unsafe_allow_html=True)
