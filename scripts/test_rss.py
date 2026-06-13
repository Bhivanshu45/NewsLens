from app.services.news.rss_service import RSSService

service = RSSService()

articles = service.fetch_and_parse_feeds()

print(f"Fetched {len(articles)} articles")

print()

print(articles[0])