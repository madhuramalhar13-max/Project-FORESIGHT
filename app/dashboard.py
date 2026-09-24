import streamlit as st
import pandas as pd
import os


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Project FORESIGHT",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* =========================================
       GLOBAL BACKGROUND
       ========================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(91, 33, 182, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(37, 99, 235, 0.15),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #050816 0%,
                #07101f 45%,
                #050816 100%
            );

        color: #F8FAFC;
    }


    /* =========================================
       MAIN CONTENT
       ========================================= */

    .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* =========================================
       SIDEBAR
       ========================================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #080D1D 0%,
                #0B1224 50%,
                #080D1D 100%
            );

        border-right: 1px solid rgba(139, 92, 246, 0.25);
    }


    section[data-testid="stSidebar"] h2 {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 1px;
    }


    section[data-testid="stSidebar"] p {
        color: #94A3B8;
    }


    /* =========================================
       TITLE
       ========================================= */

    .title {
        font-size: 46px;
        font-weight: 800;
        letter-spacing: -1px;

        background:
            linear-gradient(
                90deg,
                #FFFFFF,
                #C4B5FD,
                #60A5FA
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin-bottom: 5px;
    }


    .subtitle {
        font-size: 18px;
        color: #94A3B8;
        letter-spacing: 0.3px;
        margin-bottom: 25px;
    }


    /* =========================================
       SECTION TITLES
       ========================================= */

    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 20px;
        margin-bottom: 18px;
    }


    /* =========================================
       METRIC CARDS
       ========================================= */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(17, 24, 39, 0.95),
                rgba(15, 23, 42, 0.80)
            );

        border: 1px solid rgba(139, 92, 246, 0.20);

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 0 25px rgba(76, 29, 149, 0.10),
            inset 0 1px 0 rgba(255,255,255,0.04);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    div[data-testid="stMetric"]:hover {

        transform: translateY(-3px);

        box-shadow:
            0 0 30px rgba(139, 92, 246, 0.25),
            inset 0 1px 0 rgba(255,255,255,0.08);
    }


    div[data-testid="stMetricLabel"] {

        color: #94A3B8 !important;

        font-size: 13px;

        font-weight: 600;

        text-transform: uppercase;

        letter-spacing: 0.7px;
    }


    div[data-testid="stMetricValue"] {

        color: #FFFFFF !important;

        font-size: 32px !important;

        font-weight: 750 !important;
    }


    /* =========================================
       SELECT BOX
       ========================================= */

    div[data-baseweb="select"] > div {

        background-color: #0B1224;

        border: 1px solid rgba(139, 92, 246, 0.35);

        border-radius: 12px;
    }


    div[data-baseweb="select"] > div:hover {

        border-color: #8B5CF6;

        box-shadow:
            0 0 15px rgba(139, 92, 246, 0.20);
    }


    /* =========================================
       DATAFRAME
       ========================================= */

    div[data-testid="stDataFrame"] {

        border-radius: 16px;

        overflow: hidden;

        border: 1px solid rgba(139, 92, 246, 0.20);

        box-shadow:
            0 0 25px rgba(15, 23, 42, 0.5);
    }


    /* =========================================
       CHART CONTAINERS
       ========================================= */

    div[data-testid="stVegaLiteChart"] {

        background:
            linear-gradient(
                145deg,
                rgba(11, 18, 36, 0.90),
                rgba(15, 23, 42, 0.75)
            );

        border: 1px solid rgba(96, 165, 250, 0.18);

        border-radius: 18px;

        padding: 10px;

        box-shadow:
            0 0 25px rgba(37, 99, 235, 0.08);
    }


    /* =========================================
       BUTTONS
       ========================================= */

    .stButton > button {

        background:
            linear-gradient(
                90deg,
                #7C3AED,
                #2563EB
            );

        color: white;

        border: none;

        border-radius: 12px;

        padding: 10px 20px;

        font-weight: 700;

        box-shadow:
            0 0 20px rgba(124, 58, 237, 0.25);

        transition: all 0.2s ease;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 0 30px rgba(124, 58, 237, 0.45);
    }


    /* =========================================
       ALERT BOXES
       ========================================= */

    div[data-testid="stAlert"] {

        border-radius: 14px;

        border: 1px solid rgba(255,255,255,0.08);
    }


    /* =========================================
       DIVIDERS
       ========================================= */

    hr {

        border: none;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(139,92,246,0.35),
                rgba(96,165,250,0.35),
                transparent
            );

        margin-top: 25px;

        margin-bottom: 25px;
    }


    /* =========================================
       FOOTER
       ========================================= */

    .footer {

        text-align: center;

        color: #64748B;

        font-size: 13px;

        padding: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# FILE PATHS
# ==================================================

RISK_FILE = "data/processed/inventory_risk.csv"
FORECAST_FILE = "data/processed/weekly_forecasts.csv"


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_risk_data():

    if not os.path.exists(RISK_FILE):
        return None

    return pd.read_csv(RISK_FILE)


@st.cache_data
def load_forecast_data():

    if not os.path.exists(FORECAST_FILE):
        return None

    return pd.read_csv(FORECAST_FILE)


risk_df = load_risk_data()
forecast_df = load_forecast_data()


# ==================================================
# CHECK DATA
# ==================================================

if risk_df is None:

    st.error(
        "Inventory risk data not found. "
        "Please run the pipeline first."
    )

    st.stop()


if forecast_df is None:

    st.error(
        "Forecast data not found. "
        "Please run the pipeline first."
    )

    st.stop()


# ==================================================
# KPI CALCULATIONS
# ==================================================

total_skus = len(risk_df)


high_risk = len(
    risk_df[
        risk_df["Overall_Risk"] == "HIGH"
    ]
)


stockout_risk = len(
    risk_df[
        risk_df["Stockout_Risk"] == "HIGH"
    ]
)


overstock_risk = len(
    risk_df[
        risk_df["Overstock_Risk"] == "HIGH"
    ]
)


reorder_now = len(
    risk_df[
        risk_df["Recommendation"] == "REORDER NOW"
    ]
)


reorder_soon = len(
    risk_df[
        risk_df["Recommendation"] == "REORDER SOON"
    ]
)


markdown_clear = len(
    risk_df[
        risk_df["Recommendation"] == "MARKDOWN / CLEAR"
    ]
)


healthy = len(
    risk_df[
        risk_df["Recommendation"] == "HEALTHY"
    ]
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:20px 5px;
        ">

        <div style="
            font-size:42px;
            margin-bottom:5px;
        ">
        🚀
        </div>

        <div style="
            font-size:25px;
            font-weight:800;
            letter-spacing:2px;
            color:#FFFFFF;
        ">
        FORESIGHT
        </div>

        <div style="
            font-size:12px;
            color:#8B5CF6;
            letter-spacing:1px;
            margin-top:5px;
        ">
        INVENTORY INTELLIGENCE
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")


    st.markdown(
        "### Navigation"
    )


    page = st.radio(
        "Navigate",
        [
            "Executive Dashboard",
            "SKU Intelligence",
            "Action Center"
        ],
        label_visibility="collapsed"
    )


    st.markdown("---")


    st.markdown(
        """
        <div style="
            padding:15px;
            border-radius:14px;
            background:rgba(139,92,246,0.08);
            border:1px solid rgba(139,92,246,0.18);
        ">

        <div style="
            color:#A78BFA;
            font-size:12px;
            font-weight:700;
        ">
        SYSTEM STATUS
        </div>

        <div style="
            margin-top:8px;
            color:#CBD5E1;
            font-size:13px;
        ">
        🟢 Forecast Engine Online
        </div>

        <div style="
            margin-top:5px;
            color:#CBD5E1;
            font-size:13px;
        ">
        🟢 Risk Engine Online
        </div>

        <div style="
            margin-top:5px;
            color:#CBD5E1;
            font-size:13px;
        ">
        🟢 API Connected
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# PAGE 1 — EXECUTIVE DASHBOARD
# ==================================================

if page == "Executive Dashboard":

    st.markdown(
        '<div class="title">🚀 Project FORESIGHT</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="subtitle">'
        'AI-Powered Demand & Inventory Intelligence Platform'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown("---")


    # ----------------------------------------------
    # KPI CARDS
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📊 Inventory Overview'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total SKUs",
            f"{total_skus:,}"
        )


    with col2:

        st.metric(
            "🔴 High Risk",
            f"{high_risk:,}"
        )


    with col3:

        st.metric(
            "⚠️ Stockout Risk",
            f"{stockout_risk:,}"
        )


    with col4:

        st.metric(
            "📦 Overstock Risk",
            f"{overstock_risk:,}"
        )


    st.markdown("---")


    # ----------------------------------------------
    # ACTION METRICS
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🎯 Recommended Actions'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🔴 Reorder Now",
            f"{reorder_now:,}"
        )


    with col2:

        st.metric(
            "🟡 Reorder Soon",
            f"{reorder_soon:,}"
        )


    with col3:

        st.metric(
            "🏷️ Markdown / Clear",
            f"{markdown_clear:,}"
        )


    with col4:

        st.metric(
            "🟢 Healthy",
            f"{healthy:,}"
        )


    st.markdown("---")


    # ----------------------------------------------
    # CHARTS
    # ----------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            "### ⚠️ Risk Distribution"
        )


        risk_chart = pd.DataFrame(
            {
                "Category": [
                    "High Risk",
                    "Stockout",
                    "Overstock",
                    "Healthy"
                ],

                "SKUs": [
                    high_risk,
                    stockout_risk,
                    overstock_risk,
                    healthy
                ]
            }
        )


        st.bar_chart(
            risk_chart.set_index("Category")
        )


    with col2:

        st.markdown(
            "### 🎯 Action Distribution"
        )


        action_chart = pd.DataFrame(
            {
                "Action": [
                    "Reorder Now",
                    "Reorder Soon",
                    "Markdown / Clear",
                    "Healthy"
                ],

                "SKUs": [
                    reorder_now,
                    reorder_soon,
                    markdown_clear,
                    healthy
                ]
            }
        )


        st.bar_chart(
            action_chart.set_index("Action")
        )


    st.markdown("---")


    # ----------------------------------------------
    # HIGH RISK PRODUCTS
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🚨 Products Requiring Attention'
        '</div>',
        unsafe_allow_html=True
    )


    high_risk_products = risk_df[
        risk_df["Overall_Risk"] == "HIGH"
    ][
        [
            "SKU",
            "Stockout_Risk",
            "Overstock_Risk",
            "Risk_Score",
            "Recommendation"
        ]
    ].sort_values(
        "Risk_Score",
        ascending=False
    )


    st.dataframe(
        high_risk_products.head(20),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# PAGE 2 — SKU INTELLIGENCE
# ==================================================

elif page == "SKU Intelligence":

    st.markdown(
        '<div class="title">🔎 SKU Intelligence</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="subtitle">'
        'Detailed demand, inventory and risk analysis'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown("---")


    # ----------------------------------------------
    # SKU SELECTOR
    # ----------------------------------------------

    sku_list = (
        risk_df["SKU"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_sku = st.selectbox(
        "Select SKU",
        sku_list
    )


    sku_risk = risk_df[
        risk_df["SKU"].astype(str) == selected_sku
    ]


    sku_forecast = forecast_df[
        forecast_df["SKU"].astype(str) == selected_sku
    ]


    if not sku_risk.empty:

        row = sku_risk.iloc[0]


        # ------------------------------------------
        # INVENTORY
        # ------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📦 Inventory Information'
            '</div>',
            unsafe_allow_html=True
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Current Stock",
                f"{row['Current_Stock']:.0f}"
            )


        with col2:

            st.metric(
                "On Order",
                f"{row['On_Order']:.0f}"
            )


        with col3:

            st.metric(
                "Lead Time",
                f"{row['Lead_Time_Days']:.0f} days"
            )


        with col4:

            st.metric(
                "Safety Stock",
                f"{row['Safety_Stock']:.0f}"
            )


        st.markdown("---")


        # ------------------------------------------
        # RISK
        # ------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '⚠️ Risk Analysis'
            '</div>',
            unsafe_allow_html=True
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.write("**Stockout Risk**")

            st.write(
                row["Stockout_Risk"]
            )


        with col2:

            st.write("**Overstock Risk**")

            st.write(
                row["Overstock_Risk"]
            )


        with col3:

            st.write("**Overall Risk**")

            st.write(
                row["Overall_Risk"]
            )


        st.metric(
            "Risk Score",
            f"{row['Risk_Score']:.0f} / 100"
        )


        st.markdown("---")


        # ------------------------------------------
        # RECOMMENDATION
        # ------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '💡 Recommended Action'
            '</div>',
            unsafe_allow_html=True
        )


        recommendation = row[
            "Recommendation"
        ]


        if recommendation == "REORDER NOW":

            st.error(
                "🔴 REORDER NOW"
            )


        elif recommendation == "REORDER SOON":

            st.warning(
                "🟡 REORDER SOON"
            )


        elif recommendation == "MARKDOWN / CLEAR":

            st.warning(
                "🏷️ MARKDOWN / CLEAR"
            )


        else:

            st.success(
                "🟢 HEALTHY"
            )


        st.markdown("---")


        # ------------------------------------------
        # FORECAST
        # ------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📈 Demand Forecast'
            '</div>',
            unsafe_allow_html=True
        )


        if sku_forecast.empty:

            st.info(
                "No forecast available for this SKU."
            )


        else:

            chart_data = sku_forecast.copy()


            if "Week_Start" in chart_data.columns:

                chart_data["Week_Start"] = (
                    pd.to_datetime(
                        chart_data["Week_Start"]
                    )
                )


                chart_data = chart_data.sort_values(
                    "Week_Start"
                )


                chart_data = chart_data.set_index(
                    "Week_Start"
                )


            if "Forecast_Units" in chart_data.columns:

                st.line_chart(
                    chart_data["Forecast_Units"]
                )


            st.dataframe(
                sku_forecast,
                use_container_width=True,
                hide_index=True
            )


# ==================================================
# PAGE 3 — ACTION CENTER
# ==================================================

elif page == "Action Center":

    st.markdown(
        '<div class="title">🎯 Action Center</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="subtitle">'
        'Inventory decisions generated by the risk engine'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown("---")


    # ----------------------------------------------
    # ACTION FILTER
    # ----------------------------------------------

    action_options = [
        "ALL",
        "REORDER NOW",
        "REORDER SOON",
        "MARKDOWN / CLEAR",
        "HEALTHY"
    ]


    selected_action = st.selectbox(
        "Filter by recommended action",
        action_options
    )


    if selected_action == "ALL":

        action_df = risk_df.copy()


    else:

        action_df = risk_df[
            risk_df["Recommendation"]
            == selected_action
        ].copy()


    # ----------------------------------------------
    # SUMMARY
    # ----------------------------------------------

    st.metric(
        "SKUs in this category",
        len(action_df)
    )


    st.markdown("---")


    # ----------------------------------------------
    # TABLE
    # ----------------------------------------------

    columns_to_show = [
        "SKU",
        "Current_Stock",
        "On_Order",
        "Lead_Time_Days",
        "Safety_Stock",
        "Risk_Score",
        "Overall_Risk",
        "Recommendation"
    ]


    available_columns = [
        column
        for column in columns_to_show
        if column in action_df.columns
    ]


    st.dataframe(
        action_df[
            available_columns
        ].sort_values(
            "Risk_Score",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")


st.markdown(
    """
    <div class="footer">
        🚀 Project FORESIGHT • AI-Powered Demand & Inventory Intelligence
    </div>
    """,
    unsafe_allow_html=True
)