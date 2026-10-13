
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sanofi Pharma Analytics",
    page_icon="💊",
    layout="wide"
)

# =============== PROFESSIONAL DASHBOARD THEME ===============
st.markdown("""
<style>
/* Main application */
.stApp {
    background: #F4F7FB;
    color: #172B4D;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #10243A;
    border-right: 1px solid #203B55;
}

section[data-testid="stSidebar"] * {
    color: #F1F5F9;
}

/* KPI metric cards */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E3EAF3;
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 3px 12px rgba(15, 35, 60, 0.04);
}

div[data-testid="stMetricLabel"] {
    color: #64748B;
    font-size: 0.9rem;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #102A43;
    font-size: 1.8rem;
    font-weight: 700;
}

/* Headings */
h1 {
    color: #102A43 !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2, h3 {
    color: #173B5E !important;
    font-weight: 700 !important;
}

/* Section dividers */
hr {
    border-color: #DCE5EF;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Data tables */
div[data-testid="stDataFrame"] {
    border: 1px solid #E0E8F0;
    border-radius: 12px;
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    border-radius: 9px;
    border: 1px solid #2563EB;
    background: #2563EB;
    color: white;
    font-weight: 600;
    padding: 0.5rem 1rem;
}

.stButton > button:hover {
    background: #1D4ED8;
    border-color: #1D4ED8;
}

/* Multiselect and input fields */
div[data-baseweb="select"] > div {
    border-radius: 9px;
}

/* Hide Streamlit's default branding footer */
footer {
    visibility: hidden;
}

/* Sidebar filter styling */
section[data-testid="stSidebar"] {
    background: #10243A;
}

section[data-testid="stSidebar"] h2 {
    color: #FFFFFF;
    font-weight: 700;
}

section[data-testid="stSidebar"] label {
    font-weight: 600;
}

/* Softer filter corners */
div[data-baseweb="select"] > div {
    border-radius: 10px;
    border: 1px solid #DCE5EF;
}

/* More breathing room between dashboard sections */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.75rem;
}

/* ===== PROFESSIONAL SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10243A 0%, #173B5E 100%);
    border-right: 1px solid #294761;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-weight: 750 !important;
    letter-spacing: -0.3px;
}

/* Labels */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #D7E4F1;
    font-size: 0.9rem;
}

/* Filter widgets */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #FFFFFF;
    border: 1px solid #DCE6F0;
    border-radius: 10px;
    min-height: 44px;
}

/* Selected filter chips */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background: #E5F0FF;
    border: 1px solid #C7DFFF;
    border-radius: 6px;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
    color: #173B5E;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: #FFFFFF;
    color: #173B5E;
    border: 1px solid #DCE6F0;
    border-radius: 9px;
    font-weight: 650;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #E5F0FF;
    color: #10243A;
    border-color: #93C5FD;
}

/* Sidebar dividers */
section[data-testid="stSidebar"] hr {
    border-color: #35516A;
    margin: 1.25rem 0;
}

/* Sidebar help text */
section[data-testid="stSidebar"] .stCaption {
    color: #AFC3D7;
    font-size: 0.8rem;
}

/* Refined sidebar filter controls */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    border: 1px solid #DCE6F0 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
    border-color: #7DD3FC !important;
    box-shadow: 0 0 0 2px rgba(125, 211, 252, 0.18) !important;
}

/* Clear, readable reset button */
section[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF !important;
    color: #173B5E !important;
    border: 1px solid #DCE6F0 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 42px;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #E5F0FF !important;
    color: #10243A !important;
    border-color: #7DD3FC !important;
}


</style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <div style="background: linear-gradient(115deg, #10243A, #174A6E);
                padding: 28px 32px; border-radius: 18px; margin-bottom: 24px;">
        <div style="color: #7DD3FC; font-size: 12px; font-weight: 700;
                    letter-spacing: 2px;">
            PHARMACEUTICAL BUSINESS INTELLIGENCE
        </div>
        <div style="color: white; font-size: 32px; font-weight: 800;
                    margin: 8px 0; line-height: 1.3;">
            Sanofi Analytics
        </div>
        <div style="color: #D6E6F5; font-size: 15px;">
            Sales performance · Product insights · Inventory intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



# 4. Keep your existing KPI metrics below this line
# Example: st.columns(...), st.metric(...)

# 5. Keep your existing filters and charts below


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "pharma_analytics.db"


# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    with sqlite3.connect(DB_PATH) as conn:
        sales = pd.read_sql_query("SELECT * FROM sales", conn)
        products = pd.read_sql_query("SELECT * FROM products", conn)

        inventory = pd.read_sql_query(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='inventory'",
            conn
        )

        if not inventory.empty:
            inventory = pd.read_sql_query(
                "SELECT * FROM inventory", conn
            )
        else:
            inventory = pd.DataFrame()

    sales["sale_date"] = pd.to_datetime(
        sales["sale_date"], errors="coerce"
    )

    return sales, products, inventory


try:
    sales, products, inventory = load_data()
except Exception as e:
    st.error(f"Could not load database: {e}")
    st.stop()

if sales.empty or products.empty:
    st.warning("Your sales or products table is empty.")
    st.stop()

# ---------------- PREPARE SALES ----------------
df = sales.merge(
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
)

df["revenue_inr"] = (
    pd.to_numeric(df["quantity_sold"], errors="coerce")
    * pd.to_numeric(df["unit_price_inr"], errors="coerce")
)

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.markdown("""
<div style="
    padding: 18px 16px;
    margin-bottom: 22px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
">
    <div style="
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #7DD3FC;
    ">SANOFI ANALYTICS</div>
    <div style="
        font-size: 23px;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 7px;
    ">Dashboard Filters</div>
    <div style="
        font-size: 12px;
        color: #C7D7E7;
        margin-top: 5px;
    ">Customize your analysis</div>
</div>
""", unsafe_allow_html=True)


channels = sorted(
    df["sales_channel"].dropna().unique().tolist()
)


selected_channels = st.sidebar.multiselect(
    "Sales channel",
    channels,
    default=channels,
    key="Sales Channel",
)


product_names = sorted(
    products["product_name"].dropna().unique().tolist()
)

selected_products = st.sidebar.multiselect(
    "Products",
    product_names,
    default=product_names,
    key="Products",
)


# ================= DATE RANGE FILTER =================

df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

valid_dates = df["sale_date"].dropna()

if not valid_dates.empty:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    st.sidebar.divider()
    st.sidebar.subheader("📅 Date Range")

    selected_dates = st.sidebar.date_input(
        "Select sales period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="sales_date_range",
    )



# ================= RESET FILTERS =================


def reset_filters():
    st.session_state["Sales Channel"] = channels
    st.session_state["Products"] = product_names
    st.session_state["sales_date_range"] = (
        min_date,
        max_date,
    )

st.sidebar.divider()

st.sidebar.button(
    "↺ Reset All Filters",
    key="reset_all_filters",
    on_click=reset_filters,
    use_container_width=True,
)
# ================= FILTER SALES DATA =================


filtered = df[
    df["sales_channel"].isin(selected_channels)
    & df["product_name"].isin(selected_products)
].copy()

if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered = filtered[
        filtered["sale_date"].dt.date.between(start_date, end_date)
    ]

# ---------------- KPI CARDS ----------------
total_revenue = filtered["revenue_inr"].sum()
total_units = filtered["quantity_sold"].sum()
product_count = filtered["product_id"].nunique()

reorder_count = 0

if not inventory.empty:
    if {
        "closing_stock_units",
        "reorder_level_units"
    }.issubset(inventory.columns):
        reorder_count = (
            inventory["closing_stock_units"]
            <= inventory["reorder_level_units"]
        ).sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Units Sold", f"{total_units:,.0f}")
c3.metric("Products Sold", f"{product_count:,}")
c4.metric("Inventory Reorders", f"{reorder_count:,}")

st.divider()


# ================= ADDITIONAL BUSINESS KPIs =================

average_revenue_per_unit = (
    total_revenue / total_units if total_units > 0 else 0
)

monthly_revenue = (
    filtered.dropna(subset=["sale_date"])
    .assign(
        sales_month=lambda x: x["sale_date"].dt.to_period("M")
    )
    .groupby("sales_month")["revenue_inr"]
    .sum()
    .sort_index()
)

revenue_growth = None

if len(monthly_revenue) >= 2:
    previous_month = monthly_revenue.iloc[-2]
    latest_month = monthly_revenue.iloc[-1]

    if previous_month != 0:
        revenue_growth = (
            (latest_month - previous_month)
            / previous_month
        ) * 100
kpi5, kpi6 = st.columns(2)

with kpi5:
    st.metric(
        "Average Revenue per Unit",
        f"₹{average_revenue_per_unit:,.2f}",
    )


with kpi6:
    if revenue_growth is not None:
        st.metric(
            "Latest Month Revenue Growth",
            f"{revenue_growth:+.1f}%",
            delta=f"{revenue_growth:+.1f}%",
            delta_color="normal",
        )
    else:
        st.metric(
            "Latest Month Revenue Growth",
            "N/A",
        )

# ================= REVENUE TREND =================

st.subheader("📈 Monthly Revenue Trend")

monthly = (
    filtered.dropna(subset=["sale_date"])
    .assign(
        sales_month=lambda x: (
            x["sale_date"].dt.to_period("M").astype(str)
        )
    )
    .groupby("sales_month", as_index=False)["revenue_inr"]
    .sum()
    .sort_values("sales_month")
)

if not monthly.empty:
    fig_monthly = px.line(
        monthly,
        x="sales_month",
        y="revenue_inr",
        markers=True,
        title="Monthly Pharmaceutical Revenue",
        labels={
            "sales_month": "Month",
            "revenue_inr": "Revenue (INR)",
        },
    )

    # Professional chart styling
    fig_monthly.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#334155",
        ),
        title=dict(
            text="Monthly Pharmaceutical Revenue",
            font=dict(size=19, color="#173B5E"),
            x=0.02,
        ),
        margin=dict(l=20, r=20, t=70, b=25),
        hoverlabel=dict(
            bgcolor="#10243A",
            font_size=13,
            font_color="#FFFFFF",
        ),
        xaxis=dict(
            title=None,
            showgrid=False,
            tickangle=-30,
            showline=True,
            linecolor="#E2E8F0",
        ),
        yaxis=dict(
            title="Revenue (INR)",
            showgrid=True,
            gridcolor="#E5EDF5",
            zeroline=False,
            tickformat=",.0f",
        ),
        showlegend=False,
    )

    fig_monthly.update_traces(
        line=dict(color="#2563EB", width=3),
        marker=dict(
            size=7,
            color="#0D9488",
            line=dict(width=1, color="#FFFFFF"),
        ),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: ₹%{y:,.0f}"
            "<extra></extra>"
        ),
    )

    st.plotly_chart(fig_monthly, width="stretch")

else:
    st.info("No valid sales dates are available.")



# ================= MONTHLY REVENUE GROWTH =================


st.subheader("📈 Monthly Revenue Growth (%)")

if len(monthly_revenue) >= 2:
    growth_data = monthly_revenue.pct_change().mul(100).dropna()

    growth_df = growth_data.rename("growth_pct").reset_index()
    growth_df.columns = ["sales_month", "growth_pct"]

    # Convert Period values to strings for Plotly compatibility
    growth_df["sales_month"] = growth_df["sales_month"].astype(str)

    fig_growth = px.bar(
        growth_df,
        x="sales_month",
        y="growth_pct",
        title="Month-over-Month Revenue Growth",
        labels={
            "sales_month": "Month",
            "growth_pct": "Growth (%)",
        },
    )

    fig_growth.update_layout(
        template="plotly_white",
        yaxis_title="Revenue Growth (%)",
        xaxis_title="Month",
    )

    st.plotly_chart(
        fig_growth,
        width="stretch",
        key="monthly_revenue_growth_chart",
    )
else:
    st.info("Select a date range containing at least two months.")



# ================= PRODUCT AND CHANNEL ANALYSIS =================

left, right = st.columns(2)

with left:
    st.subheader("🏆 Revenue by Product")

    product_revenue = (
        filtered.groupby("product_name", as_index=False)["revenue_inr"]
        .sum()
        .sort_values("revenue_inr", ascending=False)
    )

    fig_product = px.bar(
        product_revenue.head(10),
        x="revenue_inr",
        y="product_name",
        orientation="h",
        title="Top 10 Products by Revenue",
        labels={
            "revenue_inr": "Revenue (INR)",
            "product_name": "Product",
        },
    )

    fig_product.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#334155",
        ),
        title=dict(
            font=dict(size=18, color="#173B5E"),
            x=0.02,
        ),
        margin=dict(l=20, r=25, t=65, b=25),
        hoverlabel=dict(
            bgcolor="#10243A",
            font_size=13,
            font_color="white",
        ),
        xaxis=dict(
            title="Revenue (INR)",
            showgrid=True,
            gridcolor="#E5EDF5",
            tickformat=",.0f",
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            categoryorder="total ascending",
        ),
    )

    fig_product.update_traces(
        marker_color="#2563EB",
        hovertemplate=(
            "Product: %{y}<br>"
            "Revenue: ₹%{x:,.0f}"
            "<extra></extra>"
        ),
    )

    st.plotly_chart(
        fig_product,
        width="stretch",
        key="product_revenue_chart",
    )

with right:
    st.subheader("💊 Revenue by Sales Channel")

    channel_revenue = (
        filtered.groupby("sales_channel", as_index=False)["revenue_inr"]
        .sum()
        .sort_values("revenue_inr", ascending=False)
    )

    fig_channel = px.bar(
        channel_revenue,
        x="sales_channel",
        y="revenue_inr",
        title="Channel Performance",
        labels={
            "sales_channel": "Sales Channel",
            "revenue_inr": "Revenue (INR)",
        },
    )

    fig_channel.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#334155",
        ),
        title=dict(
            font=dict(size=18, color="#173B5E"),
            x=0.02,
        ),
        margin=dict(l=20, r=25, t=65, b=25),
        hoverlabel=dict(
            bgcolor="#10243A",
            font_size=13,
            font_color="white",
        ),
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(
            title="Revenue (INR)",
            showgrid=True,
            gridcolor="#E5EDF5",
            tickformat=",.0f",
        ),
    )

    fig_channel.update_traces(
        marker_color="#0D9488",
        hovertemplate=(
            "Channel: %{x}<br>"
            "Revenue: ₹%{y:,.0f}"
            "<extra></extra>"
        ),
    )

    st.plotly_chart(
        fig_channel,
        width="stretch",
        key="sales_channel_revenue_chart",
    )

# ================= BUSINESS INSIGHTS =================

st.divider()
st.subheader("💡 Business Insights")

if not filtered.empty:
    total_revenue = filtered["revenue_inr"].sum()

    top_product = (
        filtered.groupby("product_name")["revenue_inr"]
        .sum()
        .idxmax()
    )

    top_channel = (
        filtered.groupby("sales_channel")["revenue_inr"]
        .sum()
        .idxmax()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"🏆 **Top Revenue Product:** {top_product}"
        )

    with col2:
        st.info(
            f"📊 **Leading Sales Channel:** {top_channel}"
        )

    st.caption(
        f"Total revenue across the current filters: ₹{total_revenue:,.0f}"
    )
else:
    st.info("No sales data matches the selected filters.")

# ================= DOWNLOAD SALES REPORT =================

st.divider()
st.subheader("📥 Export Sales Report")

if not filtered.empty:
    csv_data = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Sales Data (CSV)",
        data=csv_data,
        file_name="sanofi_filtered_sales_report.csv",
        mime="text/csv",
        key="download_sales_report",
        width="stretch",
    )
else:
    st.info("No sales data available to export.")


# ---------------- INVENTORY ALERTS ----------------
st.divider()
st.subheader("⚠️ Inventory Risk Monitoring")

if inventory.empty:
    st.warning(
        "Inventory table not found. Run your data preparation "
        "script to load inventory into SQLite."
    )
else:
    required = {
        "product_id",
        "closing_stock_units",
        "reorder_level_units"
    }

    if required.issubset(inventory.columns):
        stock = inventory.merge(
            products[["product_id", "product_name"]],
            on="product_id",
            how="left",
            validate="many_to_one"
        )

        stock["inventory_status"] = (
            stock["closing_stock_units"]
            <= stock["reorder_level_units"]
        ).map({
            True: "Reorder Required",
            False: "Stock Available"
        })

        alerts = stock[
            stock["inventory_status"] == "Reorder Required"
        ].sort_values("closing_stock_units")

        if alerts.empty:
            st.success("No medicines currently require reordering.")
        else:
            st.warning(
                f"{len(alerts)} inventory record(s) require attention."
            )
            st.dataframe(
                alerts[
                    [
                        "product_name",
                        "closing_stock_units",
                        "reorder_level_units",
                        "inventory_status"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        fig_stock = px.bar(
            stock,
            x="product_name",
            y="closing_stock_units",
            color="inventory_status",
            barmode="group",
            title="Closing Stock vs Reorder Risk",
            labels={
                "product_name": "Medicine",
                "closing_stock_units": "Closing Stock (Units)",
                "inventory_status": "Stock Status"
            },
            color_discrete_map={
                "Reorder Required": "#E74C3C",
                "Stock Available": "#27AE60"
            }
        )
        st.plotly_chart(fig_stock, use_container_width=True)
    else:
        st.warning(
            "Inventory columns do not match the expected schema. "
            "Check your inventory table before displaying alerts."
        )

# ---------------- DATA TABLE ----------------
with st.expander("View filtered sales data"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

st.caption("Analytics dashboard | Built with Python, SQL, Pandas, Streamlit and Plotly")
