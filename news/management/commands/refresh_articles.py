from django.core.management.base import BaseCommand

import logging

from feedparser import parse

from news.models import Article, NewsFeed

class command(BaseCommand):
    help = "Refreshes articles from all available feeds"
    logger = logging.getLogger(__name__)


    def handle(self, *args, **options):
        if 'feed_name' in options:
            raise NotImplementedError("Cannot specify feed name yet")
        else:
            feeds = NewsFeed.objects.values_list('url', flat=True)

            for feed_url in feeds:
                self.logger.debug("Getting feed from: %s", feed_url)
                feed = parse(feed_url)
                feed.get_articles(feed_url)
