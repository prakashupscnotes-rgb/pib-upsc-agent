import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
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
    # Add subject_group column if upgrading existing database
    try:
        c.execute("ALTER TABLE articles ADD COLUMN subject_group TEXT DEFAULT 'General'")
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
    published_date: str = ""
) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO articles (
            pib_id, title, ministry, link, raw_content,
            is_relevant, gs_paper, subject_group, short_summary,
            prelims_facts, mains_pointer, published_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(pib_id) DO UPDATE SET
            is_relevant = excluded.is_relevant,
            gs_paper = excluded.gs_paper,
            subject_group = excluded.subject_group,
            short_summary = excluded.short_summary,
            prelims_facts = excluded.prelims_facts,
            mains_pointer = excluded.mains_pointer
    """, (
        pib_id, title, ministry, link, raw_content,
        1 if is_relevant else 0, gs_paper, subject_group, short_summary,
        prelims_facts, mains_pointer, published_date
    ))
    conn.commit()
    inserted_id = c.lastrowid
    conn.close()
    return inserted_id

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
    search_query: Optional[str] = None
) -> List[Dict]:
    conn = get_connection()
    c = conn.cursor()
    query = "SELECT * FROM articles WHERE is_relevant = 1"
    params = []

    if gs_filter and gs_filter != "All":
        query += " AND gs_paper LIKE ?"
        params.append(f"%{gs_filter}%")

    if subject_filter and subject_filter != "All Subjects":
        query += " AND subject_group LIKE ?"
        params.append(f"%{subject_filter}%")

    if search_query:
        query += " AND (title LIKE ? OR short_summary LIKE ? OR ministry LIKE ? OR subject_group LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term, term])

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

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", config.DB_PATH)
