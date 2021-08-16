from articles.models import ArticlesPost
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
#消息通知
from notifications.signals import notify

from .forms import CommentForm
from .models import Comment

# Create your views here.


#文章评论
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlesPost, id=article_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #新生成的记录保存但是不提交，要把作者文章字段写上
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            #二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                #若回复层级超过二级，则转为二级
                new_comment.parent_id = parent_comment.get_root().id
                #被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                #给其他用户发送通知
                if  parent_comment.user.username != request.user.username:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
                return HttpResponse('200 OK')

            new_comment.save()
            #给管理发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment,
                )

            # 新增代码，添加锚点
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        #渲染二级回复表单页面
        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse("仅接受GET/POST请求")
