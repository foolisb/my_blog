from django.urls import path

from . import views

#正在部署的app名称
app_name = 'comment'

urlpatterns = [
    #发表评论
    path('post_comment/<int:article_id>/', views.post_comment, name='post_comment'),
    #处理二级回复
    path('post_comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),
]
