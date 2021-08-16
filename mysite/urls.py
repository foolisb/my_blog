"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications.urls
from articles.views import articles_list
from django import urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

'''
    include语法相当于多级路由，它把接收到的url地
    址去除与此项匹配的部分，将剩下的字符串传递给下一级路由urlconf进行判断
    不要在代码内部出现多行注释，放在import内容之后
'''
urlpatterns = [
    # home
    path('', articles_list, name='home'),
    #评论
    path('comment/', include('comment.urls', namespace='comment')),
    path('articles/', include('articles.urls', namespace='articles')),
    #用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('password_reset/', include('password_reset.urls')),
    #富文本
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #消息通知
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('notice/', include('notice.urls', namespace='notice')),
    #第三方登陆,其实可以不用这个库带的模板只要把第三方登陆功能添加到原来的登陆模板就行
    path('accounts/', include('allauth.urls')),
    #可以修改url避免轻易泄露后台url，把admin/改成control
    path('control/', admin.site.urls),
]


#上传media文件
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
