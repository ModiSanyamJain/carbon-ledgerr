"""
CarbonLedger – Main Application Entry Point
Streamlit multi-page app with sidebar navigation and industry selector.
"""

import sys
import os
import streamlit as st

# ── Ensure project root is on the path ───────────────────────────────────────
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
# Fallback: also add cwd (needed for some cloud deployments)
_CWD = os.getcwd()
if _CWD not in sys.path:
    sys.path.insert(0, _CWD)

from config import APP_TITLE, APP_SUBTITLE

# ── Auto-initialise SQLite database on first run ────────────────────────────
from database.init_db import init_db
init_db()

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load Custom CSS ──────────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center; padding: 1rem 0 0.5rem;">
            <span style="font-size:2.5rem;">🌿</span>
            <h2 style="margin:0; background:linear-gradient(135deg,#00e676,#1de9b6);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        font-weight:800; letter-spacing:-0.5px;">
                {APP_TITLE}
            </h2>
            <p style="color:#9aa0ab; font-size:0.75rem; margin-top:2px;">
                {APP_SUBTITLE}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Navigation
    page = st.radio(
        "NAVIGATION",
        options=[
            "📊  Dashboard",
            "🧮  Carbon Calculator",
            "📜  Emission History",
            "🏅  Benchmarking",
            "💱  Marketplace",
            "🏭  Register Industry",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()

    # ── Industry Selector ────────────────────────────────────────────────
    st.markdown("##### 🏭 Select Industry")

    # Lazy import to avoid circular imports at module level
    from backend.industry_service import get_all_industries

    industries = []
    try:
        industries = get_all_industries()
    except Exception:
        st.warning("⚠️ Could not load industries from the database.")

    if industries:
        industry_options = {f"{ind['industry_name']} ({ind['sector']})": ind["industry_id"] for ind in industries}
        selected_label = st.selectbox(
            "Industry",
            options=list(industry_options.keys()),
            label_visibility="collapsed",
        )
        selected_industry_id = industry_options[selected_label]
    else:
        selected_industry_id = None
        if not industries and page != "🏭  Register Industry":
            st.info("No industries found. Register one first!")

    st.divider()
    st.caption(f"v1.0.0 • © 2025 CarbonLedger")


# ── Page Router ──────────────────────────────────────────────────────────────

if page == "📊  Dashboard":
    from frontend.dashboard import render
    render(selected_industry_id)

elif page == "🧮  Carbon Calculator":
    from frontend.calculator_page import render
    render(selected_industry_id)

elif page == "📜  Emission History":
    from frontend.history_page import render
    render(selected_industry_id)

elif page == "🏅  Benchmarking":
    from frontend.benchmarking_page import render
    render(selected_industry_id)

elif page == "💱  Marketplace":
    from frontend.marketplace_page import render
    render(selected_industry_id)

elif page == "🏭  Register Industry":
    # ── Inline Registration Page ─────────────────────────────────────────
    st.title("🏭 Register New Industry")
    st.caption("Add a new industrial facility to the CarbonLedger network")

    from backend.industry_service import register_industry, get_sectors

    existing_sectors = []
    try:
        existing_sectors = get_sectors()
    except Exception:
        pass

    with st.form("register_industry_form"):
        industry_name = st.text_input("🏢 Industry Name", placeholder="e.g. Tata Steel Works")

        c1, c2 = st.columns(2)
        with c1:
            use_existing = st.checkbox("Use existing sector", value=True)
            if use_existing and existing_sectors:
                sector = st.selectbox("🏷️ Sector", options=existing_sectors)
            else:
                sector = st.text_input("🏷️ Sector", placeholder="e.g. Steel, Cement, Petrochemical")
        with c2:
            location = st.text_input("📍 Location", placeholder="e.g. Jamshedpur")

        production_capacity = st.number_input(
            "⚙️ Annual Production Capacity (tons)",
            min_value=0.0,
            value=1000000.0,
            step=100000.0,
        )

        submitted = st.form_submit_button("🚀  Register Industry", use_container_width=True)

    if submitted:
        if not industry_name or not sector or not location:
            st.error("Please fill in all required fields.")
        else:
            try:
                new_id = register_industry(industry_name, sector, location, production_capacity)
                st.success(f"✅ Industry registered successfully! (ID: {new_id})")
                st.balloons()
                st.info("Refresh the page to see it in the industry selector.")
            except Exception as e:
                st.error(f"❌ Registration failed: {e}")
