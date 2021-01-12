from django.shortcuts import render, get_object_or_404
from .models import Article


def all_articles(request):
    all_articles = Article.published.all()
    context = {'all_articles': all_articles}
    return render(request, 'myblog/all_articles.html', context)


def article_detail(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    context = {'article': article}
    return render(request, 'myblog/article.html', context)