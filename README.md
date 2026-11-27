# 🏛 PIB UPSC Agentic AI App

A 100% free, automated Agentic AI application that continuously monitors the **Press Information Bureau (PIB)** website, intelligently filters out exam-irrelevant noise, tags releases according to the **UPSC Civil Services Syllabus (GS-1, GS-2, GS-3, GS-4, Prelims)**, generates concise 60-word "Inshorts-style" summaries with Prelims/Mains pointers, and delivers them via **Telegram push notifications** and an **interactive Web Dashboard**, complete with direct clickable links to the original PIB releases.

---

## 🌟 Key Features

1. **Continuous PIB Monitoring**:
   - Fetches official English press releases from `pib.gov.in`.
   - Built-in anti-blocking headers and automatic deduplication via SQLite.
2. **Multi-Stage Agentic AI (Powered by Google Gemini 2.5 Flash Free Tier)**:
   - **Relevance Gatekeeper**: Drops routine protocol greetings, minor transfers, and political rallies.
   - **Syllabus Mapper**: Classifies news into GS-1, GS-2, GS-3, GS-4, or Prelims Pointer.
   - **Inshorts Summarizer**: Generates 60–80 word summaries, 2–3 high-yield Prelims facts, and 1 Mains dimension.
3. **Dual Delivery Interface**:
   - **Mobile Push (Telegram)**: Real-time formatted cards on your phone with inline button `[📖 Read Full PIB Article]` linking directly to PIB.
   - **Web App (Streamlit)**: Modern dashboard with GS syllabus filters, keyword search, and on-demand sync.
4. **100% Free 24/7 Cloud Automation**:
   - Includes a ready-to-use **GitHub Actions** cron workflow that runs automatically in the cloud every hour with zero hosting costs.

---

## 🚀 Quick Setup Guide

### 1. Install Dependencies
In your terminal or PowerShell inside `c:\pib notification`:
```bash
pip install -r requirements.txt
```

### 2. Configure Free Keys
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in:
```env
# 1. Free Gemini API Key: Get from https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here

# 2. Telegram Bot Token:
# - Open Telegram, search for @BotFather
# - Send /newbot, give it a name and username
# - Copy the API token given by BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# 3. Your Telegram Chat ID or Channel:
# - Send any message to your new bot
# - Open in browser: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
# - Look for "chat":{"id": 123456789...} and copy that number here
# - (Or if using a public channel, write @your_channel_name)
TELEGRAM_CHAT_ID=your_chat_id_here

# Check interval in minutes
CHECK_INTERVAL_MINUTES=30
```

---

## 💻 How to Run

### Option A: Launch the Web Dashboard (Streamlit)
```bash
streamlit run web_app.py
```
- Open your browser at `http://localhost:8501`.
- Browse filtered UPSC news cards.
- Click **"🔄 Check & Fetch Latest PIB News"** in the sidebar anytime for an instant manual check.
- Click **"🔗 Open on PIB Page"** on any card to navigate directly to the official release.

### Option B: Run Continuous Background Monitor & Telegram Bot
```bash
python main.py
```
- Keeps running continuously in the background.
- Scrapes PIB every 30 minutes (configurable).
- Automatically posts every UPSC-relevant release to your Telegram phone app.

### Option C: 24/7 Cloud Automation (Zero Hosting Cost via GitHub Actions)
1. Push this repository to a private GitHub repo.
2. In your GitHub repository:
   - Go to **Settings > Secrets and variables > Actions > New repository secret**.
   - Add `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID`.
3. The workflow in `.github/workflows/monitor.yml` will automatically run every hour 24/7 for free!

---

## 📁 File Structure

| File | Purpose |
| :--- | :--- |
| `web_app.py` | Streamlit interactive web dashboard with filters and cards |
| `main.py` | Background monitor & scheduler |
| `scraper.py` | PIB RSS and article parser with custom browser headers |
| `agent.py` | Multi-stage Gemini 2.5 Flash agentic analyzer |
| `database.py` | SQLite persistence and deduplication engine |
| `telegram_notifier.py` | Formats and dispatches cards to Telegram with buttons |
| `config.py` | Settings & environment loader |
| `.github/workflows/monitor.yml` | 24/7 free cloud cron workflow |
