import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Any
import config

def get_connection():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pib_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            ministry TEXT,
            link TEXT NOT NULL,
            raw_content TEXT,
            is_relevant INTEGER DEFAULT 0,
            gs_paper TEXT,
            subject_group TEXT DEFAULT 'General',
            short_summary TEXT,
            prelims_facts TEXT,
            mains_pointer TEXT,
            telegram_sent INTEGER DEFAULT 0,
            published_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add columns if upgrading existing database
    for col, col_type in [
        ("subject_group", "TEXT DEFAULT 'General'"),
        ("main_pillar", "TEXT DEFAULT 'National'"),
        ("sub_topic", "TEXT DEFAULT 'General'"),
        ("source_name", "TEXT DEFAULT 'PIB (Official)'"),
        ("image_url", "TEXT DEFAULT ''"),
        ("image_verified", "INTEGER DEFAULT 1"),
        ("content_verified", "INTEGER DEFAULT 1")
    ]:
        try:
            c.execute(f"ALTER TABLE articles ADD COLUMN {col} {col_type}")
        except Exception:
            pass
    conn.commit()
    conn.close()

def is_article_processed(pib_id: str) -> bool:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM articles WHERE pib_id = ?", (pib_id,))
    row = c.fetchone()
    conn.close()
    return row is not None

def save_article(
    pib_id: str,
    title: str,
    ministry: str,
    link: str,
    raw_content: str,
    is_relevant: bool,
    gs_paper: str = "",
    subject_group: str = "General",
    short_summary: str = "",
    prelims_facts: str = "",
    mains_pointer: str = "",
    published_date: str = "",
    main_pillar: str = "National",
    sub_topic: str = "General",
    source_name: str = "PIB (Official)",
    image_url: str = ""
) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO articles (
            pib_id, title, ministry, link, raw_content,
            is_relevant, gs_paper, subject_group, short_summary,
            prelims_facts, mains_pointer, published_date,
            main_pillar, sub_topic, source_name, image_url,
            image_verified, content_verified
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
        ON CONFLICT(pib_id) DO UPDATE SET
            is_relevant = excluded.is_relevant,
            gs_paper = excluded.gs_paper,
            subject_group = excluded.subject_group,
            short_summary = excluded.short_summary,
            prelims_facts = excluded.prelims_facts,
            mains_pointer = excluded.mains_pointer,
            main_pillar = excluded.main_pillar,
            sub_topic = excluded.sub_topic,
            source_name = excluded.source_name,
            image_url = CASE WHEN excluded.image_url != '' THEN excluded.image_url ELSE articles.image_url END,
            image_verified = 1,
            content_verified = 1
    """, (
        pib_id, title, ministry, link, raw_content,
        1 if is_relevant else 0, gs_paper, subject_group, short_summary,
        prelims_facts, mains_pointer, published_date,
        main_pillar, sub_topic, source_name, image_url
    ))
    conn.commit()
    inserted_id = c.lastrowid
    conn.close()
    return inserted_id

def update_article_verification(
    pib_id: str,
    title: str,
    short_summary: str,
    prelims_facts: str,
    mains_pointer: str,
    image_url: str,
    image_verified: int = 1,
    content_verified: int = 1
):
    """Updates an article after passing through the Overhead Flow Path Inspector."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE articles SET
            title = ?,
            short_summary = ?,
            prelims_facts = ?,
            mains_pointer = ?,
            image_url = ?,
            image_verified = ?,
            content_verified = ?
        WHERE pib_id = ?
    """, (title, short_summary, prelims_facts, mains_pointer, image_url, image_verified, content_verified, pib_id))
    conn.commit()
    conn.close()

def mark_telegram_sent(pib_id: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE articles SET telegram_sent = 1 WHERE pib_id = ?", (pib_id,))
    conn.commit()
    conn.close()

def get_unsent_relevant_articles() -> List[Dict]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM articles 
        WHERE is_relevant = 1 AND telegram_sent = 0
        ORDER BY id ASC
    """)
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_recent_articles(
    limit: int = 50,
    gs_filter: Optional[str] = None,
    subject_filter: Optional[str] = None,
    search_query: Optional[str] = None,
    pillar_filter: Optional[str] = None,
    sub_topic_filter: Optional[str] = None,
    date_filter: Optional[str] = None,
    source_filter: Optional[str] = None
) -> List[Dict]:
    conn = get_connection()
    c = conn.cursor()
    query = "SELECT * FROM articles WHERE is_relevant = 1"
    params = []

    if source_filter and source_filter != "All Sources":
        s_clean = source_filter.split("(")[0].strip()
        query += " AND source_name LIKE ?"
        params.append(f"%{s_clean}%")

    if pillar_filter and pillar_filter != "All":
        query += " AND main_pillar LIKE ?"
        params.append(f"%{pillar_filter}%")

    if sub_topic_filter and sub_topic_filter != "All":
        query += " AND (sub_topic LIKE ? OR subject_group LIKE ?)"
        params.extend([f"%{sub_topic_filter}%", f"%{sub_topic_filter}%"])

    if gs_filter and gs_filter != "All":
        query += " AND gs_paper LIKE ?"
        params.append(f"%{gs_filter}%")

    if subject_filter and subject_filter != "All Subjects":
        query += " AND (subject_group LIKE ? OR sub_topic LIKE ?)"
        params.extend([f"%{subject_filter}%", f"%{subject_filter}%"])

    if date_filter and date_filter != "All Dates":
        if "28 Nov" in date_filter:
            query += " AND (published_date LIKE '%28 Nov%' OR published_date LIKE '%November 28%')"
        elif "27 Nov" in date_filter:
            query += " AND (published_date LIKE '%27 Nov%' OR published_date LIKE '%November 27%')"
        else:
            query += " AND published_date LIKE ?"
            params.append(f"%{date_filter}%")

    if search_query:
        query += " AND (title LIKE ? OR short_summary LIKE ? OR ministry LIKE ? OR subject_group LIKE ? OR sub_topic LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term, term, term])

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit * 2)

    c.execute(query, tuple(params))
    rows = c.fetchall()
    conn.close()

    # Filter out any lingering Hindi or mojibake releases
    clean_articles = []
    for r in rows:
        d = dict(r)
        t = d.get("title", "")
        # If title has Devanagari or mojibake symbols, skip
        if any('\u0900' <= char <= '\u0d7f' for char in t) or "à¤" in t:
            continue
        clean_articles.append(d)
        if len(clean_articles) >= limit:
            break

    return clean_articles

def get_dashboard_stats() -> Dict[str, Any]:
    """Returns analytics for visual charts on the dashboard."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT main_pillar, COUNT(*) FROM articles WHERE is_relevant = 1 GROUP BY main_pillar")
    pillar_counts = dict(c.fetchall())

    c.execute("SELECT gs_paper, COUNT(*) FROM articles WHERE is_relevant = 1 GROUP BY gs_paper")
    gs_counts = dict(c.fetchall())

    c.execute("SELECT subject_group, COUNT(*) FROM articles WHERE is_relevant = 1 GROUP BY subject_group")
    subject_counts = dict(c.fetchall())

    c.execute("SELECT ministry, COUNT(*) FROM articles WHERE is_relevant = 1 GROUP BY ministry ORDER BY COUNT(*) DESC LIMIT 8")
    ministry_counts = dict(c.fetchall())

    conn.close()
    return {
        "pillars": pillar_counts,
        "gs_papers": gs_counts,
        "subjects": subject_counts,
        "ministries": ministry_counts,
        "top_ministries": ministry_counts
    }

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", config.DB_PATH)
