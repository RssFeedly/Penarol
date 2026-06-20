import requests
from bs4 import BeautifulSoup
from datetime import datetime
import html

URL = "https://www.xn--pearol-xwa.org/categoria/Noticias-2"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
}

def get_page():
    response = requests.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text

def parse_news(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.select("h2 a")

    items = []

    for link in links[:10]:
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        title = html.escape(title)

        items.append(f"""
        <item>
            <title>{title}</title>
            <link>{href}</link>
            <guid>{href}</guid>
            <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        </item>
        """)

    return items

def save_rss(items):
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Mi RSS automático</title>
    <link>{URL}</link>
    <description>Noticias automáticas</description>
    {''.join(items)}
</channel>
</rss>
"""

    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss)

def main():
    html_content = get_page()
    items = parse_news(html_content)
    save_rss(items)
    print(f"RSS generado con {len(items)} items")

if __name__ == "__main__":
    main()
