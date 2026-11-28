import streamlit as st
import re
import importlib
import pandas as pd
from datetime import datetime
import database
importlib.reload(database)
import vajiram_content

st.set_page_config(
    page_title="Vajiram & Ravi Style UPSC & KEA Current Affairs Hub",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Vajiram & Ravi Inspired Styling
st.markdown("""
<style>
    .reportview-container {
        background: #fdfbf7;
    }
    .vajiram-header {
        background: linear-gradient(135deg, #c2410c 0%, #ea580c 50%, #f97316 100%);
        padding: 24px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 18px rgba(234, 88, 12, 0.22);
    }
    .vajiram-hub-card {
        background: #fffaf0;
        border: 2px solid #fdba74;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 2px 10px rgba(249, 115, 22, 0.08);
        height: 100%;
    }
    .vajiram-card-header {
        background-color: #ea580c;
        color: white;
        padding: 8px 14px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 1.05rem;
        text-align: center;
        margin-bottom: 14px;
        letter-spacing: 0.5px;
    }
    .date-row {
        padding: 10px 12px;
        border-bottom: 1px dashed #fed7aa;
        color: #7c2d12;
        font-size: 0.95rem;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
    }
    .date-row:hover {
        background-color: #ffedd5;
        border-radius: 6px;
    }
    .news-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-left: 5px solid #ea580c;
    }
    .source-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 700;
        font-size: 0.82rem;
        background-color: #ffedd5;
        color: #c2410c;
        margin-right: 6px;
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
    .species-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
        border-top: 4px solid #16a34a;
        margin-bottom: 20px;
    }
    .places-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
        border-top: 4px solid #0284c7;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Database Initialization
database.init_db()

# Start 24/7 Cloud Background Monitor
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
        print("[Cloud] 24/7 Background monitor worker started!")

start_cloud_background_monitor()

# Top Header matching Vajiram & Ravi Style
st.markdown("""
<div class="vajiram-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 style="color: white; margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.5px;">
                🏛️ VAJIRAM & RAVI STYLE UPSC & KEA CURRENT AFFAIRS HUB
            </h1>
            <p style="color: #ffedd5; margin-top: 8px; margin-bottom: 0; font-size: 1.05rem;">
                Prelims Pointers • Mains Articles • Daily Editorial Analysis • UPSC Daily Quiz • Wildlife & Maps in News
            </p>
        </div>
        <div style="background: rgba(255,255,255,0.18); padding: 8px 16px; border-radius: 20px; font-weight: 700; font-size: 0.9rem;">
            ⚡ 24/7 Live Cloud Engine
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Branding & Quick Controls
st.sidebar.markdown("### 🏛️ UPSC & KEA Portal")
st.sidebar.caption("High-Yield Daily Notes & Official Gov Ingestion")

# On-demand refresh button
if st.sidebar.button("🔄 Check & Fetch Latest Releases", use_container_width=True):
    with st.spinner("Scraping PIB, PM India, Mann Ki Baat, Karnataka State & Newspapers..."):
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

# Official Source Filter
source_options = [
    "All Sources",
    "PIB (Official)",
    "PM India (Visits & Cabinet)",
    "Mann Ki Baat (PM Address)",
    "Karnataka State News",
    "The Hindu",
    "Indian Express",
    "The Hindu Editorial"
]
source_choice = st.sidebar.selectbox("📡 News & Govt Source", source_options)
active_source_query = None if source_choice == "All Sources" else source_choice

# Date Filter
date_choice = st.sidebar.selectbox(
    "📅 Date Filter",
    ["All Dates", "28 Nov 2026", "27 Nov 2026", "26 Nov 2026", "Monthly Address"]
)
active_date_query = None if date_choice == "All Dates" else date_choice

# GS Syllabus Filter
gs_options = ["All", "GS-1", "GS-2", "GS-3", "GS-4", "Prelims Pointer"]
selected_gs = st.sidebar.selectbox("Filter by GS Paper", gs_options)

# Keyword search
search_term = st.sidebar.text_input("🔍 Search Keyword / Scheme / Place", placeholder="e.g. Ambedkar, IORA, ISRO, NHRC, Mann Ki Baat...")

# Global Access Note
st.sidebar.markdown("---")
st.sidebar.markdown("📱 **Permanent Cloud URL:**")
st.sidebar.success("""
Live 24/7 on any device:  
👉 **`https://pib-upsc-agent.onrender.com`**
""")

# Top Navigation Tabs (Vajiram Architecture)
tabs = st.tabs([
    "🏠 Vajiram Hub (Home)",
    "🎯 Prelims Pointers",
    "💡 Mains GS Articles",
    "📰 Daily Editorial Analysis",
    "🐾 Species & Wildlife in News",
    "🗺️ Places in News & Maps",
    "📝 UPSC Daily Quiz",
    "🟡 Karnataka State (KEA)",
    "📊 Exam Analytics"
])

def render_article_cards(article_list):
    if not article_list:
        st.info("No articles found under this filter. Click **'🔄 Check & Fetch Latest Releases'** in the sidebar to scrape today's updates!")
        return

    st.caption(f"Showing **{len(article_list)}** exam-yield items:")

    for art in article_list:
        pillar = art.get("main_pillar") or "National"
        sub_topic = art.get("sub_topic") or art.get("subject_group") or "General"
        source_name = art.get("source_name") or "PIB (Official)"
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

        thumb_img = vajiram_content.get_article_thumbnail(title, summary, sub_topic, pillar)

        with st.container():
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            col_t1, col_t2 = st.columns([1, 2.5])
            with col_t1:
                st.image(thumb_img, use_container_width=True)
            with col_t2:
                st.markdown(f"""
                <div>
                    <span class="source-badge">📡 {source_name}</span>
                    <span class="pillar-badge">📁 {pillar}</span>
                    <span class="subtopic-badge">🏷️ {sub_topic}</span>
                    <span class="gs-badge">{gs_tag}</span>
                    <span class="ministry-badge">🏢 {ministry}</span>
                    {f'<span class="ministry-badge">📅 {pub_date}</span>' if pub_date else ''}
                </div>
                <h3 style="margin-top: 10px; margin-bottom: 6px; color: #0f172a; font-size: 1.25rem;">{title}</h3>
                <p class="summary-text">{summary}</p>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1.3, 1.3, 1])
                with col1:
                    with st.expander("🎯 Key Prelims Pointers", expanded=False):
                        st.write(prelims if prelims else "No specific prelims points extracted.")
                with col2:
                    with st.expander("💡 Mains Dimensions", expanded=False):
                        st.write(mains if mains else "General socio-economic and governance significance.")
                with col3:
                    is_mkb = "mann ki baat" in source_name.lower() or "mann ki baat" in title.lower()
                    is_pm = "pm india" in source_name.lower() or "prime minister" in ministry.lower()
                    is_kar = "karnataka" in source_name.lower() or "karnataka" in pillar.lower()
                    is_pib = "pib" in source_name.lower()

                    if is_mkb:
                        st.link_button("🎙️ Official Transcript", url=link, use_container_width=True)
                        st.link_button("▶️ Watch on YouTube", url="https://www.youtube.com/results?search_query=mann+ki+baat+narendra+modi+latest", use_container_width=True)
                    elif is_pm:
                        st.link_button("🏛️ PM India Official", url=link, use_container_width=True)
                    elif is_kar:
                        st.link_button("🟡 Karnataka Report", url=link, use_container_width=True)
                    elif is_pib:
                        st.link_button("🔗 Official PIB (English)", url=link, use_container_width=True)
                    else:
                        st.link_button("📰 Read Full Article", url=link, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed #e2e8f0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 1: VAJIRAM HUB (HOME) - Visual Showcase & Signature Cards
# -------------------------------------------------------------
with tabs[0]:
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <h2 style="color: #0f172a; font-weight: 800; margin-bottom: 6px; font-size: 1.8rem;">Current Affairs 2026 for UPSC & KEA Exam</h2>
        <p style="color: #475569; font-size: 1.05rem; margin-top: 0;">
            Daily Current Affairs simplifies the preparation process by providing daily updates, Prelims facts, Mains dimensions, wildlife profiles, and maps.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. TWO LARGE FEATURED HERO CARDS (Matching Screenshot top row)
    f_c1, f_c2 = st.columns(2)
    hero_items = vajiram_content.FEATURED_HERO_CARDS
    with f_c1:
        item = hero_items[0]
        st.image(item["image_url"], use_container_width=True)
        st.markdown(f"""
        <div style="background: white; border-radius: 8px; padding: 12px; margin-top: -8px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 3px solid #ea580c;">
            <span class="gs-badge">{item['gs_paper']}</span>
            <span class="subtopic-badge">{item['category']}</span>
            <h3 style="color: #0f172a; margin: 8px 0 4px 0; font-size: 1.2rem;">{item['title']}</h3>
            <p style="color: #475569; font-size: 0.95rem; margin-bottom: 8px;">{item['summary']}</p>
        </div>
        """, unsafe_allow_html=True)
        with st.expander(f"📖 Study Dimensions: {item['title'][:25]}...", expanded=False):
            st.markdown(f"**🎯 Prelims:**\n{item['prelims']}")
            st.markdown(f"**💡 Mains:**\n{item['mains']}")

    with f_c2:
        item = hero_items[1]
        st.image(item["image_url"], use_container_width=True)
        st.markdown(f"""
        <div style="background: white; border-radius: 8px; padding: 12px; margin-top: -8px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 3px solid #0284c7;">
            <span class="gs-badge">{item['gs_paper']}</span>
            <span class="subtopic-badge">{item['category']}</span>
            <h3 style="color: #0f172a; margin: 8px 0 4px 0; font-size: 1.2rem;">{item['title']}</h3>
            <p style="color: #475569; font-size: 0.95rem; margin-bottom: 8px;">{item['summary']}</p>
        </div>
        """, unsafe_allow_html=True)
        with st.expander(f"📖 Study Dimensions: {item['title'][:25]}...", expanded=False):
            st.markdown(f"**🎯 Prelims:**\n{item['prelims']}")
            st.markdown(f"**💡 Mains:**\n{item['mains']}")

    # 2. FOUR MEDIUM FEATURED CARDS (Matching Screenshot bottom row)
    m_c1, m_c2, m_c3, m_c4 = st.columns(4)
    cols = [m_c1, m_c2, m_c3, m_c4]
    for idx, col in enumerate(cols):
        with col:
            item = hero_items[2 + idx]
            st.image(item["image_url"], use_container_width=True)
            st.markdown(f"""
            <div style="background: white; border-radius: 8px; padding: 10px; margin-top: -6px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); min-height: 130px; border-top: 2px solid #ea580c;">
                <span class="gs-badge" style="font-size: 0.72rem; padding: 2px 6px;">{item['gs_paper']}</span>
                <h4 style="color: #0f172a; margin: 6px 0 3px 0; font-size: 0.98rem;">{item['title']}</h4>
                <p style="color: #64748b; font-size: 0.8rem; margin: 0;">{item['category']}</p>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("📖 Study Pointers", expanded=False):
                st.caption(item["summary"])
                st.markdown(f"**🎯 Prelims:**\n{item['prelims']}")

    st.markdown("<hr style='margin: 25px 0; border: none; border-top: 2px solid #fed7aa;'>", unsafe_allow_html=True)
    st.subheader("🔥 Daily UPSC & KEA Coverage Hub")

    # 4 Signature Vajiram Cards (matching user screenshot)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("""
        <div class="vajiram-hub-card">
            <div class="vajiram-card-header">Prelims Pointers</div>
            <div class="date-row"><span>November 28, 2026</span><span>→</span></div>
            <div class="date-row"><span>November 27, 2026</span><span>→</span></div>
            <div class="date-row"><span>November 26, 2026</span><span>→</span></div>
            <div class="date-row"><span>November 25, 2026</span><span>→</span></div>
            <div class="date-row"><span>November 24, 2026</span><span>→</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col_v2:
        st.markdown("""
        <div class="vajiram-hub-card">
            <div class="vajiram-card-header">Mains Articles</div>
            <div class="date-row"><span>November 28, 2026 (GS-1 & GS-2)</span><span>→</span></div>
            <div class="date-row"><span>November 27, 2026 (GS-3 & GS-4)</span><span>→</span></div>
            <div class="date-row"><span>November 26, 2026 (Policy & Bills)</span><span>→</span></div>
            <div class="date-row"><span>November 25, 2026 (Economy & Trade)</span><span>→</span></div>
            <div class="date-row"><span>November 24, 2026 (International)</span><span>→</span></div>
        </div>
        """, unsafe_allow_html=True)

    col_v3, col_v4 = st.columns(2)
    with col_v3:
        st.markdown("""
        <div class="vajiram-hub-card">
            <div class="vajiram-card-header">UPSC Daily Editorial Analysis</div>
            <div class="date-row"><span>Daily Editorial Analysis 28 November 2026</span><span>→</span></div>
            <div class="date-row"><span>Daily Editorial Analysis 27 November 2026</span><span>→</span></div>
            <div class="date-row"><span>Daily Editorial Analysis 26 November 2026</span><span>→</span></div>
            <div class="date-row"><span>Daily Editorial Analysis 25 November 2026</span><span>→</span></div>
            <div class="date-row"><span>Daily Editorial Analysis 24 November 2026</span><span>→</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col_v4:
        st.markdown("""
        <div class="vajiram-hub-card">
            <div class="vajiram-card-header">UPSC Daily Quiz</div>
            <div class="date-row"><span>UPSC Daily Quiz 28 November 2026</span><span>→</span></div>
            <div class="date-row"><span>UPSC Daily Quiz 27 November 2026</span><span>→</span></div>
            <div class="date-row"><span>UPSC Daily Quiz 26 November 2026</span><span>→</span></div>
            <div class="date-row"><span>UPSC Daily Quiz 25 November 2026</span><span>→</span></div>
            <div class="date-row"><span>UPSC Daily Quiz 24 November 2026</span><span>→</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📰 Today's Curated High-Yield Stream")
    articles_home = database.get_recent_articles(
        limit=20,
        gs_filter=None if selected_gs == "All" else selected_gs,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    render_article_cards(articles_home)

# -------------------------------------------------------------
# TAB 2: PRELIMS POINTERS
# -------------------------------------------------------------
with tabs[1]:
    st.subheader("🎯 Prelims High-Yield Facts & Pointers")
    st.caption("Focus on factual benchmarks: Nodal Ministries, Statutory Provisions, Outlays, Reports & Committees.")
    articles_prelims = database.get_recent_articles(
        limit=50,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    for art in articles_prelims:
        p_facts = art.get("prelims_facts")
        if p_facts and p_facts.strip():
            with st.container():
                st.markdown(f"""
                <div class="news-card" style="border-left-color: #ea580c;">
                    <span class="source-badge">📡 {art.get('source_name', 'Official')}</span>
                    <span class="gs-badge">{art.get('gs_paper', 'Prelims')}</span>
                    <span class="ministry-badge">🏢 {art.get('ministry', '')}</span>
                    <h4 style="margin: 8px 0; color: #0f172a;">{art.get('title')}</h4>
                    <div style="background: #fff7ed; padding: 12px; border-radius: 8px; border-left: 3px solid #ea580c; font-size: 0.98rem;">
                        <b>🎯 Prelims Pointers:</b><br>{p_facts}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 3: MAINS GS ARTICLES
# -------------------------------------------------------------
with tabs[2]:
    st.subheader("💡 Mains Answer-Writing Dimensions")
    st.caption("Structured Dimensions: Governance significance, constitutional angles, socio-economic impact.")
    articles_mains = database.get_recent_articles(
        limit=40,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    for art in articles_mains:
        m_dim = art.get("mains_pointer")
        if m_dim and m_dim.strip():
            with st.container():
                st.markdown(f"""
                <div class="news-card" style="border-left-color: #0284c7;">
                    <span class="pillar-badge">📁 {art.get('main_pillar', 'National')}</span>
                    <span class="gs-badge">{art.get('gs_paper', 'GS-2')}</span>
                    <span class="ministry-badge">🏢 {art.get('ministry', '')}</span>
                    <h4 style="margin: 8px 0; color: #0f172a;">{art.get('title')}</h4>
                    <p style="color: #475569; font-size: 0.95rem;">{art.get('short_summary', '')}</p>
                    <div style="background: #f0f9ff; padding: 12px; border-radius: 8px; border-left: 3px solid #0284c7; font-size: 0.98rem;">
                        <b>💡 Mains Dimension:</b><br>{m_dim}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 4: DAILY EDITORIAL ANALYSIS
# -------------------------------------------------------------
with tabs[3]:
    st.subheader("📰 Daily Editorial Analysis (The Hindu & The Indian Express)")
    st.caption("Deep-dive critical analysis of leading national editorials, Supreme Court verdicts, and economic reforms.")
    articles_ed = database.get_recent_articles(
        limit=30,
        source_filter=None,
        search_query=search_term if search_term.strip() else None
    )
    editorial_items = [a for a in articles_ed if "editorial" in a.get("source_name", "").lower() or "the hindu" in a.get("source_name", "").lower() or "indian express" in a.get("source_name", "").lower()]
    render_article_cards(editorial_items if editorial_items else articles_ed[:8])

# -------------------------------------------------------------
# TAB 5: SPECIES & WILDLIFE IN NEWS (With Animals Pictures!)
# -------------------------------------------------------------
with tabs[4]:
    st.subheader("🐾 Species & Wildlife in News (High-Yield Biodiversity Framework)")
    st.caption("Official IUCN Red List Status, Wildlife Protection Act (WPA 1972) Schedules, CITES Appendices, and Distribution Maps.")

    for sp in vajiram_content.SPECIES_IN_NEWS:
        with st.container():
            col_img, col_info = st.columns([1.2, 2.2])
            with col_img:
                st.image(sp["image_url"], caption=sp["name"], use_container_width=True)
            with col_info:
                st.markdown(f"""
                <div class="species-card">
                    <h3 style="margin-top: 0; color: #15803d; font-size: 1.3rem;">{sp['name']}</h3>
                    <p style="margin: 0; font-style: italic; color: #64748b; font-size: 0.95rem;">Scientific Name: {sp['scientific_name']}</p>
                    <div style="margin: 12px 0;">
                        <span style="background-color: {sp['iucn_badge_color']}; color: white; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.82rem;">IUCN: {sp['iucn_status']}</span>
                        <span style="background-color: #f3f4f6; color: #1f2937; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 0.82rem;">WPA: {sp['wpa_schedule']}</span>
                        <span style="background-color: #dbeafe; color: #1e40af; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 0.82rem;">CITES: {sp['cites']}</span>
                    </div>
                    <p style="font-size: 0.95rem; margin-bottom: 8px;"><b>🌿 Habitat & Distribution:</b><br>{sp['habitat']}</p>
                    <div style="background: #f0fdf4; border-left: 3px solid #16a34a; padding: 10px; border-radius: 6px; font-size: 0.95rem;">
                        <b>🎯 Why in News (Exam Angle):</b><br>{sp['why_in_news']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed #cbd5e1;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 6: PLACES IN NEWS & INTERACTIVE MAPS
# -------------------------------------------------------------
with tabs[5]:
    st.subheader("🗺️ Places in News & Interactive Geographic Mapping")
    st.caption("Explore key global choke points, maritime passages, historical heritage sites, and national strategic locations.")

    # Convert places to DataFrame for Streamlit interactive map
    places_data = vajiram_content.PLACES_IN_NEWS
    map_df = pd.DataFrame([
        {"lat": p["lat"], "lon": p["lon"], "name": p["name"]}
        for p in places_data
    ])

    st.markdown("#### 📍 Interactive Hotspot Map")
    st.map(map_df, zoom=3, use_container_width=True)

    st.markdown("#### 📌 Location Profiles & Exam Pointers")
    for place in places_data:
        with st.container():
            st.markdown(f"""
            <div class="places-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #0284c7; font-size: 1.25rem;">📍 {place['name']}</h3>
                    <span style="background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 0.85rem;">{place['region']}</span>
                </div>
                <p style="margin-top: 10px; font-size: 0.98rem; color: #334155;"><b>Geo-Strategic Importance:</b> {place['importance']}</p>
                <div style="background: #f0fdfa; border-left: 3px solid #0d9488; padding: 10px; border-radius: 6px; font-size: 0.95rem;">
                    <b>🧭 UPSC & KEA Geographic Facts:</b><br>{place['upsc_kea_facts']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 7: UPSC DAILY QUIZ (Interactive Test Engine)
# -------------------------------------------------------------
with tabs[6]:
    st.subheader("📝 UPSC & KEA Daily Practice Quiz")
    st.caption("Daily exam-standard multiple choice questions. Choose your answers and get immediate scoring and explanations.")

    quiz_questions = vajiram_content.DAILY_QUIZ_QUESTIONS
    score = 0
    submitted = False

    for q in quiz_questions:
        st.markdown(f"**Q{q['id']}.** {q['question']}")
        user_choice = st.radio(
            f"Select your answer for Q{q['id']}:",
            q["options"],
            key=f"quiz_opt_{q['id']}",
            index=None
        )
        
        with st.expander(f"🔍 Show Answer & Explanation (Q{q['id']})", expanded=False):
            correct_opt = q["options"][q["correct_index"]]
            st.markdown(f"**Correct Answer:** `{correct_opt}`")
            st.info(f"**Detailed Explanation:**\n\n{q['explanation']}")
        
        st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px dashed #e2e8f0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 8: KARNATAKA STATE (KEA SPECIAL 20-25 QUESTIONS)
# -------------------------------------------------------------
with tabs[7]:
    st.subheader("🟡 Karnataka State Affairs & KEA Corner")
    st.caption("State Acts (2026), Statutory Bodies, Schemes, Programmes, and Regional Ecology.")

    articles_kar = database.get_recent_articles(
        limit=50,
        pillar_filter="Karnataka",
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    if not articles_kar:
        # Fallback to source filter if pillar not tagged yet
        articles_kar = database.get_recent_articles(
            limit=50,
            source_filter="Karnataka State News"
        )
    render_article_cards(articles_kar)

# -------------------------------------------------------------
# TAB 9: EXAM ANALYTICS & TRENDS
# -------------------------------------------------------------
with tabs[8]:
    st.subheader("📊 Syllabus Coverage & Weightage Analytics")
    stats = database.get_dashboard_stats()
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### 📁 Pillar Breakdown")
        pillar_df = pd.DataFrame(list(stats["pillars"].items()), columns=["Pillar", "Articles"])
        st.bar_chart(pillar_df.set_index("Pillar"), color="#ea580c")

    with col_g2:
        st.markdown("#### 🏛 GS Paper Weightage")
        gs_df = pd.DataFrame(list(stats["gs_papers"].items()), columns=["GS Paper", "Articles"])
        st.bar_chart(gs_df.set_index("GS Paper"), color="#0284c7")

    st.markdown("#### 🏢 Top Ministries in Focus")
    min_df = pd.DataFrame(list(stats["top_ministries"].items()), columns=["Ministry", "Articles"])
    st.bar_chart(min_df.set_index("Ministry"), color="#16a34a")
