from django.shortcuts import render
from django.http import HttpResponse

from news.models import Article

def index(request):
    articles = Article.objects.all()[::-1]
    context = {
        "article_list": articles,
    }
    return render(request, 'index.html', context)