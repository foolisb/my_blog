__Auhtor = 'foolisb'
'''
自定义模板标签、过滤器等
在模板中通过{% load pagetag %}来引用
app_name：对应app名称
'''

from django import template

#需要模板库
register = template.Library()

from django.utils.html import format_html

'''
功能：博客分页固定显示的页数
curr_page：当前页码
loop_page：循环页码
'''
#注册标签
@register.simple_tag
def circle_page(curr_page, order, loop_page, search):
    if curr_page <= 4:
        if loop_page <= 4:
            if loop_page == curr_page:
                page_ele = '<li class="page-item active"><a class="page-link" href="?page=%s&order=%s&search=%s">%s</a></li>'%(loop_page, order, search, loop_page)
            else:
                page_ele = '<li class="page-item"><a class="page-link" href="?page=%s&order=%s&search=%s">%s</a></li>'%(loop_page, order, search, loop_page)
            return format_html(page_ele)
        else:
            return ''
    elif curr_page > 4:
        if curr_page - loop_page <= 3 and curr_page - loop_page >= 0:
            if loop_page == curr_page:
                page_ele = '<li class="page-item active"><a class="page-link" href="?page=%s&order=%s&search=%s">%s</a></li>'%(loop_page, order, search, loop_page)
            else:
                page_ele = '<li class="page-item"><a class="page-link" href="?page=%s&order=%s&search=%s">%s</a></li>'%(loop_page, order, search, loop_page)
            return format_html(page_ele)
        else:
            return ''

