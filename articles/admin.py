from django.contrib import admin

from .models import ArticlesColumn, ArticlesPost

# Register your models here.

#注册ArticLesPost到admin中
admin.site.register(ArticlesPost)
#注册文章栏目
admin.site.register(ArticlesColumn)
