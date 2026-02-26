<div align="center">

# 🏎️ BMW Used Car Intelligence Dashboard

### A Premium, Production-Grade Analytics Platform for BMW Used Car Market Insights

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Repo Size](https://img.shields.io/github/repo-size/Arjunan-lab/Streamlit_WebUI?style=for-the-badge&color=blue)](https://github.com/Arjunan-lab/Streamlit_WebUI)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://appwebui-6z76crdkhzio2ntdgkax36.streamlit.app/)

<br/>

**Explore 10,000+ BMW used car listings through an elegant glassmorphism dashboard featuring 13+ interactive visualizations, real-time filtering, and one-click data export.**

### [🔴 Live Demo](https://appwebui-6z76crdkhzio2ntdgkax36.streamlit.app/)

[Getting Started](#-getting-started) · [Features](#-features-at-a-glance) · [Dashboard Walkthrough](#️-dashboard-walkthrough) · [Tech Stack](#️-tech-stack) · [Contributing](#-contributing)

</div>

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Features at a Glance](#-features-at-a-glance)
- [Project Structure](#️-project-structure)
- [Dataset](#-dataset)
- [Getting Started](#-getting-started)
- [Dashboard Walkthrough](#️-dashboard-walkthrough)
- [Architecture & Code Structure](#-architecture--code-structure)
- [Design System](#-design-system)
- [Tech Stack](#️-tech-stack)
- [Dependencies](#-dependencies)
- [Performance Optimizations](#-performance-optimizations)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 📖 About the Project

**BMW Used Car Intelligence** is a full-featured, interactive data analytics dashboard designed to provide deep insights into the BMW used car market in the United Kingdom. Built entirely in Python using Streamlit as the web framework and Plotly for visualization, this project transforms a raw CSV dataset of 10,782 BMW listings into a rich, explorable intelligence platform.

### Why This Project?

The used car market is one of the most data-rich yet underserved sectors for consumer analytics. Buyers, dealers, and analysts often struggle to answer critical questions like:

- *"What's the fair price for a 2018 BMW 3 Series with 30,000 miles?"*
- *"Which fuel types hold value best over time?"*
- *"How does transmission type affect pricing across different models?"*
- *"What's the most cost-efficient engine size for daily driving?"*

This dashboard answers all of these questions — and more — through intuitive, interactive visualizations that update in real time as users adjust filters.

### Key Objectives

| Objective | How It's Achieved |
|-----------|-------------------|
| **Market Transparency** | 13+ chart types reveal pricing patterns, depreciation curves, and inventory composition |
| **Interactive Exploration** | 5 sidebar filters (year, fuel, transmission, price, model) instantly update all visuals |
| **Professional Presentation** | Glassmorphism UI with BMW brand palette delivers a polished, premium feel |
| **Data Accessibility** | One-click CSV export lets users download any filtered subset for offline analysis |
| **Performance** | `@st.cache_data` ensures the 10K+ row dataset loads once and filters in milliseconds |

---

## 📸 Features at a Glance

| Feature | Description |
|---------|-------------|
| 🎯 **4 KPI Cards** | Real-time average price, mileage, MPG, and engine size — recalculated on every filter change |
| 🎛️ **5 Dynamic Filters** | Sidebar controls: Model Year (range slider), Fuel Type, Transmission (multi-select), Price Range (range slider), Model |
| 📊 **4 Analytics Tabs** | Overview · Pricing Deep-Dive · Inventory Mix · Data Explorer |
| 📈 **13+ Chart Types** | Bar, donut/pie, spline line with area fill, scatter, histogram with marginal box plot, violin, heatmap, horizontal bar, treemap, sunburst, bubble, data table |
| 🌗 **Dark Glassmorphism UI** | Custom CSS: translucent cards, `backdrop-filter: blur(16px)`, hover animations, BMW brand palette |
| ⬇️ **CSV Export** | Download filtered dataset directly as `bmw_filtered_export.csv` |
| 📋 **Summary Statistics** | Auto-generated descriptive statistics (count, mean, std, min, 25%, 50%, 75%, max) for all numeric columns |
| 🏎️ **BMW Branding** | Official BMW logo in sidebar, brand blue (`#1C69D4`), hero banner with gradient, and branded footer |
| 📱 **Responsive Layout** | KPI grid switches from 4-column to 2-column on screens under 768px |
| 🔒 **Clean Data Pipeline** | Automatic removal of null values and duplicates on load via cached function |

---

## 🗂️ Project Structure

```
Streamlit_WebUI/
│
├── app1.py              # Main Streamlit dashboard (560 lines)
│                        #   ├── Page config & CSS injection (~160 lines)
│                        #   ├── Data loading with caching
│                        #   ├── Shared Plotly theme & color palette
│                        #   ├── Sidebar filters (5 controls)
│                        #   ├── Hero banner with live counter
│                        #   ├── KPI row (4 metric cards)
│                        #   ├── Tab 1: Overview (3 charts)
│                        #   ├── Tab 2: Pricing Deep-Dive (4 charts)
│                        #   ├── Tab 3: Inventory Mix (5 charts)
│                        #   ├── Tab 4: Data Explorer (table + stats)
│                        #   └── Footer
│
├── bmw.csv              # Dataset — 10,782 BMW used car listings (9 columns)
├── requirements.txt     # Python dependencies
└── README.md            # This documentation
```

---

## 📊 Dataset

The dataset (`bmw.csv`) contains **10,782 real-world BMW used car listings** scraped from UK automotive marketplaces. After the automated cleaning pipeline (drop nulls + deduplicate), the working dataset is used across all dashboards and filters.

### Schema

| # | Column | Type | Description | Example Values |
|---|--------|------|-------------|----------------|
| 1 | `model` | string | BMW model series/name | `1 Series`, `3 Series`, `X5`, `Z4` |
| 2 | `year` | int | Year of first registration | `2014` – `2020` |
| 3 | `price` | int | Listed sale price in GBP (£) | `£1,500` – `£123,456` |
| 4 | `transmission` | string | Gearbox type | `Automatic`, `Manual`, `Semi-Auto` |
| 5 | `mileage` | int | Odometer reading in miles | `1` – `214,000+` |
| 6 | `fuelType` | string | Fuel/power category | `Petrol`, `Diesel`, `Hybrid`, `Electric`, `Other` |
| 7 | `tax` | int | Annual UK road tax in GBP (£) | `£0` – `£580` |
| 8 | `mpg` | float | Miles per gallon (fuel economy) | `12.4` – `470.8` |
| 9 | `engineSize` | float | Engine displacement in litres | `0.0` – `6.6` |

### Data Cleaning Pipeline

```python
@st.cache_data
def load_data():
    df = pd.read_csv("bmw.csv")
    df.dropna(inplace=True)       # Remove rows with any missing values
    df.drop_duplicates(inplace=True)  # Remove exact duplicate rows
    return df
```

- **Null Handling**: Any row with a missing value in any column is dropped entirely (complete-case analysis)
- **Deduplication**: Exact row-level duplicates are removed to prevent double-counting
- **Caching**: `@st.cache_data` ensures the CSV is read and cleaned only once per session; subsequent interactions use the in-memory cached DataFrame

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.8 or higher |
| pip | Latest recommended |
| Browser | Any modern browser (Chrome, Firefox, Edge, Safari) |

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Arjunan-lab/Streamlit_WebUI.git
   cd Streamlit_WebUI
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   streamlit run app1.py
   ```

5. **Open in browser**
   - Streamlit will automatically open `http://localhost:8501` in your default browser
   - If not, navigate to the URL manually
   - The Network URL (e.g., `http://192.168.x.x:8501`) allows access from other devices on the same network

> **Or skip all the above and try the live deployment instantly:**
> **https://appwebui-6z76crdkhzio2ntdgkax36.streamlit.app/**

### Quick Start (One-Liner)

```bash
git clone https://github.com/Arjunan-lab/Streamlit_WebUI.git && cd Streamlit_WebUI && pip install -r requirements.txt && streamlit run app1.py
```

---

## 🖥️ Dashboard Walkthrough

### 🏠 Hero Banner

The top of the page displays a gradient banner showing:
- The app title: **"🏎️ BMW Used Car Intelligence"**
- A live counter: *"Real-time analytics across **X** listings from a universe of **Y** vehicles"*
- X updates dynamically as filters change; Y is the total unfiltered dataset size

### 🎯 KPI Row (4 Metric Cards)

Immediately below the banner, four glass-styled KPI chips provide at-a-glance metrics for the current filter selection:

| KPI | Icon | Color Accent | Metric |
|-----|------|-------------|--------|
| **Avg Price** | 💷 | BMW Blue (`#1C69D4`) | Mean listing price in £ |
| **Avg Mileage** | 🛣️ | Cyan (`#22D3EE`) | Mean odometer reading |
| **Avg MPG** | ⛽ | Green (`#34D399`) | Mean fuel economy |
| **Avg Engine** | 🔧 | Amber (`#FBBF24`) | Mean engine displacement in litres |

Each card features:
- A colored icon badge with translucent background
- Large bold numeric value
- Uppercase label with letter-spacing
- A 3px accent bar along the bottom edge
- Hover animation (`translateY(-3px)`)

### 🎛️ Sidebar Filters

The left sidebar provides 5 interactive controls that dynamically filter the entire dashboard:

| Filter | Widget | Behavior |
|--------|--------|----------|
| **Model Year** | Range Slider | Selects a min–max year range from the dataset's full year span |
| **Fuel Type** | Multi-Select | Choose one or more fuel types; defaults to all |
| **Transmission** | Multi-Select | Choose one or more gearbox types; defaults to all |
| **Price Range (£)** | Range Slider (step: £500) | Sets a minimum and maximum price window |
| **Model** | Multi-Select | Optionally filter to specific BMW models; leave blank for all |

The sidebar also includes:
- The **official BMW logo** loaded from Wikimedia Commons with a blue glow drop-shadow
- Title: "BMW Intelligence" / "Used Car Analytics Platform"
- Version indicator: "v2.0 · Streamlit + Plotly"

### 📊 Tab 1 — Overview

Provides a high-level summary of the filtered market in 3 charts across 2 rows:

| Chart | Type | Layout | Description |
|-------|------|--------|-------------|
| **Fuel Type Breakdown** | Vertical Bar Chart | Left column (50%) | Color-coded bars showing the count of listings per fuel type (Petrol, Diesel, Hybrid, etc.). Labels shown outside bars with `text_auto=True`. |
| **Transmission Split** | Donut Chart (55% hole) | Right column (50%) | Proportional pie showing Automatic vs Manual vs Semi-Auto. Displays `percent+label`, with a subtle `pull` effect on each segment. Horizontal legend below. |
| **Average Price Trajectory** | Spline Line + Area Fill | Full width | Year-over-year average price trend. Uses `go.Scatter` with `shape="spline"` for smooth curves, circular markers with dark borders, and a translucent cyan area fill (`rgba(34,211,238,0.08)`). Custom hover template shows year and formatted price. |

### 💰 Tab 2 — Pricing Deep-Dive

Four visualizations focused on price analysis and distribution patterns:

| Chart | Type | Layout | Description |
|-------|------|--------|-------------|
| **Price vs Mileage** | Scatter Plot | Left column (50%) | Each dot represents one listing. X = mileage, Y = price. Color = fuel type. Bubble size = engine capacity. Opacity at 0.65 to handle overplotting. Hover reveals model, year, and transmission. |
| **Mileage Distribution** | Histogram + Marginal Box Plot | Right column (50%) | 40-bin histogram of mileage values in BMW Blue. A box plot above the histogram shows median, IQR, and outliers for quick statistical summary. |
| **Price Distribution by Fuel Type** | Violin Plot with Box | Full width | One violin per fuel type showing the full probability density of prices. Inner box shows quartiles (25th, median, 75th). Reveals how price distributions vary across fuel categories (e.g., Hybrid tends to cluster higher). |
| **Year × Fuel Type Heatmap** | Annotated Heatmap | Full width | Pivot table rendered as `px.imshow` with the Blues color scale. Rows = fuel types, columns = years. Each cell shows the average price formatted as `£XX,XXX`. Helps identify which year-fuel combinations offer the best value. |

### 🏗️ Tab 3 — Inventory Mix

Five visualizations mapping the structure and composition of available inventory:

| Chart | Type | Layout | Description |
|-------|------|--------|-------------|
| **Top 12 Models by Volume** | Horizontal Bar Chart | Left column (60%) | Ranks the 12 most-listed BMW models. Color gradient from dark navy → BMW Blue → cyan encodes count magnitude. Auto-reversed Y axis for rank-order readability. |
| **Engine Size Split** | Donut Chart (50% hole) | Right column (40%) | Shows the proportion of listings by engine displacement. Labels formatted as "X.XL". Horizontal legend below the chart. |
| **Model × Transmission Treemap** | Treemap | Full width | Two-level hierarchy: Model → Transmission. Area encodes listing count. Shows the top 40 model-transmission combinations. Subtle white border lines between cells. Color gradient matches the horizontal bar above. |
| **Fuel → Transmission → Engine Sunburst** | Sunburst Chart | Left column (50%) | Three-level radial hierarchy. Outer ring = engine size labels, middle = transmission, inner = fuel type. Click any segment to drill down. |
| **MPG vs Tax — Efficiency Matrix** | Bubble Chart | Right column (50%) | One bubble per fuel type. X = average MPG, Y = average tax (£). Bubble size = number of listings. Hover also shows average price. Quickly identifies which fuel types are most cost-efficient to run. |

### 📋 Tab 4 — Data Explorer

Raw data access and statistical summaries:

| Component | Description |
|-----------|-------------|
| **Filtered Data Table** | Full interactive `st.dataframe` showing all 9 columns for the current filter selection. Sorted by price (descending). Height: 520px. Columns: model, year, price, transmission, mileage, fuelType, tax, mpg, engineSize. |
| **CSV Download Button** | One-click download of the currently filtered dataset as `bmw_filtered_export.csv`. Uses `st.download_button` with UTF-8 encoding. |
| **Quick Statistics** | Auto-generated `DataFrame.describe().T` table formatted to 1 decimal place. Shows count, mean, std, min, 25%, 50%, 75%, max for all numeric columns. |

---

## 🏗 Architecture & Code Structure

The application follows a single-file architecture optimized for Streamlit's execution model (top-to-bottom re-run on every interaction):

```
┌─────────────────────────────────────────┐
│  1. PAGE CONFIG                         │  st.set_page_config()
├─────────────────────────────────────────┤
│  2. CSS INJECTION                       │  ~140 lines of custom CSS
│     • Root variables (BMW palette)      │  injected via st.markdown()
│     • Glass-card components             │
│     • KPI chip grid (responsive)        │
│     • Tab styling overrides             │
│     • Hide Streamlit branding           │
├─────────────────────────────────────────┤
│  3. DATA LAYER                          │  @st.cache_data → pd.read_csv()
│     • Load → Clean → Cache              │  dropna + drop_duplicates
├─────────────────────────────────────────┤
│  4. CHART THEME                         │  CHART_LAYOUT dict + PALETTE list
│     • Shared across all 13+ charts      │  plotly_dark template, transparent bg
├─────────────────────────────────────────┤
│  5. SIDEBAR                             │  BMW logo, 5 filter widgets
│     • Filters → Boolean mask            │  Outputs: `filtered` DataFrame
├─────────────────────────────────────────┤
│  6. HERO BANNER                         │  HTML with live record counter
├─────────────────────────────────────────┤
│  7. KPI ROW                             │  4 metric cards (HTML + inline data)
├─────────────────────────────────────────┤
│  8. TABBED CONTENT                      │  st.tabs() → 4 tabs
│     • Tab 1: Overview     (3 charts)    │  bar, donut, spline area
│     • Tab 2: Pricing      (4 charts)    │  scatter, hist, violin, heatmap
│     • Tab 3: Inventory    (5 charts)    │  h-bar, donut, treemap, sunburst, bubble
│     • Tab 4: Data Explorer              │  table, download, statistics
├─────────────────────────────────────────┤
│  9. FOOTER                              │  Centered attribution line
└─────────────────────────────────────────┘
```

### Filter Logic

All five sidebar controls combine into a single boolean mask applied to the full DataFrame:

```python
mask = (
    df["year"].between(*year_range)
    & df["fuelType"].isin(selected_fuels)
    & df["transmission"].isin(selected_trans)
    & df["price"].between(*price_range)
)
if selected_models:
    mask &= df["model"].isin(selected_models)
filtered = df[mask]
```

Every visualization downstream reads from `filtered`, ensuring consistency across all tabs and KPIs.

---

## 🎨 Design System

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bmw-blue` | `#1C69D4` | Primary accent, hero banner, KPI bar, chart highlights |
| `--bmw-dark` | `#0A0E17` | Main background, app base color |
| `--card-bg` | `rgba(17, 25, 40, 0.75)` | Glass card backgrounds |
| `--card-border` | `rgba(255, 255, 255, 0.08)` | Subtle card borders |
| `--text-primary` | `#E2E8F0` | Chart titles, headings |
| `--text-muted` | `#94A3B8` | Labels, subtitles, sidebar text |
| `--accent-cyan` | `#22D3EE` | Secondary accent, active tab, line charts |
| `--accent-green` | `#34D399` | MPG KPI, success indicators |
| `--accent-amber` | `#FBBF24` | Engine KPI, warning indicators |
| `--accent-rose` | `#FB7185` | Available for alerts/emphasis |

### Chart Color Sequence

All charts share a unified 7-color palette:
```
#1C69D4 → #22D3EE → #34D399 → #FBBF24 → #FB7185 → #A78BFA → #F472B6
 Blue      Cyan      Green     Amber     Rose      Purple    Pink
```

### Typography

- **Font**: [Inter](https://fonts.google.com/specimen/Inter) (weights: 300–700)
- **Loaded via**: Google Fonts CDN `@import` in the CSS block
- **Applied to**: Entire app via `html, body, [class*="css"]` selector

### Glassmorphism Technique

```css
.glass-card {
    background: rgba(17, 25, 40, 0.75);         /* semi-transparent dark */
    backdrop-filter: blur(16px) saturate(180%);  /* glass blur effect */
    border: 1px solid rgba(255, 255, 255, 0.08); /* subtle white border */
    border-radius: 14px;                          /* rounded corners */
    transition: transform .2s, box-shadow .2s;    /* smooth hover */
}
.glass-card:hover {
    transform: translateY(-2px);                  /* lift on hover */
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);     /* deeper shadow */
}
```

### Responsive Breakpoints

| Breakpoint | Behavior |
|------------|----------|
| `> 768px` | KPI grid: 4 columns |
| `≤ 768px` | KPI grid: 2 columns |
| All widths | Streamlit columns auto-stack on narrow viewports |

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| [Python](https://python.org) | 3.8+ | Core programming language |
| [Streamlit](https://streamlit.io/) | 1.x | Web application framework — handles layout, widgets, caching, and server |
| [Plotly Express](https://plotly.com/python/plotly-express/) | 5.x | High-level declarative charting (bar, pie, scatter, violin, histogram, treemap, sunburst, heatmap) |
| [Plotly Graph Objects](https://plotly.com/python/graph-objects/) | 5.x | Low-level chart API for custom spline line chart with area fill |
| [Pandas](https://pandas.pydata.org/) | 2.x | DataFrame operations — loading, cleaning, filtering, grouping, pivoting, aggregation |
| [NumPy](https://numpy.org/) | 1.x | Numerical computing (imported for potential extensions; used by Pandas internally) |
| HTML / CSS | — | Custom glassmorphism UI injected via `st.markdown(unsafe_allow_html=True)` |

---

## 📦 Dependencies

### requirements.txt

```
streamlit
pandas
plotly
numpy
```

### Install all at once

```bash
pip install streamlit pandas plotly numpy
```

### Full dependency tree (auto-installed)

Streamlit, Plotly, and Pandas each bring their own transitive dependencies (e.g., `pyarrow`, `tornado`, `tenacity`, etc.) which pip resolves automatically.

---

## ⚡ Performance Optimizations

| Technique | Implementation | Impact |
|-----------|----------------|--------|
| **Data Caching** | `@st.cache_data` on `load_data()` | CSV parsed & cleaned once; subsequent re-runs use cached DataFrame |
| **Boolean Masking** | Vectorized Pandas `.between()` and `.isin()` | Filters 10K+ rows in < 5ms |
| **Plotly Transparency** | `paper_bgcolor` and `plot_bgcolor` set to `rgba(0,0,0,0)` | Charts blend seamlessly into glass cards without extra rendering layers |
| **Compact Margins** | `margin=dict(l=20, r=20, t=30, b=20)` | Maximizes chart drawing area within each card |
| **Streamlit Branding Hidden** | `#MainMenu, footer, header { visibility: hidden; }` | Cleaner UI, no unnecessary DOM rendering |

---

## 🗺️ Future Roadmap

- [ ] **Predictive Pricing Model** — Integrate a trained ML model (e.g., XGBoost/Random Forest) to predict fair market value based on model, year, mileage, and fuel type
- [ ] **Depreciation Calculator** — Interactive tool showing projected value loss over 1–5 years
- [ ] **Comparison Mode** — Side-by-side comparison of two or more models/configurations
- [ ] **Map Visualization** — Geographic distribution of listings (requires location data)
- [ ] **Dark / Light Theme Toggle** — Allow users to switch between dark glassmorphism and a light mode
- [ ] **Database Backend** — Replace CSV with SQLite or PostgreSQL for larger datasets and concurrent access
- [ ] **Authentication** — Add user login for saved filter presets and personalized dashboards
- [x] **Streamlit Cloud Deployment** — Deployed at [appwebui-6z76crdkhzio2ntdgkax36.streamlit.app](https://appwebui-6z76crdkhzio2ntdgkax36.streamlit.app/)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make** your changes and test locally with `streamlit run app1.py`
4. **Commit** with a descriptive message
   ```bash
   git commit -m "Add: amazing feature description"
   ```
5. **Push** to your fork
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open** a Pull Request against `main`

### Contribution Ideas

- Add new chart types (e.g., radar chart for model comparison, box plots by model)
- Improve mobile responsiveness
- Add unit tests for data loading and filtering logic
- Optimize CSS for accessibility (WCAG contrast ratios)
- Expand the dataset with additional columns (e.g., dealer location, listing date)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2026 Arjunan-lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgements

- **Dataset**: Sourced for demonstration and educational purposes from publicly available UK automotive listing data
- **Streamlit**: [streamlit.io](https://streamlit.io/) — the fastest way to build data apps in Python
- **Plotly**: [plotly.com](https://plotly.com/) — interactive graphing library that powers all 13+ visualizations
- **Inter Font**: [Google Fonts](https://fonts.google.com/specimen/Inter) — clean, modern typeface by Rasmus Andersson
- **BMW Logo**: Sourced from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:BMW.svg) (used for educational/demonstration purposes only)

---

<div align="center">

### ⭐ Star this repo if you found it useful!

**BMW Used Car Intelligence** · Built with ❤️ using Streamlit & Plotly

*Made by [Arjunan-lab](https://github.com/Arjunan-lab)*

</div>
