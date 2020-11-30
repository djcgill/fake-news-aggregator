from django.db import models

from django.utils import timezone

from urllib.parse import urlparse
from feedparser import parse

class NewsFeed(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            data = parse(url)

            if 'title' in kwargs:
                feed_title = kwargs['title']
            elif data.feed.title:
                feed_title = data.feed.title
            else:
                feed_title = get_feed_title_from_url(url)

            self.name = feed_title

            super(NewsFeed, self).save(*args, **kwargs)

            self.get_articles(self.url)


    def get_articles(self, url):
        feed = parse(url)

        for entry in feed.entries: # Limit the amount of new article e.g top 10 newest
            if not Article.objects.get(url=entry.link): # Or updated time is newer than we have
                article = Article()
                article.title = entry.title
                article.url = entry.link
                article.publictaion_date = entry.published.parsed
                article.last_updated_date = entry.updated_parsed
                article.source = self
                #TODO: add article score when HAProxy is implemented
                #TODO: add images

                article.save()

    @staticmethod
    def get_feed_title_from_url(url):
        return urlparse(url).netloc

class Article(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    url = models.URLField()
    score = models.IntegerField(default=50)
    publication_date = models.DateTimeField()
    last_updated_date = models.DateTimeField()
    source = models.ForeignKey(NewsFeed, on_delete=models.PROTECT)

    def __str__(self):
        return self.title