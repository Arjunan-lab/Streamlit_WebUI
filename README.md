# 🏎️ BMW Used Car Intelligence Dashboard

A sleek, interactive analytics dashboard built with **Streamlit** and **Plotly** for exploring BMW used car listings. Features a glassmorphism UI with BMW brand styling, real-time filtering, and rich visualizations across 10,000+ vehicle records.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Features at a Glance

| Feature | Description |
|---------|-------------|
| **KPI Cards** | Average price, mileage, MPG, and engine size at a glance |
| **Dynamic Filters** | Sidebar controls for year, fuel type, transmission, price range, and model |
| **4 Analytics Tabs** | Overview · Pricing Deep-Dive · Inventory Mix · Data Explorer |
| **10+ Chart Types** | Bar, pie/donut, line, scatter, violin, heatmap, treemap, sunburst, histogram, bubble |
| **Dark Glassmorphism UI** | Custom CSS with BMW brand palette, glass-card effects, and responsive layout |
| **CSV Export** | Download filtered dataset directly from the app |

---

## 🗂️ Project Structure

```
├── app1.py              # Main Streamlit dashboard application
├── bmw.csv              # Dataset — 10,000+ BMW used car listings
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 📊 Dataset

The dataset (`bmw.csv`) contains **10,782 BMW used car listings** with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `model` | string | BMW model name (e.g., 1 Series, 3 Series, X5) |
| `year` | int | Year of registration |
| `price` | int | Listing price in GBP (£) |
| `transmission` | string | Gearbox type (Automatic, Manual, Semi-Auto) |
| `mileage` | int | Odometer reading in miles |
| `fuelType` | string | Fuel type (Petrol, Diesel, Hybrid, Electric, Other) |
| `tax` | int | Annual road tax in GBP (£) |
| `mpg` | float | Miles per gallon (fuel efficiency) |
| `engineSize` | float | Engine displacement in litres |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Arjunan-lab/Streamlit_WebUI.git
   cd Streamlit_WebUI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run app1.py
   ```

4. Open your browser at **http://localhost:8501**

---

## 🖥️ Dashboard Walkthrough

### 🎛️ Sidebar Filters
Interactive controls to slice the data by:
- **Model Year** — range slider
- **Fuel Type** — multi-select
- **Transmission** — multi-select
- **Price Range** — range slider (£)
- **Model** — optional multi-select (leave blank for all)

### 📊 Tab 1 — Overview
- **Fuel Type Breakdown** — color-coded bar chart of listing counts
- **Transmission Split** — donut chart showing gearbox proportions
- **Average Price Trajectory** — spline line chart with area fill showing year-over-year trends

### 💰 Tab 2 — Pricing Deep-Dive
- **Price vs Mileage** — scatter plot sized by engine capacity, colored by fuel type
- **Mileage Distribution** — histogram with marginal box plot
- **Price Distribution by Fuel Type** — violin plot with quartile boxes
- **Year × Fuel Type Heatmap** — average price matrix to spot value pockets

### 🏗️ Tab 3 — Inventory Mix
- **Top 12 Models by Volume** — horizontal bar ranking
- **Engine Size Split** — donut chart of engine capacities
- **Model × Transmission Treemap** — proportional area map of listing density
- **Sunburst Chart** — hierarchical drill-down: Fuel → Transmission → Engine
- **MPG vs Tax Bubble Chart** — efficiency matrix sized by listing count

### 📋 Tab 4 — Data Explorer
- **Sortable Data Table** — full filtered dataset with all columns
- **CSV Download** — one-click export of filtered records
- **Summary Statistics** — descriptive stats (mean, std, min, max, quartiles)

---

## 🎨 Design Highlights

- **Glassmorphism UI** — translucent cards with `backdrop-filter: blur()`, subtle borders, and hover animations
- **BMW Brand Palette** — BMW Blue (`#1C69D4`), dark backgrounds, and accent colors (cyan, green, amber, rose)
- **Inter Font** — clean, modern typography loaded from Google Fonts
- **Responsive Layout** — KPI grid adapts from 4 columns to 2 on smaller screens
- **Plotly Dark Theme** — all charts use a unified dark template with transparent backgrounds

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [Streamlit](https://streamlit.io/) | Web framework & UI components |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive chart library |
| [Plotly Graph Objects](https://plotly.com/python/graph-objects/) | Advanced chart customization |
| [Pandas](https://pandas.pydata.org/) | Data loading, filtering & aggregation |
| [NumPy](https://numpy.org/) | Numerical operations |

---

## 📦 Dependencies

```
streamlit
pandas
plotly
numpy
```

Install all at once:
```bash
pip install streamlit pandas plotly numpy
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- Dataset sourced for demonstration and educational purposes
- Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/)

---

<p align="center">
  <b>BMW Used Car Intelligence</b> · Built with ❤️ using Streamlit & Plotly
</p>
