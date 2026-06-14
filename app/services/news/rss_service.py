# Responsibility:

# Fetch RSS Feed
# Parse Feed
# Return Parsed Articles

# No database code.

from app.core.rss_feeds import RSS_FEEDS
from app.services.news.schemas import ParsedArticle
import feedparser
from dateutil import parser


class RSSService:

    def fetch_and_parse_feeds(self):
        articles = []

        for feed_url in RSS_FEEDS:

            try:
                feed = feedparser.parse(feed_url)

            except Exception as e:
                print(f"Failed to parse {feed_url}: {e}")
                continue

            for entry in feed.entries:

                title = entry.get("title")
                url = entry.get("link")

                if not title or not url:
                    continue

                published_at = None

                if entry.get("published"):
                    try:
                        published_at = parser.parse(
                            entry.get("published")
                        )
                    except Exception:
                        pass

                articles.append(
                    ParsedArticle(
                        title=title,
                        url=url,
                        source=feed.feed.get("title", "Unknown"),
                        published_at=published_at,
                        content=entry.get("summary", ""),
                    )
                )

        return articles