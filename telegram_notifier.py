import html
import json
from typing import Dict, Any
import config

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    import urllib.request
    REQUESTS_AVAILABLE = False

class TelegramNotifier:
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID

    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id and self.bot_token != "your_telegram_bot_token_here")

    def format_message(self, article: Dict[str, Any]) -> str:
        """
        Formats article into a clean, readable Inshorts-style HTML card.
        """
        source = html.escape(str(article.get("source_name", "PIB (Official)")))
        pillar = html.escape(str(article.get("main_pillar", "National")))
        sub_topic = html.escape(str(article.get("sub_topic", "General")))
        gs_paper = html.escape(str(article.get("gs_paper", "UPSC GS")))
        title = html.escape(str(article.get("title", "")))
        ministry = html.escape(str(article.get("ministry", "Government of India")))
        summary = html.escape(str(article.get("short_summary", "")))
        prelims = html.escape(str(article.get("prelims_facts", "")))
        mains = html.escape(str(article.get("mains_pointer", "")))
        link = article.get("link", config.PIB_BASE_URL)
        if "pib.gov.in" in link and "lang=" not in link.lower():
            link += "&lang=1" if "?" in link else "?lang=1"

        msg = (
            f"📡 <b>{source}</b> | 📁 <b>{pillar}</b> › <i>{sub_topic}</i>\n"
            f"🏛 <b>{gs_paper}</b> • 🏢 <i>{ministry}</i>\n\n"
            f"📌 <b>{title}</b>\n\n"
            f"📝 <b>Short Summary:</b>\n{summary}\n\n"
        )

        if prelims and prelims.strip():
            msg += f"🎯 <b>Prelims High-Yield Facts:</b>\n{prelims}\n\n"

        if mains and mains.strip():
            msg += f"💡 <b>Mains Dimension:</b>\n{mains}\n\n"

        msg += f"🔗 <a href=\"{link}\">Click here to open Full Article</a>"
        return msg

    def send_article(self, article: Dict[str, Any]) -> bool:
        """
        Sends the article to Telegram channel(s) or chat(s) with an inline button.
        Supports single ID, comma-separated IDs, or Channel (@channelname / -100...).
        """
        if not self.is_configured():
            print("[Telegram] Bot token or Chat ID not configured. Skipping telegram send.")
            return False

        message_html = self.format_message(article)
        link = article.get("link", config.PIB_BASE_URL)
        yt_link = article.get("youtube_link", "")
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        buttons = [
            {"text": "📖 Read Official Article", "url": link}
        ]
        if yt_link and yt_link.strip():
            buttons.append({"text": "▶️ Watch on YouTube", "url": yt_link})

        chat_ids = [cid.strip() for cid in str(self.chat_id).split(",") if cid.strip()]
        any_success = False

        for cid in chat_ids:
            payload = {
                "chat_id": cid,
                "text": message_html,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
                "reply_markup": {
                    "inline_keyboard": [buttons]
                }
            }

            try:
                if REQUESTS_AVAILABLE:
                    response = requests.post(url, json=payload, timeout=10)
                    if response.status_code == 200:
                        any_success = True
                    else:
                        print(f"[Telegram] Failed to send to {cid}: {response.text}")
                else:
                    import urllib.request
                    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        if resp.status == 200:
                            any_success = True
            except Exception as e:
                print(f"[Telegram] Error sending to {cid}: {e}")

        return any_success

if __name__ == "__main__":
    notifier = TelegramNotifier()
    sample = {
        "title": "Cabinet approves PM-PRANAM scheme",
        "ministry": "Ministry of Chemicals & Fertilizers",
        "gs_paper": "GS-3",
        "short_summary": "The Union Cabinet has approved the PM-PRANAM initiative to incentivize states promoting alternate fertilizers and balanced use of chemical fertilizers.",
        "prelims_facts": "• Outlay: Funded via savings in fertilizer subsidies\n• Focus: Bio-fertilizers & organic farming",
        "mains_pointer": "Crucial for fiscal sustainability of farm subsidies and soil rejuvenation.",
        "link": "https://pib.gov.in"
    }
    print("Formatted Preview:\n")
    print(notifier.format_message(sample))
