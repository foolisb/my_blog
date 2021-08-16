from articles.models import ArticlesPost
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import related
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

#博文评论
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlesPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    #body = models.TextField()
    body = RichTextField(config_name='comment')
    #新增加树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    #新增二级评论，回复
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyer'
    )
    #auto_now_add只在创建时添加时间
    created = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created']
    
    def __str__(self) -> str:
        return self.body[:20]

'''
原先类型结构
class Comment(models.Model):
    article = models.ForeignKey(
        ArticlesPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    #body = models.TextField()
    body = RichTextField(config_name='comment')
    #auto_now_add只在创建时添加时间
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self) -> str:
        return self.body[:20]
'''
