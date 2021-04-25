from django.core.management.base import BaseCommand

import logging

from feedparser import parse

from news.models import Article, NewsFeed

class Command(BaseCommand):
    help = "Add new RSS feed"
    logger = logging.getLogger(__name__)

    # TODO: Allow a RSS feeds to be added via a file
    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)
        parser.add_argument(
            '--name',
            action='store_true',
            help='Name of feed to be saved as',
        )

    def handle(self, *args, **options):
        if 'url' in options:
            for url in options['url']:
                feed = NewsFeed(url=url)
                feed.save()
        