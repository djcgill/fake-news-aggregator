from django.core.management.base import BaseCommand

import logging

from feedparser import parse

from news.models import Article, NewsFeed

class command(BaseCommand):
    help = "Add new RSS feed"
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)
        parser.add_argument(
            '--name',
            action='store_true',
            help='Name of feed to be saved as',
        )

    def handle(self, *args, **options):
        feed_name = options['name'] if 'name' in options else None
        feed = NewsFeed(url=options['url'], title=feed_name)
        feed.save()
        