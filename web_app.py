import streamlit as st
import re
import importlib
import database
importlib.reload(database)

st.set_page_config(
    page_title="PIB Daily UPSC Digest",
    page_icon="🏛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern card styling
st.markdown("""
<style>
    .reportview-container {
        background: #f7f9fc;
    }
    .news-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-left: 5px solid #1e40af;
    }
    .gs-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
        background-color: #e0e7ff;
        color: #3730a3;
        margin-right: 8px;
    }
    .ministry-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        background-color: #f3f4f6;
        color: #4b5563;
        margin-right: 8px;
    }
    .summary-text {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1f2937;
        margin: 14px 0;
    }
</style>
""", unsafe_allow_html=True)

# Ensure database exists
database.init_db()

# Start 24/7 Cloud Background Monitor (Runs continuously on Render even when laptop is off)
import threading
import time

def start_cloud_background_monitor():
    def monitor_loop():
        time.sleep(10)  # Initial grace period on startup
        try:
            import main
            while True:
                main.run_pipeline()
                time.sleep(1800)  # Run every 30 minutes
        except Exception as ex:
            print(f"[Cloud Background Monitor] Notice: {ex}")

    if not hasattr(st, "_pib_cloud_monitor_started"):
        st._pib_cloud_monitor_started = True
        worker = threading.Thread(target=monitor_loop, daemon=True, name="PIBCloudWorker")
        worker.start()
        print("[Cloud] 24/7 Background PIB monitor worker started!")

start_cloud_background_monitor()

# Initialize session state for active filters
if "selected_subject" not in st.session_state:
    st.session_state["selected_subject"] = "All Subjects"
if "selected_gs" not in st.session_state:
    st.session_state["selected_gs"] = "All"

# Sidebar
st.sidebar.title("🏛 PIB UPSC Agent")
st.sidebar.caption("Continuous PIB Monitor & AI UPSC Summarizer")

# On-demand refresh button
if st.sidebar.button("🔄 Check & Fetch Latest PIB News", use_container_width=True):
    with st.spinner("Scraping PIB & Running Agentic AI Filter..."):
        try:
            from scraper import PIBScraper
            from agent import UPSCNewsAgent
            from telegram_notifier import TelegramNotifier

            scraper = PIBScraper()
            agent = UPSCNewsAgent()
            notifier = TelegramNotifier()

            new_items = scraper.fetch_latest_releases_from_rss()
            processed_count = 0
            relevant_count = 0

            for item in new_items:
                prid = item["pib_id"]
                if database.is_article_processed(prid):
                    continue

                details = scraper.fetch_article_full_content(item["link"])
                content = details["content"] or item.get("initial_desc", "")
                ministry = details["ministry"]
                title = details.get("title") or item["title"]
                actual_link = details.get("english_url") or item["link"]
                actual_date = details.get("date") or item.get("published_date", "")

                analysis = agent.analyze(title, ministry, content)
                is_relevant = analysis.get("is_relevant", False)

                clean_title = analysis.get("title_en") or title
                clean_ministry = analysis.get("ministry_en") or ministry
                clean_subject = analysis.get("subject_group") or "General"
                clean_gs = analysis.get("gs_paper") or "GS-2"
                if clean_gs.strip().lower() == "none":
                    clean_gs = "GS-2"

                database.save_article(
                    pib_id=prid,
                    title=clean_title,
                    ministry=clean_ministry,
                    link=actual_link,
                    raw_content=content,
                    is_relevant=is_relevant,
                    gs_paper=clean_gs,
                    subject_group=clean_subject,
                    short_summary=analysis.get("short_summary", ""),
                    prelims_facts=analysis.get("prelims_facts", ""),
                    mains_pointer=analysis.get("mains_pointer", ""),
                    published_date=actual_date
                )

                if is_relevant:
                    relevant_count += 1
                    article_payload = {
                        "title": clean_title,
                        "ministry": clean_ministry,
                        "link": actual_link,
                        "gs_paper": clean_gs,
                        "subject_group": clean_subject,
                        "short_summary": analysis.get("short_summary", ""),
                        "prelims_facts": analysis.get("prelims_facts", ""),
                        "mains_pointer": analysis.get("mains_pointer", "")
                    }
                    if notifier.is_configured():
                        if notifier.send_article(article_payload):
                            database.mark_telegram_sent(prid)

                processed_count += 1

            st.sidebar.success(f"Processed {processed_count} releases ({relevant_count} relevant for UPSC).")
        except Exception as e:
            st.sidebar.warning(f"Live fetch notice: {e}")

# 1-Click Auto-Sync to GitHub (Optional for local development)
try:
    import sync_github
    gh_token = sync_github.get_github_token()
    HAS_SYNC = True
except ImportError:
    gh_token = ""
    HAS_SYNC = False

if HAS_SYNC and gh_token:
    with st.sidebar.expander("☁️ Auto-Sync to GitHub", expanded=False):
        st.caption("Connected to `prakashupscnotes-rgb/pib-upsc-agent`")
        if st.button("🚀 Push All Updates to GitHub", use_container_width=True):
            with st.spinner("Syncing all code, database & fixes to GitHub..."):
                res = sync_github.sync_all_files(gh_token)
                ok_count = sum(1 for v in res.values() if v)
                if ok_count > 0:
                    st.success(f"Synced {ok_count} files to GitHub!")
                else:
                    st.error("Sync failed. Check token permissions.")

# Filter Section
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 UPSC Filters")

subject_options = [
    "All Subjects",
    "🛡️ Defence & Security",
    "🚀 Science & Technology",
    "💰 Economy & Infrastructure",
    "🌾 Environment & Agriculture",
    "⚖️ Polity & Governance",
    "🌐 International Relations",
    "🤝 Social Justice & Health",
    "🏛️ Art & Culture"
]

current_subj_idx = subject_options.index(st.session_state["selected_subject"]) if st.session_state["selected_subject"] in subject_options else 0
selected_subject = st.sidebar.selectbox("Filter by Subject Group", subject_options, index=current_subj_idx)
st.session_state["selected_subject"] = selected_subject

# Strip emoji for DB query
db_subject_filter = None
if selected_subject != "All Subjects":
    db_subject_filter = selected_subject.split(" ", 1)[-1].strip()

gs_options = ["All", "GS-1", "GS-2", "GS-3", "GS-4", "Prelims Pointer"]
current_gs_idx = gs_options.index(st.session_state["selected_gs"]) if st.session_state["selected_gs"] in gs_options else 0
gs_choice = st.sidebar.selectbox("Filter by GS Syllabus", gs_options, index=current_gs_idx)
st.session_state["selected_gs"] = gs_choice

search_term = st.sidebar.text_input("Search Topics / Ministry", placeholder="e.g. DRDO, ISRO, RBI, Health...")

# Global Device Access Pill in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("📱 **Live Cloud Access (Any Device / Internet):**")
st.sidebar.success("""
Open anywhere on mobile, tablet, or PC:  
👉 **`https://pib-upsc-agent.onrender.com`**
""")

# Main Content Area
st.title("📰 PIB Daily UPSC Digest")
st.markdown("Exam-oriented daily summaries categorized by **GS Paper** & **Subject Group** with direct official English PIB links.")

# Quick subject pills at the top
st.caption(f"Quick Subject Filter (Active: **{selected_subject}**):")
cols = st.columns(5)
with cols[0]:
    if st.button("🌐 All", use_container_width=True):
        st.session_state["selected_subject"] = "All Subjects"
        st.rerun()
with cols[1]:
    if st.button("🛡️ Defence", use_container_width=True):
        st.session_state["selected_subject"] = "🛡️ Defence & Security"
        st.rerun()
with cols[2]:
    if st.button("🚀 Science", use_container_width=True):
        st.session_state["selected_subject"] = "🚀 Science & Technology"
        st.rerun()
with cols[3]:
    if st.button("💰 Economy", use_container_width=True):
        st.session_state["selected_subject"] = "💰 Economy & Infrastructure"
        st.rerun()
with cols[4]:
    if st.button("🤝 Health / Justice", use_container_width=True):
        st.session_state["selected_subject"] = "🤝 Social Justice & Health"
        st.rerun()

# Fetch articles from database with fail-safe fallback
try:
    articles = database.get_recent_articles(
        limit=50,
        gs_filter=None if gs_choice == "All" else gs_choice,
        subject_filter=db_subject_filter,
        search_query=search_term if search_term.strip() else None
    )
except TypeError:
    articles = database.get_recent_articles(
        limit=50,
        gs_filter=None if gs_choice == "All" else gs_choice,
        search_query=search_term if search_term.strip() else None
    )

if not articles:
    st.info("No articles found matching your criteria. Try switching subject filters or click **'🔄 Check & Fetch Latest PIB News'** in the sidebar!")
else:
    st.write(f"Showing **{len(articles)}** curated articles.")

    for art in articles:
        gs_tag = art.get("gs_paper") or "GS-2"
        if gs_tag.strip().lower() == "none":
            gs_tag = "GS-2"

        subject_group = art.get("subject_group") or "General"
        ministry = art.get("ministry") or "Government of India"
        title = art.get("title", "")
        summary = art.get("short_summary", "")
        prelims = art.get("prelims_facts", "")
        mains = art.get("mains_pointer", "")

        # Clean date string
        pub_date = art.get("published_date", "")
        if pub_date:
            pub_date = re.sub(r"^प्रविष्टि\s*तिथि:\s*", "", pub_date).strip()
            pub_date = re.sub(r"^Posted\s*On:\s*", "", pub_date, flags=re.I).strip()
            pub_date = re.sub(r"^Release ID:\s*\d+,?\s*", "", pub_date, flags=re.I).strip()

        # Build official English PIB link
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
                    <span class="gs-badge">{gs_tag}</span>
                    <span class="gs-badge" style="background-color: #fef3c7; color: #92400e;">🏷️ {subject_group}</span>
                    <span class="ministry-badge">🏢 {ministry}</span>
                    {f'<span class="ministry-badge">📅 {pub_date}</span>' if pub_date else ''}
                </div>
                <h3 style="margin-top: 10px; margin-bottom: 5px; color: #111827;">{title}</h3>
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
                st.link_button("🔗 Open on PIB (English)", url=link, use_container_width=True)

            st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed #e5e7eb;'>", unsafe_allow_html=True)
