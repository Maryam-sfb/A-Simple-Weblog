from django.urls import path
from . import views


app_name = 'myblog'
urlpatterns = [
    path('', views.all_articles, name='all_articles'),
    path('<int:id>/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('article/create/', views.ArticleCreate.as_view(), name='article_create'),
    path('article/update/<int:pk>/', views.ArticleUpdate.as_view(), name='article_update'),
    path('article/delete/<int:pk>/', views.ArticleDelete.as_view(), name='article_delete'),
    path('search/', views.SearchList.as_view(), name='search')
]