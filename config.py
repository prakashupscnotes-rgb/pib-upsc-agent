import os
from pathlib import Path

# Load .env file safely without requiring python-dotenv
BASE_DIR = Path(__file__).resolve().parent
env_file = BASE_DIR / ".env"

if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        # Fallback basic .env parser
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())

# API Keys & Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Database path
DB_PATH = BASE_DIR / "pib_upsc.db"

# Scraper Settings
PIB_BASE_URL = "https://pib.gov.in"
PIB_ALL_RELEASES_URL = "https://pib.gov.in/allRel.aspx"
PIB_RSS_ENGLISH = "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1"

# Request Headers to avoid 403 Forbidden
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
    "Referer": "https://pib.gov.in/",
    "Connection": "keep-alive",
}

# Monitoring interval in minutes
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
