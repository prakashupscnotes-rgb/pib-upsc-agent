import time
from datetime import datetime
import config
import database
from scraper import PIBScraper
from agent import UPSCNewsAgent
from telegram_notifier import TelegramNotifier

def run_pipeline():
    """
    Executes one complete monitoring and analysis cycle:
    1. Fetches latest releases from PIB RSS
    2. Filters already processed articles
    3. Runs Agentic AI for UPSC relevance, GS classification & summary
    4. Saves to database
    5. Sends instant push notification via Telegram with direct PIB link
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] --- Starting PIB UPSC Monitor Cycle ---")

    scraper = PIBScraper()
    agent = UPSCNewsAgent()
    notifier = TelegramNotifier()

    # 1. Fetch releases
    releases = scraper.fetch_latest_releases_from_rss()
    print(f"[{timestamp}] Retrieved {len(releases)} items from PIB RSS feed.")

    processed = 0
    relevant_found = 0

    for item in releases:
        prid = item["pib_id"]
        link = item["link"]
        title = item["title"]

        # Check if already processed
        if database.is_article_processed(prid):
            continue

        print(f"\n[New Release] Processing PRID {prid}: {title[:60]}...")

        # 2. Extract full text
        details = scraper.fetch_article_full_content(link)
        content = details["content"] or item.get("initial_desc", "")
        ministry = details["ministry"]

        # 3. Agentic AI Evaluation
        analysis = agent.analyze(title=title, ministry=ministry, content=content)
        is_relevant = analysis.get("is_relevant", False)

        # Use English-refined title, ministry and subject
        clean_title = analysis.get("title_en") or title
        clean_ministry = analysis.get("ministry_en") or ministry
        clean_subject = analysis.get("subject_group") or "General"

        # 4. Save to Database
        database.save_article(
            pib_id=prid,
            title=clean_title,
            ministry=clean_ministry,
            link=link,
            raw_content=content,
            is_relevant=is_relevant,
            gs_paper=analysis.get("gs_paper", ""),
            subject_group=clean_subject,
            short_summary=analysis.get("short_summary", ""),
            prelims_facts=analysis.get("prelims_facts", ""),
            mains_pointer=analysis.get("mains_pointer", ""),
            published_date=details.get("date") or item.get("published_date", "")
        )

        if is_relevant:
            relevant_found += 1
            print(f"  -> ✅ RELEVANT: Tagged as {analysis.get('gs_paper')} [{clean_subject}] | {clean_title[:50]}...")

            # 5. Send via Telegram Bot (100% English)
            article_payload = {
                "title": clean_title,
                "ministry": clean_ministry,
                "link": link,
                "gs_paper": analysis.get("gs_paper", ""),
                "subject_group": clean_subject,
                "short_summary": analysis.get("short_summary", ""),
                "prelims_facts": analysis.get("prelims_facts", ""),
                "mains_pointer": analysis.get("mains_pointer", "")
            }
            if notifier.is_configured():
                sent = notifier.send_article(article_payload)
                if sent:
                    database.mark_telegram_sent(prid)
        else:
            print(f"  -> ⏭ Filtered out: {analysis.get('relevance_reason', 'Not relevant to UPSC')}")

        processed += 1

    print(f"[{timestamp}] Cycle Finished. Processed {processed} new releases ({relevant_found} marked relevant for UPSC).")

def main():
    database.init_db()
    print("=====================================================")
    print("  🏛 PIB UPSC Continuous Agentic AI Monitor Started  ")
    print(f"  Interval: Every {config.CHECK_INTERVAL_MINUTES} minutes")
    print("=====================================================")

    # Run immediate cycle on launch
    run_pipeline()

    # Continuous loop
    interval_seconds = config.CHECK_INTERVAL_MINUTES * 60
    while True:
        try:
            time.sleep(interval_seconds)
            run_pipeline()
        except KeyboardInterrupt:
            print("\n[Monitor] Stopping background scheduler.")
            break
        except Exception as e:
            print(f"\n[Monitor] Unexpected error during loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
