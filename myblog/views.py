from django.shortcuts import render, get_object_or_404, reverse
from .models import Article, Category
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib import messages
from accounts.mixins import SuperUserAccessMixin
from django.db.models import Count, Q
from datetime import datetime, timedelta


def all_articles(request):
    last_month = datetime.today() - timedelta(days=30)
    all_articles = Article.objects.published()
    paginator = Paginator(all_articles, 8)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    categories = Category.objects.filter(status=True)
    popular_articles = Article.objects.published().annotate(count=Count('hits', filter=Q(articlehit__created__gt=last_month))).order_by('-count')
    context = {'categories': categories,
               'articles': articles,
               'popular_articles': popular_articles}
    return render(request, 'myblog/all_articles.html', context)


def article_detail(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    ip_address = request.user.ip_address
    if ip_address not in article.hits.all():
        article.hits.add(ip_address)
    context = {'article': article}
    return render(request, 'myblog/article_detail.html', context)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug, status=True)
    articles_list = category.articles.published()
    paginator = Paginator(articles_list, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    all_categories = Category.objects.filter(status=True)
    return render(request, 'myblog/category.html', {'category': category, 'all_categories': all_categories, 'articles': articles})


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'body', 'category', 'status', 'writer')
    template_name = 'myblog/article_create_update.html'
    success_url = reverse_lazy('myblog:all_articles')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.slug = slugify(form.cleaned_data['title'])
        article.save()
        messages.success(self.request, 'مقاله شما با موفقیت ارسال شد.', 'success')
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'body', 'category', 'status', 'writer')
    template_name = 'myblog/article_create_update.html'

    def get_success_url(self):
        messages.success(self.request, 'مقاله شما با موفقیت ویرایش شد.', 'success')
        return reverse('myblog:article_detail', kwargs={'id': self.object.id, 'slug': self.object.slug})


class ArticleDelete(LoginRequiredMixin, SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('myblog:all_articles')


class SearchList(ListView):
    template_name = 'myblog/search_list.html'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(body__icontains=search) | Q(title__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context









