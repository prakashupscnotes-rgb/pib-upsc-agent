import streamlit as st
import database
from scraper import PIBScraper
from agent import UPSCNewsAgent
from telegram_notifier import TelegramNotifier

st.set_page_config(
    page_title="PIB Daily UPSC Agent",
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
    .meta-box {
        background: #f9fafb;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 10px;
        font-size: 0.95rem;
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

            # Fetch full details
            details = scraper.fetch_article_full_content(item["link"])
            content = details["content"] or item.get("initial_desc", "")
            ministry = details["ministry"]

            # Run Agentic AI analysis
            analysis = agent.analyze(item["title"], ministry, content)
            is_relevant = analysis.get("is_relevant", False)

            database.save_article(
                pib_id=prid,
                title=item["title"],
                ministry=ministry,
                link=item["link"],
                raw_content=content,
                is_relevant=is_relevant,
                gs_paper=analysis.get("gs_paper", ""),
                short_summary=analysis.get("short_summary", ""),
                prelims_facts=analysis.get("prelims_facts", ""),
                mains_pointer=analysis.get("mains_pointer", ""),
                published_date=item.get("published_date", "")
            )

            if is_relevant:
                relevant_count += 1
                # Trigger telegram if configured
                article_payload = {
                    "title": item["title"],
                    "ministry": ministry,
                    "link": item["link"],
                    "gs_paper": analysis.get("gs_paper", ""),
                    "short_summary": analysis.get("short_summary", ""),
                    "prelims_facts": analysis.get("prelims_facts", ""),
                    "mains_pointer": analysis.get("mains_pointer", "")
                }
                if notifier.is_configured():
                    if notifier.send_article(article_payload):
                        database.mark_telegram_sent(prid)

            processed_count += 1

        st.sidebar.success(f"Processed {processed_count} releases ({relevant_count} relevant for UPSC).")

# Filter Section
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")
gs_choice = st.sidebar.selectbox(
    "Filter by Syllabus",
    ["All", "GS-1", "GS-2", "GS-3", "GS-4", "Prelims Pointer"]
)

search_term = st.sidebar.text_input("Search Topics / Ministry", placeholder="e.g. RBI, ISRO, Health...")

# Main Content Area
st.title("📰 PIB Inshorts for UPSC Civil Services")
st.markdown("Automated, exam-oriented daily digest filtered and summarized from official Press Information Bureau releases.")

# Fetch articles from database
articles = database.get_recent_articles(
    limit=50,
    gs_filter=None if gs_choice == "All" else gs_choice,
    search_query=search_term if search_term.strip() else None
)

if not articles:
    st.info("No articles found matching your criteria. Click **'🔄 Check & Fetch Latest PIB News'** in the sidebar to scrape and process the latest releases!")
else:
    st.write(f"Showing **{len(articles)}** curated articles.")

    for art in articles:
        gs_tag = art.get("gs_paper") or "UPSC GS"
        ministry = art.get("ministry") or "Government of India"
        title = art.get("title", "")
        summary = art.get("short_summary", "")
        prelims = art.get("prelims_facts", "")
        mains = art.get("mains_pointer", "")
        link = art.get("link", "#")
        pub_date = art.get("published_date", "")

        with st.container():
            st.markdown(f"""
            <div class="news-card">
                <div>
                    <span class="gs-badge">{gs_tag}</span>
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
                st.link_button("🔗 Open on PIB Page", url=link, use_container_width=True)

            st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed #e5e7eb;'>", unsafe_allow_html=True)
