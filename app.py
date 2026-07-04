import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Billionaire Wealth Analytics",
    page_icon="💰",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/billionaires_clean.csv")
    return df

df = load_data()
df["Continent"] = df["Continent"].replace({"Australia": "Oceania"})
df_original = df.copy()

# ---- Sidebar CSS + header ----
st.sidebar.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E5E7EB;
    }
    [data-testid="stSidebar"] h2 {
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #374151;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🎛️ Filters")
st.sidebar.markdown(
    "<p style='color:#9CA3AF; font-size:13px; margin-top:-8px;'>Narrow the view — every chart updates live</p>",
    unsafe_allow_html=True
)
st.sidebar.divider()

# ---- Sidebar widgets ----
year_range = st.sidebar.slider(
    "Year range",
    min_value=int(df.Year.min()),
    max_value=int(df.Year.max()),
    value=(int(df.Year.min()), int(df.Year.max())),
)

st.sidebar.divider()

continents = sorted(df.Continent.dropna().unique())
selected_continents = st.sidebar.multiselect(
    "Continent",
    options=continents,
    default=continents,
)

gender_options = ["All"] + sorted(df.Gender.dropna().unique().tolist())
selected_gender = st.sidebar.selectbox(
    "Gender",
    options=gender_options,
    index=0,
)

# ---- Apply filters ONCE ----
# df_for_kpis: year + continent only (used by KPIs and the gender chart,
# which both need BOTH genders present to compute ratios/comparisons)
df_for_kpis = df_original[
    (df_original.Year >= year_range[0]) &
    (df_original.Year <= year_range[1]) &
    (df_original.Continent.isin(selected_continents))
]

# df: the fully filtered version (year + continent + gender), used by
# every chart that doesn't specifically need both genders present
df = df[
    (df.Year >= year_range[0]) &
    (df.Year <= year_range[1]) &
    (df.Continent.isin(selected_continents))
]
if selected_gender != "All":
    df = df[df.Gender == selected_gender]

# ---- Custom CSS for polished KPI cards ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #14213D;
    }

    .kpi-card {
        background: linear-gradient(135deg, #1B2A4A 0%, #22345C 100%);
        border-radius: 14px;
        padding: 22px 26px;
        min-height: 130px;
        box-shadow: 0 4px 12px rgba(20,33,61,0.2);
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #A9B8D1;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 34px;
        font-weight: 700;
        font-family: 'Playfair Display', serif;
        color: #FAF9F7;
        line-height: 1.2;
    }
    .kpi-delta-positive {
        font-size: 13px;
        font-weight: 700;
        color: #E08E52;
        margin-top: 6px;
    }
    .kpi-delta-negative {
        font-size: 13px;
        font-weight: 700;
        color: #F3C9A0;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown("## The Anatomy of Billionaire Wealth")
st.markdown(
    "<p style='color:#6B7280; font-size:15px; margin-top:-10px;'>"
    "25 years of Forbes billionaire data, 2001–2026 — including history's first trillionaire</p>",
    unsafe_allow_html=True
)
st.write("")

# ---- KPI calculations (uses df_for_kpis so gender filter doesn't break these) ----
latest_year = df_for_kpis.Year.max()
prev_year = latest_year - 1
latest = df_for_kpis[df_for_kpis.Year == latest_year]
prev = df_for_kpis[df_for_kpis.Year == prev_year]

total_wealth = latest["NetWorth_USD_B"].sum() / 1000
prev_wealth = prev["NetWorth_USD_B"].sum() / 1000
wealth_change_pct = (total_wealth - prev_wealth) / prev_wealth * 100 if prev_wealth else 0

total_count = len(latest)
prev_count = len(prev)
count_change = total_count - prev_count

richest = latest.nlargest(1, "NetWorth_USD_B").iloc[0]

pct_women = (latest.Gender == "Female").sum() / latest.Gender.notna().sum() * 100 if latest.Gender.notna().sum() else 0
prev_women_denom = prev.Gender.notna().sum()
prev_pct_women = (prev.Gender == "Female").sum() / prev_women_denom * 100 if prev_women_denom else 0
pct_women_change = pct_women - prev_pct_women if prev_women_denom else None

def kpi_card(label, value, delta=None, positive=True):
    delta_html = ""
    if delta:
        cls = "kpi-delta-positive" if positive else "kpi-delta-negative"
        arrow = "↑" if positive else "↓"
        delta_html = f'<div class="{cls}">{arrow} {delta}</div>'
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(kpi_card("Total Wealth", f"${total_wealth:.2f}T", f"{wealth_change_pct:+.1f}% vs {prev_year}"), unsafe_allow_html=True)
with col2:
    st.markdown(kpi_card("Billionaire Count", f"{total_count:,}", f"{count_change:+,} vs {prev_year}"), unsafe_allow_html=True)
with col3:
    st.markdown(kpi_card("Richest Person", richest["Name"], f"${richest['NetWorth_USD_B']:.0f}B"), unsafe_allow_html=True)
with col4:
    if pct_women_change is not None:
        women_delta = f"{pct_women_change:+.1f} pts vs {prev_year}"
    else:
        women_delta = f"No gender data for {prev_year}"
    st.markdown(kpi_card("Women on the List", f"{pct_women:.1f}%", women_delta, positive=(pct_women_change is not None and pct_women_change >= 0)), unsafe_allow_html=True)

st.write("")

# ---- Data preview, tucked away instead of dominating the page ----
with st.expander("🔍 View raw data sample"):
    st.dataframe(df.head(20))

# =========================================================
# CHART 1 — Tech Takeover
# =========================================================
st.write("")
st.markdown("### The Tech Takeover: 25 Years in the Making")
st.markdown(
    "<p style='color:#6B7280; font-size:14px;'>"
    "For 25 straight years, old-money Consumer industries — retail, consumer goods, auto — "
    "held the #1 spot in billionaire wealth. In 2026, that changed for the first time.</p>",
    unsafe_allow_html=True
)

industry_trend = (
    df.groupby(["Year", "Industry_Broad"])["NetWorth_USD_B"]
    .sum()
    .reset_index()
)
yearly_totals = df.groupby("Year")["NetWorth_USD_B"].sum().reset_index(name="TotalWealth")
industry_trend = industry_trend.merge(yearly_totals, on="Year")
industry_trend["Share"] = industry_trend["NetWorth_USD_B"] / industry_trend["TotalWealth"] * 100

focus_industries = ["Information Technology", "Consumer", "Financials"]
plot_data = industry_trend[industry_trend.Industry_Broad.isin(focus_industries)]

fig = px.line(
    plot_data,
    x="Year",
    y="Share",
    color="Industry_Broad",
    color_discrete_map={
        "Information Technology": "#C1652B",
        "Consumer": "#14213D",
        "Financials": "#A9B8D1",
    },
    labels={"Share": "Share of Total Wealth (%)", "Industry_Broad": "Industry"},
    markers=True,
)

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_family="Source Sans 3, sans-serif",
    legend_title_text="",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.05, x=0, font=dict(size=11)),
)

fig.add_annotation(
    x=2026, y=26.8,
    text="Tech overtakes Consumer<br>for the first time",
    showarrow=True,
    arrowhead=2,
    ax=-100, ay=-70,
    font=dict(size=12, color="#C1652B"),
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# CHART 2 — Gender story (always uses BOTH genders, ignores gender filter)
# =========================================================
st.write("")
st.markdown("### The Real Gender Story: It's Not About How Much")
st.markdown(
    "<p style='color:#6B7280; font-size:14px;'>"
    "Female billionaires have matched or exceeded male billionaires in median wealth every year. "
    "The real gap is who gets on the list at all.</p>",
    unsafe_allow_html=True
)

gender_df = df_for_kpis.dropna(subset=["Gender"])

gender_yearly = gender_df.groupby(["Year", "Gender"]).agg(
    median_worth=("NetWorth_USD_B", "median"),
    count=("Name", "count"),
).reset_index()

pivot = gender_yearly.pivot(index="Year", columns="Gender", values=["median_worth", "count"])
pivot["pct_women"] = pivot[("count", "Female")] / (pivot[("count", "Female")] + pivot[("count", "Male")]) * 100
pivot["wealth_ratio"] = pivot[("median_worth", "Female")] / pivot[("median_worth", "Male")]
pivot = pivot.reset_index()

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Scatter(
        x=pivot["Year"], y=pivot["pct_women"],
        name="% of billionaires who are women",
        line=dict(color="#C1652B", width=3),
        mode="lines+markers",
    ),
    secondary_y=False,
)

fig2.add_trace(
    go.Scatter(
        x=pivot["Year"], y=pivot["wealth_ratio"],
        name="Female-to-male median wealth ratio",
        line=dict(color="#14213D", width=2, dash="dot"),
        mode="lines+markers",
    ),
    secondary_y=True,
)

fig2.add_hline(y=1.0, line_dash="dash", line_color="#D1D5DB", secondary_y=True)

fig2.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_family="Source Sans 3, sans-serif",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.05, x=0, font=dict(size=11)),
)
fig2.update_yaxes(title_text="% of billionaires who are women", secondary_y=False)
fig2.update_yaxes(title_text="Wealth ratio (1.0 = equal)", secondary_y=True)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# CHART 3 — Geography
# =========================================================
st.write("")
st.markdown("### The Geography of Wealth: A Story of Rebound")
st.markdown(
    "<p style='color:#6B7280; font-size:14px;'>"
    "The US share of global billionaire wealth fell for nearly two decades, while China rose. "
    "Then the AI boom — and one trillionaire — flipped it back.</p>",
    unsafe_allow_html=True
)

country_trend = (
    df.groupby(["Year", "Citizenship"])["NetWorth_USD_B"]
    .sum()
    .reset_index()
    .merge(yearly_totals, on="Year")
)
country_trend["Share"] = country_trend["NetWorth_USD_B"] / country_trend["TotalWealth"] * 100

focus_countries = ["United States", "China"]
geo_plot = country_trend[country_trend.Citizenship.isin(focus_countries)]

fig3 = px.line(
    geo_plot,
    x="Year",
    y="Share",
    color="Citizenship",
    color_discrete_map={"United States": "#14213D", "China": "#C1652B"},
    labels={"Share": "Share of Total Wealth (%)", "Citizenship": "Country"},
    markers=True,
)

fig3.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_family="Source Sans 3, sans-serif",
    legend_title_text="",
    hovermode="x unified",
)

fig3.add_vline(x=2020, line_dash="dash", line_color="#D1D5DB")
fig3.add_annotation(
    x=2020, y=50,
    text="China peaks<br>then reverses",
    showarrow=False,
    font=dict(size=11, color="#6B7280"),
)

st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# CHART 4 — Crisis barometer
# =========================================================
st.write("")
st.markdown("### Billionaire Count as a Crisis Barometer")
st.markdown(
    "<p style='color:#6B7280; font-size:14px;'>"
    "The number of billionaires in the world isn't just a headcount — it tracks financial crises in real time.</p>",
    unsafe_allow_html=True
)

count_by_year = df.groupby("Year").size().reset_index(name="Count")

fig4 = px.line(
    count_by_year,
    x="Year",
    y="Count",
    markers=True,
)

fig4.update_traces(line=dict(color="#14213D", width=2.5))

fig4.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_family="Source Sans 3, sans-serif",
    yaxis_title="Number of Billionaires",
)

fig4.add_vrect(
    x0=2008, x1=2009,
    fillcolor="#F3C9A0", opacity=0.6, line_width=0,
    annotation_text="2008 crash", annotation_position="top left",
    annotation=dict(font_size=11, font_color="#C1652B"),
)
fig4.add_vrect(
    x0=2020, x1=2021,
    fillcolor="#A9B8D1", opacity=0.5, line_width=0,
    annotation_text="COVID rebound", annotation_position="top left",
    annotation=dict(font_size=11, font_color="#14213D"),
)

st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# Footer
# =========================================================
st.write("")
st.divider()

with st.expander("📋 Methodology & Known Limitations"):
    st.markdown("""
    **Data sources**
    - 2001–2023: Forbes World's Billionaires archive (academic Pareto-law research dataset)
    - 2024–2025: Forbes World's Billionaires official annual lists
    - 2026: Live snapshot from Forbes' real-time billionaires tracker, pulled July 3, 2026

    **Known limitations**
    - 2024–2026 wealth/demographic data comes from a live real-time tracker (not an official annual snapshot), so counts run slightly below Forbes' official published totals for those years (e.g. 2026: 3,381 vs. official 3,428). Age/Gender coverage for these years is 97-100%, consistent with the rest of the dataset.
    - The 2026 figures come from a live tracker, not an official annual snapshot, so its count (3,381) doesn't exactly match Forbes' official March 2026 count (3,428). Treat 2026 as directionally accurate, not perfectly comparable to prior years.
    - Industry categories were standardized across two different taxonomies Forbes has used over 25 years (see `Industry_Broad` column) — some nuance is lost in that mapping.
    - 4 multi-person family entries (e.g. sibling groups) were left in their original format since they don't fit a standard single-person name structure.

    **Why this matters**: these aren't hidden — they're documented so the numbers can be trusted for what they actually show, not overstated.
    """)

st.markdown(
    "<p style='color:#9CA3AF; font-size:12px; text-align:center; margin-top:20px;'>"
    "Built by Haneen · Data: Forbes World's Billionaires, 2001–2026</p>",
    unsafe_allow_html=True
)