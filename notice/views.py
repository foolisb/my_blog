from articles.models import ArticlesColumn, ArticlesPost
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

@login_required(login_url='/userprofile/login/')
def comment_notice_list(request):
    #未读通知
    notices = request.user.notifications.unread()
    readnotices = request.user.notifications.read()
    context = {
        'notices': notices,
        'readnotices': readnotices
    }

    return render(request, 'notice/notice_list.html', context)


#更新通知状态
def comment_notice_update(request):
    #获取未读消息
    notice_id = request.GET.get('notice_id')
    #更新单条通知
    if notice_id:
        article = ArticlesPost.objects.get(id=request.GET.get('article_id'))
        #消息设置为已读
        request.user.notifications.get(id=notice_id).mark_as_read()
        #跳转评论对应文章
        return redirect(article)
    #更新全部通知
    else:
        if request.user.notifications.count():
            request.user.notifications.mark_all_as_read()
        return redirect('notice:list')
