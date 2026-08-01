import calendar

import feedparser
from dateutil import parser
from datetime import datetime, timezone

from app.core.logger import logger
from app.core.rss_feeds import RSS_FEEDS
from app.services.news.schemas import ParsedArticle


class RSSService:

    def fetch_and_parse_feeds(self):
        articles = []

        for feed_url in RSS_FEEDS:

            try:
                feed = feedparser.parse(feed_url)

            except Exception:
                logger.exception("Failed to parse RSS feed %s", feed_url)
                continue

            for entry in feed.entries:

                title = entry.get("title")
                url = entry.get("link")

                if not title or not url:
                    continue

                published_at = None

                published_value = (
                    entry.get("published")
                    or entry.get("updated")
                    or entry.get("pubDate")
                )

                if published_value:
                    try:
                        published_at = parser.parse(published_value)
                    except Exception:
                        logger.warning(
                            "Failed to parse publication date for feed entry %s",
                            url,
                        )

                if published_at is None:
                    published_parsed = (
                        entry.get("published_parsed")
                        or entry.get("updated_parsed")
                    )

                    if published_parsed:
                        published_at = datetime.fromtimestamp(
                            calendar.timegm(published_parsed),
                            tz=timezone.utc,
                        )

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