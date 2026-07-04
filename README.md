# 💰 The Anatomy of Billionaire Wealth

An interactive dashboard analyzing 25 years (2001–2026) of Forbes World's Billionaires data — built end-to-end with Python, Pandas, and Streamlit, including a live snapshot capturing the moment history's first trillionaire emerged.

**[🔗 View Live Dashboard](https://billionaire-wealth-dashboard.streamlit.app/)**

**[🎥 Watch Walkthrough Demo](https://drive.google.com/file/d/11EvqmR3gmlh78lifJnuHlRNmAqAYfBvK/view?usp=sharing)**

---

## 📊 Key Findings

- **Tech dethroned old-money wealth for the first time in 25 years.** Consumer industries (retail, auto, consumer goods) held the #1 spot in billionaire wealth every single year from 2001–2025. In 2026, Technology overtook it — 26.8% vs. 20.2% of total wealth.
- **The gender gap isn't about wealth amount — it's about access.** Female billionaires have matched or exceeded male billionaires in median net worth every year since 2010. The real gap: women are still only 13.8% of the list.
- **The US "lost," then abruptly "won back" global wealth dominance.** US share of global billionaire wealth fell from 52.5% (2001) to ~36% (2015–2023), then rebounded to 43.7% in 2026 — driven largely by a single event.
- **One person now holds ~5% of all billionaire wealth on Earth.** SpaceX's June 2026 IPO made Elon Musk history's first trillionaire, at roughly $997B.
- **Billionaire count is a real-time barometer of financial crises** — visible drops during the 2008 crash and sharp rebounds following COVID-era stimulus.

---

## 🗂️ Data Sources

| Years | Source |
|---|---|
| 2001–2023 | Forbes World's Billionaires archive (academic Pareto-law research dataset) |
| 2024–2026 | Live snapshots from Forbes' real-time billionaires tracker |

Full data transparency — including known limitations and methodology decisions — is documented directly in the app's **"Methodology & Known Limitations"** section.

---

## 🛠️ Tech Stack

- **Python** & **Pandas** — data cleaning, reshaping (wide-to-long transformation), and feature engineering
- **Streamlit** — dashboard framework and interactivity (filters, KPI cards)
- **Plotly** — interactive, annotated charts

---

## 🚀 Run It Locally

```bash
git clone https://github.com/HaneenAyman23/billionaire-wealth-dashboard.git
cd billionaire-wealth-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
billionaire-wealth-dashboard/
├── app.py                       # Main Streamlit app
├── requirements.txt             # Python dependencies
├── .streamlit/
│   └── config.toml       # Theme configuration
├── data/
│   └── billionaires_clean.csv   # Cleaned, reshaped dataset (2001–2026)
└── README.md
```

---

Built by **Haneen Ayman**
