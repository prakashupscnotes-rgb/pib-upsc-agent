import streamlit as st
import re
import importlib
from datetime import datetime
import database
importlib.reload(database)

st.set_page_config(
    page_title="KEA & UPSC Current Affairs Digest",
    page_icon="🏛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern card styling & tabs
st.markdown("""
<style>
    .reportview-container {
        background: #f8fafc;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border-left: 4px solid #3b82f6;
        text-align: center;
    }
    .news-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-left: 5px solid #1e40af;
    }
    .pillar-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 700;
        font-size: 0.82rem;
        background-color: #dbeafe;
        color: #1e40af;
        margin-right: 6px;
    }
    .subtopic-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.82rem;
        background-color: #fef3c7;
        color: #92400e;
        margin-right: 6px;
    }
    .gs-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.82rem;
        background-color: #e0e7ff;
        color: #3730a3;
        margin-right: 6px;
    }
    .ministry-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.82rem;
        background-color: #f3f4f6;
        color: #4b5563;
        margin-right: 6px;
    }
    .summary-text {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1f2937;
        margin: 14px 0;
    }
</style>
""", unsafe_allow_html=True)

# Ensure database exists & initialize
database.init_db()

# Start 24/7 Cloud Background Monitor (Runs continuously on Render even when laptop is off)
import threading
import time

def start_cloud_background_monitor():
    def monitor_loop():
        time.sleep(10)
        try:
            import main
            while True:
                main.run_pipeline()
                time.sleep(1800)
        except Exception as ex:
            print(f"[Cloud Background Monitor] Notice: {ex}")

    if not hasattr(st, "_pib_cloud_monitor_started"):
        st._pib_cloud_monitor_started = True
        worker = threading.Thread(target=monitor_loop, daemon=True, name="PIBCloudWorker")
        worker.start()
        print("[Cloud] 24/7 Background PIB monitor worker started!")

start_cloud_background_monitor()

# Sidebar: Branding & Quick Controls
st.sidebar.title("🏛 KEA & UPSC Portal")
st.sidebar.caption("High-Yield Daily Current Affairs & Exam Framework")

# On-demand refresh button
if st.sidebar.button("🔄 Check & Fetch Latest Releases", use_container_width=True):
    with st.spinner("Scraping PIB & Running Multi-Pillar AI Classifier..."):
        try:
            import main
            main.run_pipeline()
            st.sidebar.success("Pipeline executed successfully! Fresh news loaded.")
            st.rerun()
        except Exception as e:
            st.sidebar.warning(f"Fetch notice: {e}")

# Sidebar Filters
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Filter Controls")

# Date Filter
date_choice = st.sidebar.selectbox(
    "📅 Date Filter",
    ["All Dates", "28 Nov 2026", "27 Nov 2026", "26 Nov 2026"]
)
active_date_query = None if date_choice == "All Dates" else date_choice

# GS Syllabus Filter
gs_options = ["All", "GS-1", "GS-2", "GS-3", "GS-4", "Prelims Pointer"]
selected_gs = st.sidebar.selectbox("Filter by GS Paper", gs_options)

# Keyword search
search_term = st.sidebar.text_input("🔍 Search Keyword / Scheme / Place", placeholder="e.g. Ambedkar, IORA, ISRO, NHRC...")

# Global Access Note
st.sidebar.markdown("---")
st.sidebar.markdown("📱 **Live Cloud Access (Any Device / 24/7):**")
st.sidebar.success("""
Open anywhere on mobile, tablet, or PC:  
👉 **`https://pib-upsc-agent.onrender.com`**
""")

# Main Content Area
st.title("📖 KEA & UPSC Daily Current Affairs")
st.markdown("Automated Exam-Ready Notes categorized into **National**, **International**, **Karnataka Special**, and **Static Core**.")

# 1-Row Summary Metrics Bar
stats = database.get_dashboard_stats()
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Total Curated Articles", sum(stats["pillars"].values()))
with col_m2:
    st.metric("National Affairs", stats["pillars"].get("National", 0))
with col_m3:
    st.metric("International & Summits", stats["pillars"].get("International", 0))
with col_m4:
    st.metric("Karnataka & Misc", stats["pillars"].get("Karnataka", 0) + stats["pillars"].get("Miscellaneous", 0) + stats["pillars"].get("Static", 0))

st.markdown("---")

# Main Navigation Tabs matching Handwritten Diagram
tabs = st.tabs([
    "🏛️ All Updates",
    "🇮🇳 National",
    "🌐 International",
    "🟡 Karnataka State",
    "🎖️ Miscellaneous",
    "📚 Static Corner (8-10 Q)",
    "📊 Exam Analytics & Trends"
])

def render_article_cards(article_list):
    if not article_list:
        st.info("No articles found under this section. Click **'🔄 Check & Fetch Latest Releases'** in the sidebar to scrape today's updates!")
        return

    st.caption(f"Displaying **{len(article_list)}** exam-yield items:")

    for art in article_list:
        pillar = art.get("main_pillar") or "National"
        sub_topic = art.get("sub_topic") or art.get("subject_group") or "General"
        gs_tag = art.get("gs_paper") or "GS-2"
        if gs_tag.strip().lower() == "none":
            gs_tag = "GS-2"

        ministry = art.get("ministry") or "Government of India"
        title = art.get("title", "")
        summary = art.get("short_summary", "")
        prelims = art.get("prelims_facts", "")
        mains = art.get("mains_pointer", "")

        pub_date = art.get("published_date", "")
        if pub_date:
            pub_date = re.sub(r"^प्रविष्टि\s*तिथि:\s*", "", pub_date).strip()
            pub_date = re.sub(r"^Posted\s*On:\s*", "", pub_date, flags=re.I).strip()
            pub_date = re.sub(r"^Release ID:\s*\d+,?\s*", "", pub_date, flags=re.I).strip()

        link = art.get("link", "#")
        link = link.replace("PressReleaseIframePage.aspx", "PressReleasePage.aspx")
        if "lang=" in link.lower():
            link = re.sub(r"lang=\d+", "lang=1", link, flags=re.IGNORECASE)
        elif "pib.gov.in" in link:
            sep = "&" if "?" in link else "?"
            link = f"{link}{sep}lang=1"

        with st.container():
            st.markdown(f"""
            <div class="news-card">
                <div>
                    <span class="pillar-badge">📁 {pillar}</span>
                    <span class="subtopic-badge">🏷️ {sub_topic}</span>
                    <span class="gs-badge">{gs_tag}</span>
                    <span class="ministry-badge">🏢 {ministry}</span>
                    {f'<span class="ministry-badge">📅 {pub_date}</span>' if pub_date else ''}
                </div>
                <h3 style="margin-top: 10px; margin-bottom: 5px; color: #0f172a;">{title}</h3>
                <p class="summary-text">{summary}</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1.5, 1.5, 1])
            with col1:
                with st.expander("🎯 Key Prelims Pointers", expanded=False):
                    st.write(prelims if prelims else "No specific prelims points extracted.")
            with col2:
                with st.expander("💡 Mains Dimensions", expanded=False):
                    st.write(mains if mains else "General socio-economic and governance significance.")
            with col3:
                st.link_button("🔗 Official English PIB Link", url=link, use_container_width=True)

            st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed #e2e8f0;'>", unsafe_allow_html=True)

# TAB 1: ALL UPDATES
with tabs[0]:
    articles_all = database.get_recent_articles(
        limit=50,
        gs_filter=None if selected_gs == "All" else selected_gs,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query
    )
    render_article_cards(articles_all)

# TAB 2: NATIONAL
with tabs[1]:
    st.subheader("🇮🇳 National Current Affairs")
    st.caption("Polity • Economy • Geography • Environment • History & Culture • Science & Tech • Health & Society")
    sub_nat = st.pills(
        "National Sub-Topic Filter:",
        ["All National", "Polity", "Economy", "Geography", "Environment", "History & Culture", "Science & Tech", "Health & Society"],
        default="All National"
    )
    active_sub = None if sub_nat == "All National" else sub_nat
    articles_nat = database.get_recent_articles(
        limit=50,
        pillar_filter="National",
        sub_topic_filter=active_sub,
        gs_filter=None if selected_gs == "All" else selected_gs,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query
    )
    render_article_cards(articles_nat)

# TAB 3: INTERNATIONAL
with tabs[2]:
    st.subheader("🌐 International Relations & Global Affairs")
    st.caption("International Groupings • International Organisations • Mapping / Places in News • Summits")
    sub_intl = st.pills(
        "International Sub-Topic Filter:",
        ["All International", "I. Groupings", "I. Organisations", "Mapping (Places in News)", "I. Summit"],
        default="All International"
    )
    active_sub_intl = None if sub_intl == "All International" else sub_intl
    articles_intl = database.get_recent_articles(
        limit=50,
        pillar_filter="International",
        sub_topic_filter=active_sub_intl,
        gs_filter=None if selected_gs == "All" else selected_gs,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query
    )
    render_article_cards(articles_intl)

# TAB 4: KARNATAKA SPECIAL
with tabs[3]:
    st.subheader("🟡 Karnataka State Specific Current Affairs")
    st.caption("State Acts (2026) • Statutory Bodies • Policy • Schemes • Programmes • Campaigns • Apps & Portals")
    sub_kar = st.pills(
        "Karnataka Filter:",
        ["All Karnataka", "Acts (2026)", "Statutory Bodies", "Policy", "Schemes", "Programmes & Campaigns", "Apps & Portals"],
        default="All Karnataka"
    )
    active_sub_kar = None if sub_kar == "All Karnataka" else sub_kar
    articles_kar = database.get_recent_articles(
        limit=50,
        pillar_filter="Karnataka",
        sub_topic_filter=active_sub_kar,
        gs_filter=None if selected_gs == "All" else selected_gs,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query
    )
    render_article_cards(articles_kar)

# TAB 5: MISCELLANEOUS
with tabs[4]:
    st.subheader("🎖️ Miscellaneous Current Affairs")
    st.caption("Sports • Awards • Committees • Reports & Index • Demise • Books & Authors • Persons in News")
    sub_misc = st.pills(
        "Miscellaneous Filter:",
        ["All Misc", "Sports", "Awards", "Committees", "Reports and Index", "Demise", "Books & Authors", "Persons in News"],
        default="All Misc"
    )
    active_sub_misc = None if sub_misc == "All Misc" else sub_misc
    articles_misc = database.get_recent_articles(
        limit=50,
        pillar_filter="Miscellaneous",
        sub_topic_filter=active_sub_misc,
        gs_filter=None if selected_gs == "All" else selected_gs,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query
    )
    render_article_cards(articles_misc)

# TAB 6: STATIC CORNER (8-10 Q)
with tabs[5]:
    st.subheader("📚 Static Core [High Weightage 8-10 Questions]")
    st.caption("Karnataka Budget • Karnataka Economic Survey • Karnataka Schemes • Central Schemes")
    sub_static = st.pills(
        "Static Filter:",
        ["All Static", "Karnataka Budget", "Karnataka Economic Survey", "Karnataka Schemes", "Central Schemes"],
        default="All Static"
    )
    active_sub_static = None if sub_static == "All Static" else sub_static
    articles_static = database.get_recent_articles(
        limit=50,
        pillar_filter="Static",
        sub_topic_filter=active_sub_static,
        gs_filter=None if selected_gs == "All" else selected_gs,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query
    )
    render_article_cards(articles_static)

# TAB 7: VISUAL ANALYTICS & CHARTS
with tabs[6]:
    st.subheader("📊 Visual Analytics & Exam Question Distribution")
    st.caption("Real-time breakdown of current affairs items across syllabus pillars and GS papers.")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### 📌 Current Affairs by Pillar")
        pillar_data = stats.get("pillars", {})
        if pillar_data:
            st.bar_chart(pillar_data)
        else:
            st.info("No data available yet.")

    with col_g2:
        st.markdown("#### 🎯 GS Paper Question Weightage")
        gs_data = stats.get("gs_papers", {})
        if gs_data:
            st.bar_chart(gs_data)
        else:
            st.info("No data available yet.")

    st.markdown("#### 🏢 Ministry & Sector-wise Representation")
    subj_data = stats.get("subjects", {})
    if subj_data:
        st.bar_chart(subj_data)
