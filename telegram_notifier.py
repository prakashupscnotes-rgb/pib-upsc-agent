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
        gs_paper = html.escape(str(article.get("gs_paper", "UPSC GS")))
        subject_group = html.escape(str(article.get("subject_group", "General Affairs")))
        title = html.escape(str(article.get("title", "")))
        ministry = html.escape(str(article.get("ministry", "Government of India")))
        summary = html.escape(str(article.get("short_summary", "")))
        prelims = html.escape(str(article.get("prelims_facts", "")))
        mains = html.escape(str(article.get("mains_pointer", "")))
        link = article.get("link", config.PIB_BASE_URL)
        if "pib.gov.in" in link and "lang=" not in link.lower():
            link += "&lang=1" if "?" in link else "?lang=1"

        msg = (
            f"🏛 <b>{gs_paper}</b> • <b>{subject_group}</b>\n"
            f"🏢 <i>{ministry}</i>\n\n"
            f"📌 <b>{title}</b>\n\n"
            f"📝 <b>Short Summary:</b>\n{summary}\n\n"
        )

        if prelims and prelims.strip():
            msg += f"🎯 <b>Prelims High-Yield Facts:</b>\n{prelims}\n\n"

        if mains and mains.strip():
            msg += f"💡 <b>Mains Dimension:</b>\n{mains}\n\n"

        msg += f"🔗 <a href=\"{link}\">Click here to open PIB Release</a>"
        return msg

    def send_article(self, article: Dict[str, Any]) -> bool:
        """
        Sends the article to Telegram channel or chat with an inline button.
        """
        if not self.is_configured():
            print("[Telegram] Bot token or Chat ID not configured. Skipping telegram send.")
            return False

        message_html = self.format_message(article)
        link = article.get("link", config.PIB_BASE_URL)

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message_html,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "📖 Read Full PIB Article", "url": link}
                    ]
                ]
            }
        }

        try:
            if REQUESTS_AVAILABLE:
                response = requests.post(url, json=payload, timeout=10)
                data = response.json()
            else:
                req_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=req_data,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

            if data.get("ok"):
                print(f"[Telegram] Successfully posted: {article.get('title')[:40]}...")
                return True
            else:
                print(f"[Telegram] Failed to send message: {data.get('description')}")
                return False
        except Exception as e:
            print(f"[Telegram] Error sending message: {e}")
            return False

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
