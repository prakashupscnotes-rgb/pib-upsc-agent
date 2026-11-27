import streamlit as st
import database

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
    }
    .summary-text {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1f2937;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

# Ensure database exists
database.init_db()

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

                analysis = agent.analyze(item["title"], ministry, content)
                is_relevant = analysis.get("is_relevant", False)

                clean_title = analysis.get("title_en") or item["title"]
                clean_ministry = analysis.get("ministry_en") or ministry
                clean_subject = analysis.get("subject_group") or "General"

                database.save_article(
                    pib_id=prid,
                    title=clean_title,
                    ministry=clean_ministry,
                    link=item["link"],
                    raw_content=content,
                    is_relevant=is_relevant,
                    gs_paper=analysis.get("gs_paper", ""),
                    subject_group=clean_subject,
                    short_summary=analysis.get("short_summary", ""),
                    prelims_facts=analysis.get("prelims_facts", ""),
                    mains_pointer=analysis.get("mains_pointer", ""),
                    published_date=item.get("published_date", "")
                )

                if is_relevant:
                    relevant_count += 1
                    article_payload = {
                        "title": clean_title,
                        "ministry": clean_ministry,
                        "link": item["link"],
                        "gs_paper": analysis.get("gs_paper", ""),
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
            st.sidebar.warning(f"Notice: {e}")

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
selected_subject = st.sidebar.selectbox("Filter by Subject Group", subject_options)

db_subject_filter = None
if selected_subject != "All Subjects":
    db_subject_filter = selected_subject.split(" ", 1)[-1].strip()

gs_choice = st.sidebar.selectbox(
    "Filter by GS Syllabus",
    ["All", "GS-1", "GS-2", "GS-3", "GS-4", "Prelims Pointer"]
)

search_term = st.sidebar.text_input("Search Topics / Ministry", placeholder="e.g. DRDO, ISRO, RBI, Health...")

# Main Content Area
st.title("📰 PIB Daily UPSC Digest")
st.markdown("Exam-oriented daily summaries categorized by **GS Paper** & **Subject Group** with direct official English PIB links.")

# Quick subject pills
st.caption("Quick Subject Filter:")
cols = st.columns(4)
with cols[0]:
    if st.button("🛡️ Defence", use_container_width=True):
        db_subject_filter = "Defence & Security"
with cols[1]:
    if st.button("🚀 Science & Tech", use_container_width=True):
        db_subject_filter = "Science & Technology"
with cols[2]:
    if st.button("💰 Economy", use_container_width=True):
        db_subject_filter = "Economy & Infrastructure"
with cols[3]:
    if st.button("🌾 Environment", use_container_width=True):
        db_subject_filter = "Environment & Agriculture"

# Fetch articles from database
articles = database.get_recent_articles(
    limit=50,
    gs_filter=None if gs_choice == "All" else gs_choice,
    subject_filter=db_subject_filter,
    search_query=search_term if search_term.strip() else None
)

if not articles:
    st.info("No articles in database yet. Click '🔄 Check & Fetch Latest PIB News' in the sidebar to fetch today's releases!")
else:
    st.write(f"Showing **{len(articles)}** curated articles.")

    for art in articles:
        gs_tag = art.get("gs_paper") or "UPSC GS"
        subject_group = art.get("subject_group") or "General Affairs"
        ministry = art.get("ministry") or "Government of India"
        title = art.get("title", "")
        summary = art.get("short_summary", "")
        prelims = art.get("prelims_facts", "")
        mains = art.get("mains_pointer", "")
        link = art.get("link", "#")
        if "pib.gov.in" in link and "lang=" not in link.lower():
            link += "&lang=1" if "?" in link else "?lang=1"
        pub_date = art.get("published_date", "")

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
