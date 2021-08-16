#引入表单类,表单可以让用户在前端发表提交文章、评论等
from django import forms

#引入文章模型
from .models import ArticlesPost


#写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #指明数据来源
        model = ArticlesPost
        #定义表单包含的字段
        fields = ('title', 'text', 'tags', 'avatar')
