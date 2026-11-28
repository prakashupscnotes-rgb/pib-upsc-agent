import re
import urllib.parse
from typing import List, Dict, Optional
import config

try:
    import requests
    from bs4 import BeautifulSoup
    THIRD_PARTY_SCRAPER_AVAILABLE = True
except ImportError:
    import urllib.request
    import xml.etree.ElementTree as ET
    THIRD_PARTY_SCRAPER_AVAILABLE = False

def ensure_english_pib_url(url: str) -> str:
    """Ensures the PIB URL points to PressReleasePage.aspx and forces lang=1."""
    if not url:
        return url
    # Convert internal iframe page to standard release page
    url = url.replace("PressReleaseIframePage.aspx", "PressReleasePage.aspx")
    # Force lang=1
    if "lang=" in url.lower():
        url = re.sub(r"lang=\d+", "lang=1", url, flags=re.IGNORECASE)
    elif "pib.gov.in" in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}lang=1"
    return url

def clean_date_string(date_raw: str) -> str:
    """Cleans Hindi and metadata prefixes from PIB date strings to produce clean English dates."""
    if not date_raw:
        return ""
    d = date_raw.strip()
    d = re.sub(r"^Release ID:\s*\d+,?\s*", "", d, flags=re.IGNORECASE)
    d = re.sub(r"^Posted On:\s*", "", d, flags=re.IGNORECASE)
    d = re.sub(r"^प्रविष्टि\s*तिथि:\s*", "", d, flags=re.IGNORECASE)
    d = re.sub(r"\s+", " ", d).strip()
    return d

class PIBScraper:
    def __init__(self):
        if THIRD_PARTY_SCRAPER_AVAILABLE:
            self.session = requests.Session()
            self.session.headers.update(config.BROWSER_HEADERS)
        else:
            self.session = None

    def _make_request(self, url: str) -> Optional[str]:
        try:
            if THIRD_PARTY_SCRAPER_AVAILABLE and self.session:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    resp.encoding = "utf-8"
                    return resp.text
            else:
                import urllib.request
                req = urllib.request.Request(url, headers=config.BROWSER_HEADERS)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    return resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"[Scraper] Request failed for {url}: {e}")
            return None

    def extract_prid_from_url(self, url: str) -> Optional[str]:
        match = re.search(r"PRID=(\d+)", url, re.IGNORECASE)
        return match.group(1) if match else None

    def fetch_latest_releases_from_rss(self) -> List[Dict]:
        """Fetches the latest PIB releases from the official English RSS feed."""
        releases = []
        raw_xml = self._make_request(config.PIB_RSS_ENGLISH)
        if not raw_xml:
            print("[Scraper] Empty RSS feed response.")
            return releases

        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(raw_xml)
            channel = root.find("channel")
            if channel is not None:
                for item in channel.findall("item"):
                    title = (item.findtext("title") or "Untitled").strip()
                    link = (item.findtext("link") or "").strip()
                    pub_date = (item.findtext("pubDate") or "").strip()
                    desc = (item.findtext("description") or "").strip()

                    link = ensure_english_pib_url(link)
                    prid = self.extract_prid_from_url(link) or str(abs(hash(title)))

                    releases.append({
                        "pib_id": prid,
                        "title": title,
                        "link": link,
                        "published_date": clean_date_string(pub_date),
                        "initial_desc": desc
                    })
        except Exception as e:
            # Fallback regex parser
            try:
                item_blocks = re.findall(r"<item>(.*?)</item>", raw_xml, flags=re.DOTALL | re.IGNORECASE)
                for it in item_blocks:
                    t_match = re.search(r"<title>(.*?)</title>", it, flags=re.DOTALL | re.IGNORECASE)
                    l_match = re.search(r"<link>(.*?)</link>", it, flags=re.DOTALL | re.IGNORECASE)
                    p_match = re.search(r"<pubDate>(.*?)</pubDate>", it, flags=re.DOTALL | re.IGNORECASE)
                    d_match = re.search(r"<description>(.*?)</description>", it, flags=re.DOTALL | re.IGNORECASE)

                    title = t_match.group(1).strip() if t_match else "Untitled"
                    link = l_match.group(1).strip() if l_match else ""
                    pub_date = p_match.group(1).strip() if p_match else ""
                    desc = d_match.group(1).strip() if d_match else ""

                    link = ensure_english_pib_url(link)
                    prid = self.extract_prid_from_url(link) or str(abs(hash(title)))
                    releases.append({
                        "pib_id": prid,
                        "title": title,
                        "link": link,
                        "published_date": clean_date_string(pub_date),
                        "initial_desc": desc
                    })
            except Exception as ex2:
                print(f"[Scraper] Error parsing RSS XML: {e} / {ex2}")

        return releases

    def fetch_article_full_content(self, url: str) -> Dict[str, str]:
        """
        Scrapes the full text, title, ministry, and date from the PIB article URL.
        If the page is Hindi, automatically detects and follows the official 'English' link.
        """
        result = {
            "title": "",
            "ministry": "Government of India",
            "content": "",
            "date": "",
            "english_url": ensure_english_pib_url(url),
            "pib_id": self.extract_prid_from_url(url) or ""
        }
        
        raw_html = self._make_request(url)
        if not raw_html:
            return result

        try:
            if THIRD_PARTY_SCRAPER_AVAILABLE:
                soup = BeautifulSoup(raw_html, "html.parser")

                # Check if this page has an English version switch link in language bar
                for a in soup.find_all("a"):
                    txt = a.get_text(strip=True).lower()
                    href = a.get("href", "")
                    if txt == "english" and "prid=" in href.lower():
                        eng_url = href if href.startswith("http") else "https://pib.gov.in/" + href.lstrip("/")
                        eng_url = ensure_english_pib_url(eng_url)
                        eng_html = self._make_request(eng_url)
                        if eng_html:
                            # Switch to official English page
                            raw_html = eng_html
                            soup = BeautifulSoup(raw_html, "html.parser")
                            result["english_url"] = eng_url
                            eng_prid = self.extract_prid_from_url(eng_url)
                            if eng_prid:
                                result["pib_id"] = eng_prid
                        break

                # Extract Title
                title_elem = soup.find("h1") or soup.find("h2") or soup.find(class_=re.compile(r"release-title|title", re.I))
                if title_elem and len(title_elem.get_text(strip=True)) > 5:
                    result["title"] = title_elem.get_text(strip=True)

                # Extract Ministry
                ministry_elem = soup.find(class_=re.compile(r"Ministry|minName|release-ministry", re.IGNORECASE))
                if ministry_elem:
                    result["ministry"] = ministry_elem.get_text(strip=True)

                # Extract Date
                date_elem = soup.find(class_=re.compile(r"ReleaseDate|release-date|date", re.IGNORECASE))
                if date_elem:
                    result["date"] = clean_date_string(date_elem.get_text(strip=True))

                # Extract Sub-heading if present
                h3_elem = soup.find("h3")
                subhead = h3_elem.get_text(strip=True) if h3_elem else ""

                # Extract Body Paragraphs
                body_elem = soup.find("div", class_=re.compile(r"innertrans|release-text|content-area", re.IGNORECASE))
                if not body_elem:
                    body_elem = soup.find("article") or soup.find("main")

                if body_elem:
                    for unwanted in body_elem(["script", "style", "nav", "footer", "form"]):
                        unwanted.decompose()
                    paragraphs = [p.get_text(strip=True) for p in body_elem.find_all(["p", "li"])]
                    valid_p = [p for p in paragraphs if len(p) > 25]
                else:
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
                    valid_p = [p for p in paragraphs if len(p) > 30]

                if subhead and len(subhead) > 20:
                    valid_p.insert(0, subhead)

                result["content"] = "\n\n".join(valid_p)

            else:
                # Built-in regex text extractor fallback
                text = re.sub(r"<(script|style|nav|footer)[^>]*>.*?</\1>", "", raw_html, flags=re.DOTALL | re.IGNORECASE)
                paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", text, flags=re.DOTALL | re.IGNORECASE)
                clean_ps = []
                for p in paragraphs:
                    clean = re.sub(r"<[^>]+>", "", p).strip()
                    if len(clean) > 25:
                        clean_ps.append(clean)
                result["content"] = "\n\n".join(clean_ps)

        except Exception as e:
            print(f"[Scraper] Error parsing article HTML {url}: {e}")

        return result

    def get_new_releases(self) -> List[Dict]:
        """Pulls latest releases and fetches full text for each."""
        releases = self.fetch_latest_releases_from_rss()
        detailed_releases = []

        for item in releases:
            url = item["link"]
            details = self.fetch_article_full_content(url)
            content = details["content"] if details["content"] else item.get("initial_desc", "")

            detailed_releases.append({
                "pib_id": details.get("pib_id") or item["pib_id"],
                "title": details.get("title") or item["title"],
                "ministry": details["ministry"],
                "link": details.get("english_url") or url,
                "published_date": details["date"] or item["published_date"],
                "content": content
            })

        return detailed_releases

    def fetch_mann_ki_baat_episodes(self, limit: int = 3) -> List[Dict]:
        """Fetches the latest Mann Ki Baat episodes & transcripts from PM India with YouTube references."""
        episodes = []
        try:
            url = "https://www.pmindia.gov.in/en/mann-ki-baat/"
            html = self._make_request(url)
            if not html:
                return episodes

            soup = BeautifulSoup(html, "html.parser")
            found = 0
            for a in soup.find_all("a"):
                txt = a.get_text(strip=True)
                href = a.get("href", "")
                if ("episode" in txt.lower() or "mann ki baat" in txt.lower()) and "news_updates" in href:
                    full_link = href if href.startswith("http") else "https://www.pmindia.gov.in" + href
                    ep_id = f"MKB_{abs(hash(full_link)) % 1000000}"
                    
                    # Fetch episode full content
                    ep_html = self._make_request(full_link)
                    content = ""
                    yt_link = "https://www.youtube.com/results?search_query=mann+ki+baat+latest+episode"
                    if ep_html:
                        ep_soup = BeautifulSoup(ep_html, "html.parser")
                        paras = [p.get_text(strip=True) for p in ep_soup.find_all("p") if len(p.get_text(strip=True)) > 40]
                        content = "\n\n".join(paras[:15])
                        # Look for embedded youtube link if present
                        for iframe in ep_soup.find_all("iframe"):
                            src = iframe.get("src", "")
                            if "youtube.com" in src or "youtu.be" in src:
                                yt_link = src
                                break

                    episodes.append({
                        "pib_id": ep_id,
                        "title": txt,
                        "ministry": "Prime Minister's Office (PMO)",
                        "link": full_link,
                        "youtube_link": yt_link,
                        "published_date": "Monthly Address",
                        "content": content or txt,
                        "source_name": "Mann Ki Baat (PM Address)"
                    })
                    found += 1
                    if found >= limit:
                        break
        except Exception as e:
            print(f"[Scraper] Error fetching Mann Ki Baat: {e}")

        return episodes

    def fetch_pm_india_updates(self, limit: int = 4) -> List[Dict]:
        """Fetches PM visits, cabinet decisions, and bilateral summits from PM India official portal."""
        updates = []
        try:
            url = "https://www.pmindia.gov.in/en/news-updates/"
            html = self._make_request(url)
            if not html:
                return updates

            soup = BeautifulSoup(html, "html.parser")
            seen_links = set()
            found = 0

            for a in soup.find_all("a"):
                href = a.get("href", "")
                txt = a.get_text(strip=True)
                if "/news_updates/" in href and len(txt) > 25 and href not in seen_links:
                    seen_links.add(href)
                    full_link = href if href.startswith("http") else "https://www.pmindia.gov.in" + href
                    clean_id = f"PM_{abs(hash(full_link)) % 1000000}"

                    # Quick fetch of article body
                    item_html = self._make_request(full_link)
                    content = ""
                    if item_html:
                        item_soup = BeautifulSoup(item_html, "html.parser")
                        paras = [p.get_text(strip=True) for p in item_soup.find_all("p") if len(p.get_text(strip=True)) > 35]
                        content = "\n\n".join(paras[:10])

                    updates.append({
                        "pib_id": clean_id,
                        "title": txt,
                        "ministry": "Prime Minister's Office (PMO)",
                        "link": full_link,
                        "published_date": "Official Release",
                        "content": content or txt,
                        "source_name": "PM India (Visits & Cabinet)"
                    })
                    found += 1
                    if found >= limit:
                        break
        except Exception as e:
            print(f"[Scraper] Error fetching PM India news updates: {e}")

        return updates

    def fetch_karnataka_news(self, limit: int = 4) -> List[Dict]:
        """Fetches Karnataka state specific government policies, acts, and developments for KEA exams."""
        karnataka_items = []
        feed_url = "https://www.thehindu.com/news/national/karnataka/feeder/default.rss"
        try:
            raw_xml = self._make_request(feed_url)
            if raw_xml:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(raw_xml)
                channel = root.find("channel")
                if channel is not None:
                    count = 0
                    for item in channel.findall("item"):
                        title = (item.findtext("title") or "Untitled").strip()
                        link = (item.findtext("link") or "").strip()
                        pub_date = (item.findtext("pubDate") or "").strip()
                        desc = (item.findtext("description") or "").strip()
                        clean_desc = re.sub(r"<[^>]+>", "", desc).strip()
                        item_id = f"KAR_{abs(hash(link)) % 1000000}"

                        karnataka_items.append({
                            "pib_id": item_id,
                            "title": title,
                            "ministry": "Government of Karnataka",
                            "link": link,
                            "published_date": clean_date_string(pub_date),
                            "content": clean_desc or title,
                            "source_name": "Karnataka State News"
                        })
                        count += 1
                        if count >= limit:
                            break
        except Exception as e:
            print(f"[Scraper] Error fetching Karnataka news: {e}")

        return karnataka_items

    def fetch_reputed_newspapers(self, limit: int = 8) -> List[Dict]:
        """Fetches national and policy news from The Hindu and The Indian Express RSS feeds."""
        newspaper_items = []
        feeds = [
            ("The Hindu", "https://www.thehindu.com/news/national/feeder/default.rss"),
            ("Indian Express", "https://indianexpress.com/section/india/feed/"),
            ("The Hindu Editorial", "https://www.thehindu.com/opinion/editorial/feeder/default.rss")
        ]

        per_feed = max(2, limit // len(feeds))
        for source_label, feed_url in feeds:
            try:
                raw_xml = self._make_request(feed_url)
                if not raw_xml:
                    continue

                import xml.etree.ElementTree as ET
                root = ET.fromstring(raw_xml)
                channel = root.find("channel")
                if channel is None:
                    continue

                count = 0
                for item in channel.findall("item"):
                    title = (item.findtext("title") or "Untitled").strip()
                    link = (item.findtext("link") or "").strip()
                    pub_date = (item.findtext("pubDate") or "").strip()
                    desc = (item.findtext("description") or "").strip()

                    # Clean html tags from description
                    clean_desc = re.sub(r"<[^>]+>", "", desc).strip()
                    item_id = f"NEWS_{abs(hash(link)) % 1000000}"

                    newspaper_items.append({
                        "pib_id": item_id,
                        "title": title,
                        "ministry": f"National Press ({source_label})",
                        "link": link,
                        "published_date": clean_date_string(pub_date),
                        "content": clean_desc or title,
                        "source_name": source_label
                    })
                    count += 1
                    if count >= per_feed:
                        break

            except Exception as e:
                print(f"[Scraper] Error fetching {source_label}: {e}")

        return newspaper_items

if __name__ == "__main__":
    scraper = PIBScraper()
    print("[Scraper] Checking for releases...")
    items = scraper.fetch_latest_releases_from_rss()
    print(f"[Scraper] Retrieved {len(items)} releases from RSS.")
    if items:
        sample = items[0]
        print(f"Sample: {sample['title']} (PRID: {sample['pib_id']}) -> {sample['link']}")
