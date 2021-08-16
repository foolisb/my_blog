#加入markdown模块
import os
import re

from comment.forms import CommentForm
from comment.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
#Q对象返回表中所有对象
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ArticlePostForm
from .models import ArticlesColumn, ArticlesPost

# Create your views here.


#文章列表页面
def articles_list(request):
    #文章栏目
    columns = ArticlesColumn.objects.all()
    search = request.GET.get('search')
    order = request.GET.get('order')
    tags = []
    #获取所有标签
    articles = ArticlesPost.objects.all()
    for article in articles:
        for tag in article.tags.names():
            tags.append(tag)
    tags = list(set(tags))
    #用户搜索顺序逻辑并根据不同排序返回对象数组
    if search:
        if order == 'total_views':
            articles_list = ArticlesPost.objects.filter(
                Q(title__icontains=search)
                | Q(text__icontains=search)).order_by('-total_views')
        else:
            articles_list = ArticlesPost.objects.filter(
                Q(title__icontains=search) | Q(text__icontains=search))
    else:
        #将search参数重置为空，如果设置为空，search值默认为None，就会匹配None字符串
        search = ''
        if order == 'total_views':
            articles_list = ArticlesPost.objects.all().order_by('-total_views')
        else:
            articles_list = ArticlesPost.objects.all()

    #每页显示的文章数
    paginator = Paginator(articles_list, 6)
    #获取url中的页码
    page = request.GET.get('page')
    #将导航对象对应的页码内容返回给articles
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    #传给模板的对象，字典对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'columns': columns,
        'tags': tags
    }
    return render(request, 'articles/list.html', context)


#文章归档
def article_archives(request):
    #从url中提取参数
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    #文章栏目
    columns = ArticlesColumn.objects.all()
    articles = ArticlesPost.objects.all().order_by('-created')

    #栏目查询
    if column is not None:
        articles = articles.filter(column=column)

    #标签查询
    if tag is not None:
        articles = articles.filter(tags__name__in=[tag])

    context = {'articles': articles, 'columns': columns, 'tag': tag}
    return render(request, 'articles/archives.html', context)


#文章详情页面，这里的id参数由list模板中由article.id传递来的
def article_detail(request, id):
    #文章栏目
    columns = ArticlesColumn.objects.all()
    #取出对应文章
    article = ArticlesPost.objects.get(id=id)
    #取出评论
    comments = Comment.objects.filter(article=id)
    #评论表单
    coment_form = CommentForm()
    #过滤出比当前文章小和大的文章
    pre_article = ArticlesPost.objects.filter(
        id__lt=article.id).order_by('-id')
    next_article = ArticlesPost.objects.filter(
        id__gt=article.id).order_by('id')

    #取出相邻的前一篇文章
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    #取出相邻的后一篇文章
    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None
    #浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    #传递给模板的对象
    context = {
        'article': article,
        'comments': comments,
        'comment_form': coment_form,
        'pre_article': pre_article,
        'next_article': next_article,
        'columns': columns
    }
    #渲染模板返回context对象
    return render(request, 'articles/detail.html', context)


#写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    #判断用户是否提交数据
    if request.method == "POST":
        #将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        #判断数据是否符合模型的要求
        if article_post_form.is_valid():
            #保存数据，但是暂时不提交到数据库，还有字段没有填上数据
            new_article = article_post_form.save(commit=False)
            # 指定数据库中id=1的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            # 效果同下new_article.author = request.user
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticlesColumn.objects.get(
                    id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            # 新增代码，保存tags的多对多关系表单使用了commit=False选项，则必须调用save_m2m()才能正确的保存标签，就像普通的多对多关系一样
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("articles:articles_list")
        #如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有错，请重新填写")
    #如果用户请求获取数据
    else:
        #创建表单实例
        article_post_form = ArticlePostForm()
        #赋值上下文
        columns = ArticlesColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        #返回模板
        return render(request, 'articles/create.html', context)


#安全删除文章
def article_safe_delete(request, id):
    if request.method == "POST":
        #根据id删除文章
        article = ArticlesPost.objects.get(id=id)
        #调用.delete()方法删除
        #富文本中可能有图片需要用re匹配图片源文件来删除
        #注意事项，尽量更新文本时不删原图，更新文本中图片删除旧图比较麻烦
        imagesrc = re.findall('.*img.*src="(.*jpg)".*', article.text)
        if imagesrc:
            for link in imagesrc:
                fname = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))) + link
                if os.path.isfile(fname):
                    os.remove(fname)
        article.delete()
        #删完返回文章列表
        return redirect("articles:articles_list")
    else:
        #不允许通过输入url进行删除，必须点击删除按钮
        return HttpResponse("仅允许post请求")


#更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    '''
    更新文章
    通过post方法提交表单，更新title和text字段
    get方法进入初始表单页面
    id：文章的id
    '''
    #获取要更新的文章的对象
    article = ArticlesPost.objects.get(id=id)
    columns = ArticlesColumn.objects.all()
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改文章")
    #判断用户请求方式
    if request.method == "POST":
        #将数值赋值表单实例化
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        #判断数据是否符合模型要求
        if article_post_form.is_valid():
            #实例化的数据要进行清洗成为合法数据
            if request.POST['column'] != 'none':
                article.column = ArticlesColumn.objects.get(
                    id=request.POST['column'])
            else:
                article.column = None
            data = article_post_form.cleaned_data
            article.title = data['title']
            #删除被更新的图片：更新前
            pre_image = re.findall('.*img.*src="(.*jpg)".*', article.text)
            article.text = data['text']
            #要用*对字符串列表进行解包操作后传入
            article.tags.set(*data['tags'], clear=True)
            if request.FILES.get('avatar'):
                #删除原有头像图片节约存储空间
                if article.avatar:
                    fname = os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(__file__))) + article.avatar.url
                    if os.path.isfile(fname):
                        os.remove(fname)
                article.avatar = request.FILES.get('avatar')
            article.save()
            #删除更新后的图片：更新后
            after_image = re.findall('.*img.*src="(.*jpg)".*', article.text)
            for link in (set(pre_image) - set(after_image)):
                fname = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))) + link
                if os.path.isfile(fname):
                    os.remove(fname)
            return redirect("articles:article_detail", id=id)
        else:
            return HttpResponse("表单有误，请重新填写")
    #如果是get请求
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm(initial={'text': article.text})
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
        }
        # 将响应返回到模板中
        return render(request, 'articles/update.html', context)


#点赞数+1
def IncreaseLikes(request, id):
    if request.method == "POST":
        article = ArticlesPost.objects.get(id=id)
        article.likes += 1
        article.save()
        return HttpResponse('success')
