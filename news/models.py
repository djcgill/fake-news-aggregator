from django.db import models

class Article(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    url = models.TextField()
    score = models.IntegerField(default=50)

    def __str__(self):
        return self.title