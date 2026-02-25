# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BMW Used Car Intelligence — Dash + Plotly Professional Dashboard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import dash
from dash import dcc, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ── Data ──────────────────────────────────────────────────────
CSV_PATH = os.path.join(os.path.dirname(__file__), "bmw.csv")
raw_df = pd.read_csv(CSV_PATH).dropna().drop_duplicates()

# ── Brand palette & chart theme ───────────────────────────────
BMW_BLUE   = "#1C69D4"
CYAN       = "#22D3EE"
GREEN      = "#34D399"
AMBER      = "#FBBF24"
ROSE       = "#FB7185"
PURPLE     = "#A78BFA"
PINK       = "#F472B6"
PALETTE    = [BMW_BLUE, CYAN, GREEN, AMBER, ROSE, PURPLE, PINK]

BG_DARK    = "#0A0E17"
CARD_BG    = "rgba(17,25,40,0.78)"
BORDER     = "rgba(255,255,255,0.07)"
TEXT_PRI   = "#E2E8F0"
TEXT_MUT   = "#94A3B8"

CHART_TPL = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, -apple-system, sans-serif", color="#CBD5E1", size=12),
    margin=dict(l=24, r=24, t=36, b=24),
    hoverlabel=dict(bgcolor="#1e293b", font_size=12, font_family="Inter",
                    bordercolor="rgba(255,255,255,0.1)"),
)

def apply_grid(fig):
    fig.update_xaxes(gridcolor="#1e293b", zerolinecolor="#1e293b")
    fig.update_yaxes(gridcolor="#1e293b", zerolinecolor="#1e293b")
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CUSTOM CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ─ reset & base ─ */
* { box-sizing: border-box; }
body {
    margin: 0; padding: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: radial-gradient(ellipse at 18% -5%, #0d1b2a 0%, #0A0E17 65%);
    color: #E2E8F0;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
}
#_dash-app-content { background: transparent; }

/* ─ scrollbar ─ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }

/* ─ sidebar ─ */
.sidebar {
    position: fixed; top: 0; left: 0; bottom: 0; width: 280px; z-index: 100;
    background: linear-gradient(195deg, #0f172a 0%, #0A0E17 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
    padding: 1.5rem 1.25rem; overflow-y: auto;
    display: flex; flex-direction: column;
}
.sidebar-logo { text-align: center; margin-bottom: 1.2rem; }
.sidebar-logo img { width: 64px; filter: drop-shadow(0 0 14px rgba(28,105,212,.45)); }
.sidebar-logo h2 { color: #fff; font-size: 1.05rem; margin: .6rem 0 0; font-weight: 700; }
.sidebar-logo p  { color: #64748b; font-size: .68rem; margin: .15rem 0 0; }
.sidebar hr { border: 0; border-top: 1px solid rgba(255,255,255,0.06); margin: .8rem 0; }
.filter-label {
    color: #94A3B8; font-size: .75rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .7px; margin-bottom: .35rem;
}
.sidebar .Select-control, .sidebar .Select-menu-outer { font-size: .82rem !important; }
.sidebar-version {
    margin-top: auto; text-align: center; color: #475569; font-size: .68rem; padding-top: .8rem;
}

/* ─ main content ─ */
.main-content { margin-left: 280px; padding: 1.5rem 2rem 2rem; }

/* ─ hero banner ─ */
.hero-banner {
    background: linear-gradient(135deg, #1C69D4 0%, #0f172a 100%);
    border-radius: 16px; padding: 1.8rem 2.2rem; margin-bottom: 1.5rem;
    border: 1px solid rgba(28,105,212,0.3);
    box-shadow: 0 4px 30px rgba(28,105,212,0.12);
}
.hero-banner h1 { color: #fff; font-weight: 800; font-size: 1.7rem; margin: 0 0 .25rem; }
.hero-banner p  { color: rgba(255,255,255,0.7); font-size: .9rem; margin: 0; }

/* ─ KPI cards ─ */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
@media (max-width: 1100px) { .kpi-row { grid-template-columns: repeat(2,1fr); } }
@media (max-width: 600px)  { .kpi-row { grid-template-columns: 1fr; } }
.kpi-card {
    background: rgba(17,25,40,0.78); backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.07); border-radius: 14px;
    padding: 1.2rem 1.4rem; position: relative; overflow: hidden;
    transition: transform .2s, box-shadow .2s;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(0,0,0,.35); }
.kpi-icon {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
    margin-bottom: .55rem;
}
.kpi-value { color: #fff; font-size: 1.6rem; font-weight: 700; line-height: 1.1; }
.kpi-label { color: #94A3B8; font-size: .72rem; font-weight: 600; text-transform: uppercase;
             letter-spacing: .6px; margin-top: .2rem; }
.kpi-bar  { position: absolute; bottom: 0; left: 0; height: 3px; width: 100%; border-radius: 0 0 14px 14px; }

/* accent helpers */
.accent-blue  .kpi-icon { background: rgba(28,105,212,.18); color: #1C69D4; }
.accent-blue  .kpi-bar  { background: #1C69D4; }
.accent-cyan  .kpi-icon { background: rgba(34,211,238,.13); color: #22D3EE; }
.accent-cyan  .kpi-bar  { background: #22D3EE; }
.accent-green .kpi-icon { background: rgba(52,211,153,.13); color: #34D399; }
.accent-green .kpi-bar  { background: #34D399; }
.accent-amber .kpi-icon { background: rgba(251,191,36,.13); color: #FBBF24; }
.accent-amber .kpi-bar  { background: #FBBF24; }

/* ─ glass card (chart wrapper) ─ */
.glass-card {
    background: rgba(17,25,40,0.78); backdrop-filter: blur(14px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.07); border-radius: 14px;
    padding: 1.3rem 1.5rem; margin-bottom: 1rem;
    transition: transform .2s, box-shadow .2s;
}
.glass-card:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,.3); }
.card-title { color: #E2E8F0; font-size: 1rem; font-weight: 600; margin: 0 0 .1rem; }
.card-sub   { color: #94A3B8; font-size: .76rem; margin: 0 0 .7rem; }

/* ─ tab styling ─ */
.custom-tabs .tab { border: none !important; }
.custom-tabs .tab--selected {
    border-bottom: 2px solid #22D3EE !important; color: #22D3EE !important;
    font-weight: 600 !important;
}

/* ─ nav tabs (dbc) ─ */
.nav-pills .nav-link       { color: #94A3B8; font-weight: 500; border-radius: 8px; }
.nav-pills .nav-link.active { background: rgba(28,105,212,.2); color: #22D3EE; font-weight: 600; }

/* ─ data table ─ */
.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td,
.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th {
    font-family: 'Inter', sans-serif !important; font-size: .8rem;
    border-color: rgba(255,255,255,0.04) !important;
}

/* ─ footer ─ */
.footer { text-align: center; color: #475569; font-size: .72rem; padding: 1.5rem 0 1rem;
          border-top: 1px solid rgba(255,255,255,0.04); margin-top: 1.5rem; }

/* ─ dash dropdown overrides ─ */
.Select-control       { background: #0f172a !important; border-color: rgba(255,255,255,0.08) !important; }
.Select-value-label   { color: #E2E8F0 !important; }
.Select-menu-outer    { background: #0f172a !important; border-color: rgba(255,255,255,0.08) !important; }
.Select-option        { color: #CBD5E1 !important; background-color: #0f172a !important; }
.Select-option.is-focused { background-color: rgba(28,105,212,.3) !important; }
.Select-placeholder   { color: #64748b !important; }
.VirtualizedSelectOption { color: #CBD5E1 !important; }

.rc-slider-track { background-color: #1C69D4 !important; }
.rc-slider-handle { border-color: #1C69D4 !important; background: #fff !important; }
.rc-slider-rail { background-color: #1e293b !important; }
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DASH APP INIT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE],
    suppress_callback_exceptions=True,
    title="BMW Analytics | Used Car Intelligence",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server  # for deployment

# inject custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>''' + CUSTOM_CSS + '''</style>
    </head>
    <body>
        {%app_entry%}
        <footer>{%config%}{%scripts%}{%renderer%}</footer>
    </body>
</html>
'''

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HELPER — KPI card
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def kpi_card(icon, value, label, accent):
    return html.Div(className=f"kpi-card accent-{accent}", children=[
        html.Div(icon, className="kpi-icon"),
        html.Div(value, className="kpi-value"),
        html.Div(label, className="kpi-label"),
        html.Div(className="kpi-bar"),
    ])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HELPER — glass chart card
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def chart_card(title, subtitle, graph_id, height=380):
    return html.Div(className="glass-card", children=[
        html.P(title, className="card-title"),
        html.P(subtitle, className="card-sub"),
        dcc.Graph(id=graph_id, config={"displayModeBar": False},
                  style={"height": f"{height}px"}),
    ])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sidebar = html.Div(className="sidebar", children=[
    html.Div(className="sidebar-logo", children=[
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/600px-BMW.svg.png"),
        html.H2("BMW Intelligence"),
        html.P("Used Car Analytics Platform"),
    ]),
    html.Hr(),

    # Year range
    html.Div(className="filter-label", children="Model Year"),
    dcc.RangeSlider(
        id="filter-year",
        min=int(raw_df["year"].min()), max=int(raw_df["year"].max()),
        value=[int(raw_df["year"].min()), int(raw_df["year"].max())],
        marks={y: {"label": str(y), "style": {"color": "#64748b", "fontSize": ".68rem"}}
               for y in range(int(raw_df["year"].min()), int(raw_df["year"].max()) + 1, 2)},
        tooltip={"placement": "bottom", "always_visible": False},
    ),
    html.Br(),

    # Fuel type
    html.Div(className="filter-label", children="Fuel Type"),
    dcc.Dropdown(
        id="filter-fuel",
        options=[{"label": f, "value": f} for f in sorted(raw_df["fuelType"].unique())],
        value=sorted(raw_df["fuelType"].unique().tolist()),
        multi=True, placeholder="All fuel types",
        style={"fontSize": ".82rem"},
    ),
    html.Br(),

    # Transmission
    html.Div(className="filter-label", children="Transmission"),
    dcc.Dropdown(
        id="filter-trans",
        options=[{"label": t, "value": t} for t in sorted(raw_df["transmission"].unique())],
        value=sorted(raw_df["transmission"].unique().tolist()),
        multi=True, placeholder="All transmissions",
        style={"fontSize": ".82rem"},
    ),
    html.Br(),

    # Price range
    html.Div(className="filter-label", children="Price Range (£)"),
    dcc.RangeSlider(
        id="filter-price",
        min=int(raw_df["price"].min()), max=int(raw_df["price"].max()),
        value=[int(raw_df["price"].min()), int(raw_df["price"].max())],
        step=500,
        tooltip={"placement": "bottom", "always_visible": False},
        marks={
            int(raw_df["price"].min()): {"label": f"£{int(raw_df['price'].min()):,}", "style": {"color": "#64748b", "fontSize": ".68rem"}},
            int(raw_df["price"].max()): {"label": f"£{int(raw_df['price'].max()):,}", "style": {"color": "#64748b", "fontSize": ".68rem"}},
        },
    ),
    html.Br(),

    # Model
    html.Div(className="filter-label", children="Model (optional)"),
    dcc.Dropdown(
        id="filter-model",
        options=[{"label": m, "value": m} for m in sorted(raw_df["model"].unique())],
        value=[],
        multi=True, placeholder="All models",
        style={"fontSize": ".82rem"},
    ),

    html.Div(className="sidebar-version", children="v3.0 · Dash + Plotly"),
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MAIN CONTENT LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
main_content = html.Div(className="main-content", children=[

    # Hero banner
    html.Div(className="hero-banner", children=[
        html.H1("BMW Used Car Intelligence"),
        html.P(id="hero-subtitle"),
    ]),

    # KPI row
    html.Div(id="kpi-row", className="kpi-row"),

    # Tabs
    dbc.Tabs(id="main-tabs", active_tab="tab-overview", className="mb-3", children=[
        dbc.Tab(label="Overview",           tab_id="tab-overview",  label_style={"fontWeight": "500"}),
        dbc.Tab(label="Pricing Deep-Dive",  tab_id="tab-pricing",   label_style={"fontWeight": "500"}),
        dbc.Tab(label="Inventory Mix",      tab_id="tab-inventory", label_style={"fontWeight": "500"}),
        dbc.Tab(label="Data Explorer",      tab_id="tab-data",      label_style={"fontWeight": "500"}),
    ]),

    html.Div(id="tab-content"),

    # Footer
    html.Div(className="footer", children=[
        "BMW Used Car Intelligence · Built with Dash & Plotly · Data for demonstration purposes",
    ]),
])

app.layout = html.Div([sidebar, main_content])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FILTER HELPER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def filter_df(year_range, fuels, trans, price_range, models):
    dff = raw_df.copy()
    dff = dff[dff["year"].between(year_range[0], year_range[1])]
    if fuels:
        dff = dff[dff["fuelType"].isin(fuels)]
    if trans:
        dff = dff[dff["transmission"].isin(trans)]
    dff = dff[dff["price"].between(price_range[0], price_range[1])]
    if models:
        dff = dff[dff["model"].isin(models)]
    return dff


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TAB CONTENT BUILDERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def make_overview():
    return html.Div([
        dbc.Row([
            dbc.Col(chart_card("Fuel Type Breakdown",
                               "Number of listings per fuel category",
                               "chart-fuel-bar", 370), md=6),
            dbc.Col(chart_card("Transmission Split",
                               "Proportion by gearbox type",
                               "chart-trans-donut", 370), md=6),
        ]),
        dbc.Row([
            dbc.Col(chart_card("Average Price Trajectory",
                               "Year-over-year average listing price with area fill",
                               "chart-price-trend", 380), md=12),
        ]),
        dbc.Row([
            dbc.Col(chart_card("MPG Distribution by Fuel",
                               "Box plot showing range & quartiles",
                               "chart-mpg-box", 370), md=6),
            dbc.Col(chart_card("Engine Size Distribution",
                               "Share of each engine capacity",
                               "chart-engine-donut", 370), md=6),
        ]),
    ])


def make_pricing():
    return html.Div([
        dbc.Row([
            dbc.Col(chart_card("Price vs Mileage",
                               "Each dot = one listing · sized by engine capacity",
                               "chart-scatter", 440), md=6),
            dbc.Col(chart_card("Mileage Distribution",
                               "Histogram with marginal box plot",
                               "chart-mileage-hist", 440), md=6),
        ]),
        dbc.Row([
            dbc.Col(chart_card("Price Distribution by Fuel Type",
                               "Violin plot showing density + quartiles",
                               "chart-violin", 420), md=12),
        ]),
        dbc.Row([
            dbc.Col(chart_card("Year × Fuel Type — Average Price Matrix",
                               "Spot value pockets across year & fuel combinations",
                               "chart-heatmap", 350), md=12),
        ]),
    ])


def make_inventory():
    return html.Div([
        dbc.Row([
            dbc.Col(chart_card("Top 12 Models by Volume",
                               "Horizontal ranking of most-listed models",
                               "chart-top-models", 480), md=7),
            dbc.Col(chart_card("Engine Size Split",
                               "Distribution of engine capacities",
                               "chart-engine-pie", 480), md=5),
        ]),
        dbc.Row([
            dbc.Col(chart_card("Model × Transmission Treemap",
                               "Proportional area map — larger blocks = more listings",
                               "chart-treemap", 460), md=12),
        ]),
        dbc.Row([
            dbc.Col(chart_card("Fuel → Transmission → Engine Sunburst",
                               "Hierarchical drill-down of inventory structure",
                               "chart-sunburst", 450), md=6),
            dbc.Col(chart_card("MPG vs Tax — Efficiency Matrix",
                               "Bubble size = number of listings per fuel type",
                               "chart-efficiency", 450), md=6),
        ]),
    ])


def make_data_explorer(dff):
    col_order = ["model", "year", "price", "transmission", "mileage", "fuelType", "tax", "mpg", "engineSize"]
    table_df = dff[col_order].sort_values("price", ascending=False).reset_index(drop=True)
    stats_df = dff.describe().T.reset_index().rename(columns={"index": "Column"})
    for c in stats_df.columns[1:]:
        stats_df[c] = stats_df[c].apply(lambda x: f"{x:,.1f}")

    return html.Div([
        html.Div(className="glass-card", children=[
            html.P("Filtered Dataset", className="card-title"),
            html.P(f"Showing {len(dff):,} records — use sidebar to refine", className="card-sub"),
            dash_table.DataTable(
                id="data-table",
                columns=[{"name": c.title(), "id": c} for c in col_order],
                data=table_df.head(500).to_dict("records"),
                page_size=20,
                sort_action="native",
                filter_action="native",
                style_table={"overflowX": "auto"},
                style_header={
                    "backgroundColor": "#0f172a", "color": "#94A3B8",
                    "fontWeight": "600", "fontSize": ".78rem",
                    "borderBottom": "1px solid rgba(255,255,255,0.1)",
                    "textTransform": "uppercase", "letterSpacing": ".5px",
                },
                style_cell={
                    "backgroundColor": "transparent", "color": "#CBD5E1",
                    "border": "1px solid rgba(255,255,255,0.04)",
                    "padding": "10px 14px", "fontSize": ".82rem",
                    "fontFamily": "Inter, sans-serif",
                },
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": "rgba(255,255,255,0.02)"},
                    {"if": {"state": "active"}, "backgroundColor": "rgba(28,105,212,0.15)",
                     "border": "1px solid rgba(28,105,212,0.3)"},
                ],
                style_filter={
                    "backgroundColor": "#0f172a", "color": "#CBD5E1",
                    "border": "1px solid rgba(255,255,255,0.08)",
                },
            ),
        ]),
        html.Br(),
        html.Div(className="glass-card", children=[
            html.P("Quick Statistics", className="card-title"),
            html.P("Summary of numeric columns in current filter", className="card-sub"),
            dash_table.DataTable(
                columns=[{"name": c, "id": c} for c in stats_df.columns],
                data=stats_df.to_dict("records"),
                style_header={
                    "backgroundColor": "#0f172a", "color": "#94A3B8",
                    "fontWeight": "600", "fontSize": ".78rem",
                    "borderBottom": "1px solid rgba(255,255,255,0.1)",
                },
                style_cell={
                    "backgroundColor": "transparent", "color": "#CBD5E1",
                    "border": "1px solid rgba(255,255,255,0.04)",
                    "padding": "8px 12px", "fontSize": ".8rem",
                    "fontFamily": "Inter, sans-serif",
                },
            ),
        ]),
    ])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MASTER CALLBACK — updates everything in one pass
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@callback(
    Output("hero-subtitle", "children"),
    Output("kpi-row", "children"),
    Output("tab-content", "children"),
    Input("filter-year", "value"),
    Input("filter-fuel", "value"),
    Input("filter-trans", "value"),
    Input("filter-price", "value"),
    Input("filter-model", "value"),
    Input("main-tabs", "active_tab"),
)
def update_dashboard(year_range, fuels, trans, price_range, models, active_tab):
    dff = filter_df(year_range, fuels, trans, price_range, models)
    n_filtered = len(dff)
    n_total = len(raw_df)

    # ── Hero subtitle ────────────────────────────
    subtitle = f"Real-time analytics across {n_filtered:,} listings from a universe of {n_total:,} vehicles"

    # ── KPIs ─────────────────────────────────────
    avg_price   = dff["price"].mean()      if n_filtered else 0
    avg_mileage = dff["mileage"].mean()    if n_filtered else 0
    avg_mpg     = dff["mpg"].mean()        if n_filtered else 0
    avg_engine  = dff["engineSize"].mean() if n_filtered else 0

    kpis = [
        kpi_card("💷", f"£{avg_price:,.0f}",        "Avg Price",   "blue"),
        kpi_card("🛣️", f"{avg_mileage:,.0f}",       "Avg Mileage", "cyan"),
        kpi_card("⛽", f"{avg_mpg:.1f}",             "Avg MPG",     "green"),
        kpi_card("🔧", f"{avg_engine:.1f}L",         "Avg Engine",  "amber"),
    ]

    # ── Tab content ──────────────────────────────
    if active_tab == "tab-overview":
        content = make_overview()
    elif active_tab == "tab-pricing":
        content = make_pricing()
    elif active_tab == "tab-inventory":
        content = make_inventory()
    else:
        content = make_data_explorer(dff)

    return subtitle, kpis, content


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CHART CALLBACKS — OVERVIEW TAB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@callback(Output("chart-fuel-bar", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_fuel_bar(yr, fu, tr, pr, mo, tab):
    if tab != "tab-overview":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    fc = dff["fuelType"].value_counts().reset_index()
    fc.columns = ["Fuel Type", "Count"]
    fig = px.bar(fc, x="Fuel Type", y="Count", color="Fuel Type",
                 color_discrete_sequence=PALETTE, text_auto=True)
    fig.update_layout(**CHART_TPL, showlegend=False, height=370)
    fig.update_traces(textposition="outside", marker_line_width=0, marker_cornerradius=5)
    return apply_grid(fig)


@callback(Output("chart-trans-donut", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_trans_donut(yr, fu, tr, pr, mo, tab):
    if tab != "tab-overview":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    tc = dff["transmission"].value_counts().reset_index()
    tc.columns = ["Transmission", "Count"]
    fig = px.pie(tc, names="Transmission", values="Count", hole=0.55,
                 color_discrete_sequence=PALETTE)
    fig.update_layout(**CHART_TPL, height=370, showlegend=True,
                      legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"))
    fig.update_traces(textinfo="percent+label", textfont_size=12,
                      pull=[0.02]*len(tc))
    return apply_grid(fig)


@callback(Output("chart-price-trend", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_price_trend(yr, fu, tr, pr, mo, tab):
    if tab != "tab-overview":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    agg = dff.groupby("year").agg(avg_price=("price", "mean")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=agg["year"], y=agg["avg_price"], mode="lines+markers",
        line=dict(color=CYAN, width=3, shape="spline"),
        marker=dict(size=8, color=CYAN, line=dict(width=2, color=BG_DARK)),
        fill="tozeroy", fillcolor="rgba(34,211,238,0.08)",
        hovertemplate="<b>%{x}</b><br>Avg: £%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(**CHART_TPL, height=380,
                      xaxis=dict(title="Year", dtick=1),
                      yaxis=dict(title="Avg Price (£)", tickprefix="£", separatethousands=True))
    return apply_grid(fig)


@callback(Output("chart-mpg-box", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_mpg_box(yr, fu, tr, pr, mo, tab):
    if tab != "tab-overview":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    fig = px.box(dff, x="fuelType", y="mpg", color="fuelType",
                 color_discrete_sequence=PALETTE)
    fig.update_layout(**CHART_TPL, height=370, showlegend=False,
                      xaxis_title="Fuel Type", yaxis_title="MPG")
    return apply_grid(fig)


@callback(Output("chart-engine-donut", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_engine_donut(yr, fu, tr, pr, mo, tab):
    if tab != "tab-overview":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    ec = dff["engineSize"].value_counts().sort_index().reset_index()
    ec.columns = ["Engine (L)", "Count"]
    ec["Engine (L)"] = ec["Engine (L)"].astype(str) + "L"
    fig = px.pie(ec, names="Engine (L)", values="Count", hole=0.5,
                 color_discrete_sequence=PALETTE)
    fig.update_layout(**CHART_TPL, height=370,
                      legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"))
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    return apply_grid(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CHART CALLBACKS — PRICING TAB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@callback(Output("chart-scatter", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_scatter(yr, fu, tr, pr, mo, tab):
    if tab != "tab-pricing":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    fig = px.scatter(dff, x="mileage", y="price", color="fuelType",
                     size="engineSize", opacity=0.65,
                     hover_data=["model", "year", "transmission"],
                     color_discrete_sequence=PALETTE)
    fig.update_layout(**CHART_TPL, height=440,
                      xaxis_title="Mileage", yaxis_title="Price (£)",
                      legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"))
    return apply_grid(fig)


@callback(Output("chart-mileage-hist", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_mileage_hist(yr, fu, tr, pr, mo, tab):
    if tab != "tab-pricing":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    fig = px.histogram(dff, x="mileage", nbins=40,
                       color_discrete_sequence=[BMW_BLUE], marginal="box")
    fig.update_layout(**CHART_TPL, height=440,
                      xaxis_title="Mileage", yaxis_title="Frequency", bargap=0.03)
    fig.update_traces(marker_line_width=0)
    return apply_grid(fig)


@callback(Output("chart-violin", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_violin(yr, fu, tr, pr, mo, tab):
    if tab != "tab-pricing":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    fig = px.violin(dff, x="fuelType", y="price", color="fuelType",
                    box=True, points=False, color_discrete_sequence=PALETTE)
    fig.update_layout(**CHART_TPL, height=420, showlegend=False,
                      xaxis_title="Fuel Type", yaxis_title="Price (£)")
    return apply_grid(fig)


@callback(Output("chart-heatmap", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_heatmap(yr, fu, tr, pr, mo, tab):
    if tab != "tab-pricing":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    heat = dff.pivot_table(values="price", index="fuelType", columns="year", aggfunc="mean")
    fig = px.imshow(heat, text_auto=",.0f", color_continuous_scale="Blues", aspect="auto")
    fig.update_layout(**CHART_TPL, height=350,
                      xaxis_title="Year", yaxis_title="Fuel Type",
                      coloraxis_colorbar=dict(title="Avg £", tickprefix="£"))
    return apply_grid(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CHART CALLBACKS — INVENTORY TAB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@callback(Output("chart-top-models", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_top_models(yr, fu, tr, pr, mo, tab):
    if tab != "tab-inventory":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    top = dff["model"].value_counts().head(12).reset_index()
    top.columns = ["Model", "Count"]
    fig = px.bar(top, x="Count", y="Model", orientation="h",
                 color="Count", color_continuous_scale=["#0f172a", BMW_BLUE, CYAN],
                 text_auto=True)
    fig.update_layout(**CHART_TPL, height=480, coloraxis_showscale=False)
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(marker_line_width=0, textposition="outside", marker_cornerradius=4)
    return apply_grid(fig)


@callback(Output("chart-engine-pie", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_engine_pie(yr, fu, tr, pr, mo, tab):
    if tab != "tab-inventory":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    ec = dff["engineSize"].value_counts().sort_index().reset_index()
    ec.columns = ["Engine (L)", "Count"]
    ec["Engine (L)"] = ec["Engine (L)"].astype(str) + "L"
    fig = px.pie(ec, names="Engine (L)", values="Count", hole=0.5,
                 color_discrete_sequence=PALETTE)
    fig.update_layout(**CHART_TPL, height=480,
                      legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"))
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    return apply_grid(fig)


@callback(Output("chart-treemap", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_treemap(yr, fu, tr, pr, mo, tab):
    if tab != "tab-inventory":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    tree = dff.groupby(["model", "transmission"]).size().reset_index(name="count")
    tree = tree.sort_values("count", ascending=False).head(40)
    fig = px.treemap(tree, path=["model", "transmission"], values="count",
                     color="count", color_continuous_scale=["#0f172a", BMW_BLUE, CYAN])
    fig.update_layout(**CHART_TPL, height=460, coloraxis_showscale=False)
    fig.update_traces(marker_line_width=1, marker_line_color="rgba(255,255,255,0.06)",
                      textfont_size=13)
    return apply_grid(fig)


@callback(Output("chart-sunburst", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_sunburst(yr, fu, tr, pr, mo, tab):
    if tab != "tab-inventory":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    sun = dff.assign(engine_label=dff["engineSize"].astype(str) + "L")
    sun = sun.groupby(["fuelType", "transmission", "engine_label"]).size().reset_index(name="count")
    fig = px.sunburst(sun, path=["fuelType", "transmission", "engine_label"],
                      values="count", color_discrete_sequence=PALETTE)
    fig.update_layout(**CHART_TPL, height=450)
    fig.update_traces(textfont_size=12)
    return apply_grid(fig)


@callback(Output("chart-efficiency", "figure"),
          Input("filter-year", "value"), Input("filter-fuel", "value"),
          Input("filter-trans", "value"), Input("filter-price", "value"),
          Input("filter-model", "value"), Input("main-tabs", "active_tab"))
def chart_efficiency(yr, fu, tr, pr, mo, tab):
    if tab != "tab-inventory":
        raise dash.exceptions.PreventUpdate
    dff = filter_df(yr, fu, tr, pr, mo)
    eff = dff.groupby("fuelType").agg(
        mpg=("mpg", "mean"), tax=("tax", "mean"),
        count=("price", "count"), price=("price", "mean"),
    ).reset_index()
    fig = px.scatter(eff, x="mpg", y="tax", size="count", color="fuelType",
                     hover_data=["price"], color_discrete_sequence=PALETTE, size_max=55)
    fig.update_layout(**CHART_TPL, height=450,
                      xaxis_title="Avg MPG", yaxis_title="Avg Tax (£)")
    return apply_grid(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  RUN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    app.run(debug=True, port=8050)
