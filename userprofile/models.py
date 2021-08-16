from django.contrib.auth.models import User, UserManager
from django.db import models
#引入内置信号
from django.db.models.signals import post_save
#引入信号接收器的装饰器
from django.dispatch import receiver
# 引入imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# Create your models here.
#用户扩展信息
class Profile(models.Model):
    #与User模型构成一对一的关系，User模型是django自带的
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #username
    username = models.CharField(max_length=20, blank=True)
    #电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    #头像
    avatar = ProcessedImageField(
        upload_to='user/avatar/%Y%m%d',
        processors=[ResizeToFit(100, 100)],
        format='JPEG',
        options={'quality': 100},
        blank=True
    )
    #个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self) -> str:
        return 'user {}'.format(self.user.username)
        
# 信号接收函数，每当新建 User 实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
