# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from django.forms import fields

from .models import Profile


# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    #设置用户名最长字符，和模型定义的字段最长值相对应，这里的User用的django自带的User模型
    username = forms.CharField(max_length=14)
    password = forms.CharField(max_length=14)


#用户注册表单
class UserRegisterForm(forms.ModelForm):
    #复写User的密码，表单中的password fields中的参数都由html中name值相对应的提交元素赋值比如inpute标签
    password = forms.CharField(max_length=14)
    password2 = forms.CharField(max_length=14)

    class Meta:
        model = User
        fields = ('username', 'email')
    
    #对两次输入密码进行一致检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重新输入")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'phone', 'avatar', 'bio')
