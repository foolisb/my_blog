__Auhtor = 'foolisb'
'''
自定义时间过滤器
让时间的显示更友好
'''

import math

from django import template
from django.utils import timezone

#需要模板库
register = template.Library()

#获取相对时间
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return "just now"

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        return str(math.floor(diff.seconds/60)) + " min ago"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        if math.floor(diff.seconds/3600) < 2:
            return "1 hour ago"
        return str(math.floor(diff.seconds/3600)) + " hours ago"

    if diff.days >= 1 and diff.days < 30:
        if diff.days < 2:
            return "1 day ago"
        return str(diff.days) + " days ago"

    if diff.days >= 30 and diff.days < 365:
        if diff.days < 31:
            return "1 month ago"
        return str(math.floor(diff.days/30)) + " months ago"

    if diff.days >= 365:
        if diff.days < 366:
            return "1 year ago"
        return str(math.floor(diff.days/365)) + " years ago"
