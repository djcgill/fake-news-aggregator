from django.shortcuts import render
from django.http import HttpResponse

from news.models import Article

def index(request):
    # TODO: Latest by individual sources
    articles = Article.objects.order_by('last_updated_date')[:10]
    context = {
        "article_list": articles,
    }
    return render(request, 'index.html', context)