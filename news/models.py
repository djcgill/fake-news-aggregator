import os

from django.db import models

from django.utils import timezone
from django.template.defaultfilters import slugify

from datetime import datetime
from time import mktime
from urllib.parse import urlparse
from feedparser import parse


class NewsFeed(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    #default_image = models.ImageField(upload_to='imagepath', blank=True, null=True) # TODO

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            data = parse(self.url)

            if 'title' in kwargs:
                feed_title = kwargs['title']
            elif data.feed.title:
                feed_title = data.feed.title
            else:
                feed_title = get_feed_title_from_url(url)

            self.name = feed_title

            super(NewsFeed, self).save(*args, **kwargs)

            self.get_articles()


    def get_articles(self, *args, **kwargs):
        feed = parse(self.url)

        for entry in feed.entries: # Limit the amount of new article e.g top 10 newest
            if not Article.objects.filter(url=entry.link).exists(): # Or updated time is newer than we have
                article = Article()
                article.title = entry.title
                article.url = entry.link
                article.description = entry.description
                article.publictaion_date = datetime.fromtimestamp(mktime(entry.published_parsed))
                article.last_updated_date = datetime.fromtimestamp(mktime(entry.updated_parsed))

                try:
                    article.category = entry.categories
                except AttributeError:
                    #article.category = None
                    pass

                article.source = self # This is bad use something else
                #TODO: add article score when HAProxy is implemented
                #TODO: add images


                article.save()

    def get_image_path(self, filename):
        return os.path.join('photos', str(self.name), filename)

    @staticmethod
    def get_feed_title_from_url(url):
        return urlparse(url).netloc


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    url = models.URLField()
    score = models.IntegerField(default=50)
    publication_date = models.DateTimeField(default=datetime.now)
    last_updated_date = models.DateTimeField(default=datetime.now)
    source = models.ForeignKey(NewsFeed, on_delete=models.PROTECT)
    category = models.CharField(max_length=200, default='undefined')
    description = models.TextField()

    def __str__(self):
        return self.title
