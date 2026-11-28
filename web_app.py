import streamlit as st
import re
import importlib
import pandas as pd
from datetime import datetime
import database
importlib.reload(database)
import portal_content

st.set_page_config(
    page_title="You to UPSC | KEA & UPSC Current Affairs Portal",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern, Unique "You to UPSC" Identity
st.markdown("""
<style>
    .reportview-container {
        background: #f8fafc;
    }
    .brand-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #1d4ed8 100%);
        padding: 24px 28px;
        border-radius: 16px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(30, 58, 138, 0.22);
        border-bottom: 4px solid #f59e0b;
    }
    .brand-title {
        color: #ffffff;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.5px;
    }
    .brand-tagline {
        color: #93c5fd;
        font-size: 1.05rem;
        font-weight: 500;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .pillar-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.84rem;
        background-color: #e0e7ff;
        color: #3730a3;
        margin-right: 8px;
    }
    .subtopic-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.84rem;
        background-color: #fef3c7;
        color: #92400e;
        margin-right: 8px;
    }
    .source-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.84rem;
        background-color: #fee2e2;
        color: #991b1b;
        margin-right: 8px;
    }
    .news-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
        border-left: 5px solid #2563eb;
        transition: transform 0.15s ease-in-out;
    }
    .static-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
        border-top: 4px solid #f59e0b;
    }
    .species-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
        border-top: 4px solid #10b981;
        margin-bottom: 22px;
    }
    .places-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
        border-top: 4px solid #06b6d4;
        margin-bottom: 22px;
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
            print(f"[Cloud Monitor] Notice: {ex}")

    if not hasattr(st, "_pib_cloud_monitor_started"):
        st._pib_cloud_monitor_started = True
        worker = threading.Thread(target=monitor_loop, daemon=True, name="PIBCloudWorker")
        worker.start()
        print("[Cloud] 24/7 Continuous monitor worker running.")

start_cloud_background_monitor()

# Header: "You to UPSC" Identity
st.markdown(f"""
<div class="brand-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 class="brand-title">🦅 {portal_content.CHANNEL_NAME}</h1>
            <p class="brand-tagline">
                <i>"{portal_content.CHANNEL_TAGLINE}"</i> • Daily KEA & UPSC Exam Portal ({portal_content.CHANNEL_HANDLE})
            </p>
        </div>
        <div style="text-align: right; margin-top: 8px;">
            <a href="{portal_content.CHANNEL_URL}" target="_blank" style="background: #f59e0b; color: #0f172a; padding: 9px 18px; border-radius: 20px; font-weight: 800; font-size: 0.9rem; text-decoration: none; display: inline-block;">
                ▶ Visit YouTube Channel
            </a>
            <div style="color: #93c5fd; font-size: 0.8rem; margin-top: 6px; font-weight: 600;">
                ⚡ 24/7 Live Cloud Engine
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown(f"### 🦅 {portal_content.CHANNEL_NAME}")
st.sidebar.caption(f"{portal_content.CHANNEL_HANDLE} • KEA & UPSC Exam Framework")

if st.sidebar.button("🔄 Check & Fetch Latest Releases", use_container_width=True):
    with st.spinner("Scraping PIB, PM India, Mann Ki Baat, Karnataka State & Newspapers..."):
        try:
            import main
            main.run_pipeline()
            st.sidebar.success("Pipeline executed successfully! Fresh news loaded.")
            st.rerun()
        except Exception as e:
            st.sidebar.warning(f"Fetch notice: {e}")

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Filter Controls")

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

date_choice = st.sidebar.selectbox(
    "📅 Date Filter",
    ["All Dates", "28 Nov 2026", "27 Nov 2026", "26 Nov 2026", "Monthly Address"]
)
active_date_query = None if date_choice == "All Dates" else date_choice

gs_options = ["All", "GS-1", "GS-2", "GS-3", "GS-4", "Prelims Pointer"]
selected_gs = st.sidebar.selectbox("Filter by GS Paper", gs_options)

search_term = st.sidebar.text_input("🔍 Search Keyword / Scheme / Place", placeholder="e.g. Ambedkar, IORA, ISRO, NHRC, Mann Ki Baat...")

st.sidebar.markdown("---")
st.sidebar.markdown("📱 **Permanent Cloud Access:**")
st.sidebar.success("""
Access on mobile, tablet, or PC 24/7:  
👉 **`https://pib-upsc-agent.onrender.com`**
""")

# Main Navigation Tabs: Exact match to user's handwritten diagram
tabs = st.tabs([
    "🏛️ All Updates",
    "📚 Static Corner (8-10 Q)",
    "🇮🇳 National (Dynamic)",
    "🌐 International (Dynamic)",
    "🟡 Karnataka State (KEA)",
    "🎖️ Miscellaneous",
    "🐾 Species & Wildlife in News",
    "🗺️ Places in News & Maps",
    "📝 You to UPSC Quiz",
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

        with st.container():
            st.markdown(f"""
            <div class="news-card">
                <div>
                    <span class="source-pill">📡 {source_name}</span>
                    <span class="pillar-pill">📁 {pillar}</span>
                    <span class="subtopic-pill">🏷️ {sub_topic}</span>
                    <span class="pillar-pill" style="background:#f1f5f9; color:#334155;">{gs_tag}</span>
                    <span class="pillar-pill" style="background:#f8fafc; color:#64748b;">🏢 {ministry}</span>
                    {f'<span class="pillar-pill" style="background:#f8fafc; color:#64748b;">📅 {pub_date}</span>' if pub_date else ''}
                </div>
                <h3 style="margin-top: 12px; margin-bottom: 6px; color: #0f172a; font-size: 1.25rem; font-weight: 700;">{title}</h3>
                <p style="font-size: 1.05rem; line-height: 1.6; color: #334155; margin: 12px 0;">{summary}</p>
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

            st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed #e2e8f0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 1: ALL UPDATES
# -------------------------------------------------------------
with tabs[0]:
    st.subheader("🏛️ Complete Exam Current Affairs Stream")
    articles_all = database.get_recent_articles(
        limit=50,
        gs_filter=None if selected_gs == "All" else selected_gs,
        search_query=search_term if search_term.strip() else None,
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    render_article_cards(articles_all)

# -------------------------------------------------------------
# TAB 2: STATIC CORNER [8-10 Questions Weightage in Handwritten Tree]
# -------------------------------------------------------------
with tabs[1]:
    st.subheader("📚 Static Core [8-10 Questions Weightage]")
    st.caption("Essential Static foundations from your syllabus: Karnataka Budget • Karnataka Economic Survey • Karnataka Schemes • Central Schemes")

    c1, c2 = st.columns(2)
    with c1:
        kb = portal_content.STATIC_MODULES["karnataka_budget"]
        with st.container():
            st.markdown(f"""
            <div class="static-card">
                <span class="subtopic-pill" style="background:#fef3c7; color:#b45309;">{kb['weightage']}</span>
                <h3 style="color:#0f172a; margin: 10px 0;">📊 {kb['title']}</h3>
                <div style="font-size: 0.98rem; line-height: 1.7; color: #334155;">
                    {"<br>".join(kb['pointers'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        kes = portal_content.STATIC_MODULES["karnataka_economic_survey"]
        with st.container():
            st.markdown(f"""
            <div class="static-card">
                <span class="subtopic-pill" style="background:#e0e7ff; color:#3730a3;">{kes['weightage']}</span>
                <h3 style="color:#0f172a; margin: 10px 0;">📈 {kes['title']}</h3>
                <div style="font-size: 0.98rem; line-height: 1.7; color: #334155;">
                    {"<br>".join(kes['pointers'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        ks = portal_content.STATIC_MODULES["karnataka_schemes"]
        with st.container():
            st.markdown(f"""
            <div class="static-card" style="border-top-color: #10b981;">
                <span class="subtopic-pill" style="background:#d1fae5; color:#065f46;">{ks['weightage']}</span>
                <h3 style="color:#0f172a; margin: 10px 0;">🟡 {ks['title']}</h3>
                <div style="font-size: 0.98rem; line-height: 1.7; color: #334155;">
                    {"<br>".join(ks['pointers'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c4:
        cs = portal_content.STATIC_MODULES["central_schemes"]
        with st.container():
            st.markdown(f"""
            <div class="static-card" style="border-top-color: #3b82f6;">
                <span class="subtopic-pill" style="background:#dbeafe; color:#1e40af;">{cs['weightage']}</span>
                <h3 style="color:#0f172a; margin: 10px 0;">🇮🇳 {cs['title']}</h3>
                <div style="font-size: 0.98rem; line-height: 1.7; color: #334155;">
                    {"<br>".join(cs['pointers'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 3: NATIONAL (DYNAMIC)
# -------------------------------------------------------------
with tabs[2]:
    st.subheader("🇮🇳 National Current Affairs (Dynamic)")
    st.caption("Sub-Topics: Polity • Economy • Geography • Environment • History & Culture • Science & Tech • Health & Society")
    sub_nat = st.pills(
        "Filter National Sub-Topic:",
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
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    render_article_cards(articles_nat)

# -------------------------------------------------------------
# TAB 4: INTERNATIONAL (DYNAMIC)
# -------------------------------------------------------------
with tabs[3]:
    st.subheader("🌐 International Relations & Global Affairs")
    st.caption("Sub-Topics: I. Groupings (IORA, Quad, BRICS) • I. Organisations (UN, WTO, WHO, IMF) • Mapping (Places in News) • I. Summit")
    sub_intl = st.pills(
        "Filter International Sub-Topic:",
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
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    render_article_cards(articles_intl)

# -------------------------------------------------------------
# TAB 5: KARNATAKA STATE (KEA 20-25 QUESTIONS FOCUS)
# -------------------------------------------------------------
with tabs[4]:
    st.subheader("🟡 Karnataka State Specific Current Affairs")
    st.caption("Sub-Topics: Acts (2026) • Statutory Bodies • Policy • Schemes • Programmes & Campaigns • Apps & Portals")
    sub_kar = st.pills(
        "Filter Karnataka Sub-Topic:",
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
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    if not articles_kar:
        articles_kar = database.get_recent_articles(limit=50, source_filter="Karnataka State News")
    render_article_cards(articles_kar)

# -------------------------------------------------------------
# TAB 6: MISCELLANEOUS
# -------------------------------------------------------------
with tabs[5]:
    st.subheader("🎖️ Miscellaneous Section")
    st.caption("Sub-Topics: Sports • Awards • Committees • Reports and Index • Demise • Books & Authors • Persons in News")
    sub_misc = st.pills(
        "Filter Miscellaneous Sub-Topic:",
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
        date_filter=active_date_query,
        source_filter=active_source_query
    )
    render_article_cards(articles_misc)

# -------------------------------------------------------------
# TAB 7: SPECIES & WILDLIFE IN NEWS (ACCURATE ANIMAL VISUALS)
# -------------------------------------------------------------
with tabs[6]:
    st.subheader("🐾 Species & Wildlife in News (High-Yield Biodiversity)")
    st.caption("Accurate photography and official benchmarks: IUCN Red List Status, Wildlife Protection Act (WPA 1972) Schedule, CITES, and Karnataka Reserves.")

    for sp in portal_content.SPECIES_IN_NEWS:
        with st.container():
            col_img, col_info = st.columns([1.2, 2.2])
            with col_img:
                st.image(sp["image_url"], caption=sp["name"], use_container_width=True)
            with col_info:
                st.markdown(f"""
                <div class="species-card">
                    <h3 style="margin-top: 0; color: #047857; font-size: 1.3rem;">{sp['name']}</h3>
                    <p style="margin: 0; font-style: italic; color: #64748b; font-size: 0.95rem;">Scientific Name: {sp['scientific_name']}</p>
                    <div style="margin: 12px 0;">
                        <span style="background-color: {sp['iucn_badge_color']}; color: white; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.82rem;">IUCN: {sp['iucn_status']}</span>
                        <span style="background-color: #f3f4f6; color: #1f2937; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 0.82rem;">WPA: {sp['wpa_schedule']}</span>
                        <span style="background-color: #dbeafe; color: #1e40af; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 0.82rem;">CITES: {sp['cites']}</span>
                    </div>
                    <p style="font-size: 0.95rem; margin-bottom: 8px;"><b>🌿 Karnataka & Habitat Link:</b><br>{sp['karnataka_link']}</p>
                    <div style="background: #f0fdf4; border-left: 3px solid #10b981; padding: 10px; border-radius: 6px; font-size: 0.95rem;">
                        <b>🎯 Why in News (Exam Angle):</b><br>{sp['why_in_news']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed #cbd5e1;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 8: PLACES IN NEWS & INTERACTIVE MAPS
# -------------------------------------------------------------
with tabs[7]:
    st.subheader("🗺️ Places in News & Interactive Hotspot Map")
    st.caption("Active geopolitical choke points, maritime passages, historical heritage sites, and Karnataka landmarks.")

    places_data = portal_content.PLACES_IN_NEWS
    map_df = pd.DataFrame([
        {"lat": p["lat"], "lon": p["lon"], "name": p["name"]}
        for p in places_data
    ])

    st.markdown("#### 📍 Interactive Coordinates Map")
    st.map(map_df, zoom=3, use_container_width=True)

    st.markdown("#### 📌 Key Hotspot Profiles")
    for place in places_data:
        with st.container():
            st.markdown(f"""
            <div class="places-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #0891b2; font-size: 1.25rem;">📍 {place['name']}</h3>
                    <span style="background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 0.85rem;">{place['region']}</span>
                </div>
                <p style="margin-top: 10px; font-size: 0.98rem; color: #334155;"><b>Geo-Strategic Importance:</b> {place['importance']}</p>
                <div style="background: #f0fdfa; border-left: 3px solid #0891b2; padding: 10px; border-radius: 6px; font-size: 0.95rem;">
                    <b>🧭 UPSC & KEA Geographic Facts:</b><br>{place['upsc_kea_facts']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 9: YOU TO UPSC DAILY PRACTICE QUIZ
# -------------------------------------------------------------
with tabs[8]:
    st.subheader("📝 You to UPSC Daily Practice Quiz")
    st.caption("Official practice MCQs from your YouTube Channel (@youtoupsc) covering Karnataka Budget, KEA, and UPSC Prelims.")

    quiz_questions = portal_content.DAILY_QUIZ_QUESTIONS
    for q in quiz_questions:
        st.markdown(f"**Q{q['id']}.** {q['question']}")
        st.radio(
            f"Select your answer for Q{q['id']}:",
            q["options"],
            key=f"user_quiz_{q['id']}",
            index=None
        )
        with st.expander(f"🔍 Show Answer & Explanation (Q{q['id']})", expanded=False):
            correct_opt = q["options"][q["correct_index"]]
            st.markdown(f"**Correct Answer:** `{correct_opt}`")
            st.info(f"**Detailed Explanation:**\n\n{q['explanation']}")
        st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px dashed #e2e8f0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 10: EXAM ANALYTICS & TRENDS
# -------------------------------------------------------------
with tabs[9]:
    st.subheader("📊 Syllabus Coverage & Weightage Analytics")
    stats = database.get_dashboard_stats()

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### 📁 Pillar Breakdown")
        pillar_df = pd.DataFrame(list(stats.get("pillars", {}).items()), columns=["Pillar", "Articles"])
        st.bar_chart(pillar_df.set_index("Pillar"), color="#2563eb")

    with col_g2:
        st.markdown("#### 🏛 GS Paper Weightage")
        gs_df = pd.DataFrame(list(stats.get("gs_papers", {}).items()), columns=["GS Paper", "Articles"])
        st.bar_chart(gs_df.set_index("GS Paper"), color="#f59e0b")

    st.markdown("#### 🏢 Top Ministries in Focus")
    ministries_data = stats.get("top_ministries", stats.get("ministries", {}))
    if ministries_data:
        min_df = pd.DataFrame(list(ministries_data.items()), columns=["Ministry", "Articles"])
        st.bar_chart(min_df.set_index("Ministry"), color="#10b981")
    else:
        st.info("Ministry data will populate after fresh news is ingested.")
