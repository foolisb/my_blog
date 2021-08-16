#引入path

from django.urls import path

from . import views

#正在部署的app名称
app_name = 'articles'

urlpatterns = [
    path('articles_list/', views.articles_list, name='articles_list'),
    path('article_archives/', views.article_archives, name='article_archives'),
    path('article_detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article_create/', views.article_create, name='article_create'),
    path('article_safe_delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path('article_update/<int:id>/', views.article_update, name='article_update'),
    path('increase_likes/<int:id>/', views.IncreaseLikes, name='increase_likes'),
]
