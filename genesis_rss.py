import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.energy.gov/undersecretaryforscience/genesis-mission/listings/genesis-mission-news"

def fetch_news():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    items = []

    for a in soup.select("a"):
        title = a.get_text(strip=True)
        href = a.get("href")

        if not title or len(title) < 15:
            continue

        if not href:
            continue

        if href.startswith("/"):
            link = "https://www.energy.gov" + href
        else:
            link = href

        if "energy.gov" not in link:
            continue

        items.append({
            "title": title,
            "link": link,
            "date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        })

    return items[:20]


def generate_rss(items):
    rss_items = ""
    for item in items:
        rss_items += f"""
        <item>
            <title>{item['title']}</title>
            <link>{item['link']}</link>
            <pubDate>{item['date']}</pubDate>
        </item>
        """

    return f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>Genesis Mission News</title>
        <link>{URL}</link>
        <description>DOE Genesis Mission News</description>
        {rss_items}
    </channel>
    </rss>
    """


if __name__ == "__main__":
    news = fetch_news()
    rss = generate_rss(news)

    with open("docs/rss.xml", "w", encoding="utf-8") as f:
        f.write(rss)
