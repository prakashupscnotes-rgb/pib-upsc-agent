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

def is_english_text(text: str) -> bool:
    """Checks that the text is primarily in English and has no Devanagari/Indic script."""
    if not text:
        return False
    # If it contains Devanagari characters, it is Hindi/regional
    if any('\u0900' <= char <= '\u0d7f' for char in text):
        return False
    # Must have reasonable ASCII alphabetic content
    ascii_letters = sum(1 for c in text if c.isascii() and c.isalpha())
    return ascii_letters >= 4

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
                req = urllib.request.Request(url, headers=config.BROWSER_HEADERS)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    raw_bytes = resp.read()
                    return raw_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            print(f"[Scraper] Network request error for {url}: {e}")
        return None

    def extract_prid_from_url(self, url: str) -> Optional[str]:
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        prid = params.get("PRID") or params.get("prid")
        if prid:
            return prid[0]
        match = re.search(r"PRID=(\d+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def fetch_latest_releases_from_rss(self) -> List[Dict]:
        """
        Fetches latest press releases from official PIB RSS feed.
        """
        releases = []
        raw_xml = self._make_request(config.PIB_RSS_ENGLISH)
        if not raw_xml:
            return releases

        try:
            # Parse RSS XML using standard library xml.etree.ElementTree
            import xml.etree.ElementTree as ET
            root = ET.fromstring(raw_xml.encode("utf-8"))
            for item in root.findall(".//item"):
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                pub_date = item.findtext("pubDate", "").strip()
                desc = item.findtext("description", "").strip()

                prid = self.extract_prid_from_url(link) or str(abs(hash(title)))
                releases.append({
                    "pib_id": prid,
                    "title": title,
                    "link": link,
                    "published_date": pub_date,
                    "initial_desc": desc
                })
        except Exception as e:
            # Fallback regex parsing if XML has unescaped characters
            try:
                items_raw = re.findall(r"<item>(.*?)</item>", raw_xml, flags=re.DOTALL | re.IGNORECASE)
                for it in items_raw:
                    t_match = re.search(r"<title>(.*?)</title>", it, flags=re.DOTALL | re.IGNORECASE)
                    l_match = re.search(r"<link>(.*?)</link>", it, flags=re.DOTALL | re.IGNORECASE)
                    p_match = re.search(r"<pubDate>(.*?)</pubDate>", it, flags=re.DOTALL | re.IGNORECASE)
                    d_match = re.search(r"<description>(.*?)</description>", it, flags=re.DOTALL | re.IGNORECASE)

                    title = t_match.group(1).strip() if t_match else "Untitled"
                    link = l_match.group(1).strip() if l_match else ""
                    pub_date = p_match.group(1).strip() if p_match else ""
                    desc = d_match.group(1).strip() if d_match else ""

                    prid = self.extract_prid_from_url(link) or str(abs(hash(title)))
                    releases.append({
                        "pib_id": prid,
                        "title": title,
                        "link": link,
                        "published_date": pub_date,
                        "initial_desc": desc
                    })
            except Exception as ex2:
                print(f"[Scraper] Error parsing RSS XML: {e} / {ex2}")

        return releases

    def fetch_article_full_content(self, url: str) -> Dict[str, str]:
        """
        Scrapes the full text and ministry details from the specific PIB article URL.
        """
        result = {
            "ministry": "Government of India",
            "content": "",
            "date": ""
        }
        raw_html = self._make_request(url)
        if not raw_html:
            return result

        try:
            if THIRD_PARTY_SCRAPER_AVAILABLE:
                soup = BeautifulSoup(raw_html, "html.parser")
                ministry_elem = soup.find(class_=re.compile(r"Ministry|minName|release-ministry", re.IGNORECASE))
                if ministry_elem:
                    result["ministry"] = ministry_elem.get_text(strip=True)

                date_elem = soup.find(class_=re.compile(r"ReleaseDate|release-date|date", re.IGNORECASE))
                if date_elem:
                    result["date"] = date_elem.get_text(strip=True)

                body_elem = soup.find("div", class_=re.compile(r"innertrans|release-text|content-area", re.IGNORECASE))
                if not body_elem:
                    body_elem = soup.find("article") or soup.find("main")

                if body_elem:
                    for unwanted in body_elem(["script", "style", "nav", "footer", "form"]):
                        unwanted.decompose()
                    paragraphs = [p.get_text(strip=True) for p in body_elem.find_all(["p", "li"])]
                    result["content"] = "\n".join([p for p in paragraphs if len(p) > 20])
                else:
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
                    result["content"] = "\n".join([p for p in paragraphs if len(p) > 30])
            else:
                # Built-in regex text extractor fallback
                text = re.sub(r"<(script|style|nav|footer)[^>]*>.*?</\1>", "", raw_html, flags=re.DOTALL | re.IGNORECASE)
                paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", text, flags=re.DOTALL | re.IGNORECASE)
                clean_ps = []
                for p in paragraphs:
                    clean = re.sub(r"<[^>]+>", "", p).strip()
                    if len(clean) > 25:
                        clean_ps.append(clean)
                result["content"] = "\n".join(clean_ps)

        except Exception as e:
            print(f"[Scraper] Error parsing article HTML {url}: {e}")

        return result

    def get_new_releases(self) -> List[Dict]:
        """
        Pulls latest releases and fetches full text for each.
        """
        releases = self.fetch_latest_releases_from_rss()
        detailed_releases = []

        for item in releases:
            url = item["link"]
            details = self.fetch_article_full_content(url)
            content = details["content"] if details["content"] else item.get("initial_desc", "")

            detailed_releases.append({
                "pib_id": item["pib_id"],
                "title": item["title"],
                "ministry": details["ministry"],
                "link": url,
                "published_date": details["date"] or item["published_date"],
                "content": content
            })

        return detailed_releases

if __name__ == "__main__":
    scraper = PIBScraper()
    print("[Scraper] Checking for releases...")
    items = scraper.fetch_latest_releases_from_rss()
    print(f"[Scraper] Retrieved {len(items)} releases from RSS.")
    if items:
        sample = items[0]
        print(f"Sample: {sample['title']} (PRID: {sample['pib_id']}) -> {sample['link']}")
