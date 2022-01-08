from django.db import models


class Scanner(models.Model):
    TYPES = [
        ("tp", "ThirdParty")
    ]
    name = models.CharField(max_length=50, primary_key=True)
    type =  models.CharField(max_length=3, choices=TYPES)
