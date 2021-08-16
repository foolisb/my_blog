#导入内建的user模型
import os

#富文本
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
#引入内置信号
from django.db.models.signals import post_delete
#引入信号接收器的装饰器
from django.dispatch import receiver
from django.urls import reverse
#用timezone处理时间相关事务
from django.utils import timezone
# 引入imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
#标签字段
from taggit.managers import TaggableManager


# Create your models here.
#博客栏目
class ArticlesColumn(models.Model):
    #栏目标题
    title = models.CharField(max_length=100, blank=True)
    #创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title


# 博客文章模型
class ArticlesPost(models.Model):
    #文章栏目,这里外键关联的是id值所以该外键字段是int值
    column = models.ForeignKey(ArticlesColumn,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name='article')
    #文章作者,外键放在多的一方
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #文章标题
    title = models.CharField(max_length=100)
    #文章标签,blank=True可以不写
    tags = TaggableManager(blank=True)
    #文章标题图
    avatar = ProcessedImageField(
        upload_to='article/avatar/%Y%m%d',
        processors=[ResizeToFit(400, 400)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )
    #文章正文
    #text = models.TextField()
    text = RichTextUploadingField()
    #文章创建日期
    created = models.DateTimeField(default=timezone.now)
    #文章修改日期，参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    #文章浏览量
    total_views = models.PositiveIntegerField(default=0)
    #新增点赞数统计
    likes = models.PositiveIntegerField(default=0)
    #内部类class Meta 用于给model定于元数据（描述数据的数据）
    class Meta:
        #ordering指定模型返回的数据的排列顺序
        ordering = ('-updated', )

    #获取文章地址
    def get_absolute_url(self):
        return reverse('articles:article_detail', args=[self.id])

    def __str__(self):
        return self.title

#物理删除图片内容
@receiver(post_delete, sender=ArticlesPost)
def delete_upload_files(sender, instance, **kwargs):
        files = getattr(instance, 'avatar', '')
        if not files:
            return 
        #返回父路径os.dirname可以嵌套使用 返回当前文件也就是models.py绝对路径os.path.abspath(__file__)
        fname = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + files.url
        if os.path.isfile(fname):
            os.remove(fname)
