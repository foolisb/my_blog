
import os

from django.contrib.auth import authenticate, login, logout
#引入验证登陆的装饰器
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeBaseInput
from django.http import HttpResponse, request
from django.shortcuts import redirect, render

from .forms import ProfileForm, UserLoginForm, UserRegisterForm
from .models import Profile

# Create your views here.


#用户登入
def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            #清洗出合法的数据
            data = user_login_form.cleaned_data
            #检验账号、密码是否正确匹配数据库中的用户
            #匹配则返回user对象
            user = authenticate(username=data['username'],
                                password=data['password'])
            if user:
                #将数据保存在session中，即实现了登陆的动作
                login(request, user)
                return HttpResponse('200 OK')
            else:
                return HttpResponse("error1")
        else:
            return HttpResponse("error2")
    else:
        return HttpResponse("请使POST请求数据")


#用户登出
def user_logout(request):
    logout(request)
    return redirect("articles:articles_list")


#用户注册
def user_register(request):
    if request.method == "POST":
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            #设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            #保存好数据后立即登陆返回博客列表页面
            login(request, new_user)
            return HttpResponse("200 OK")
        else:
            return HttpResponse("注册表单输入有误，请重新输入")
    else:
        return HttpResponse("请使用POST请求数据")


#用户删除
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        #验证登陆用户、待删除用户是否相同
        if request.user == user:
            #退出登陆，删除数据并返回博客列表
            logout(request)
            if user.profile.avatar:
                fname = os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__))) + user.profile.avatar.url
                if os.path.isfile(fname):
                    os.remove(fname)
            user.delete()
            return redirect("articles:articles_list")
        else:
            return HttpResponse("你没有删除操作的权限")
    else:
        return HttpResponse("仅接受post请求")


#编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == "POST":
        #验证修改数据是否是用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息")
        #上传的文件保存在request.FILES中，通过参数给表单类
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            #清洗数据获得合法数据
            profile_cd = profile_form.cleaned_data
            profile.username = profile_cd['username']
            user.username = profile.username
            user.save(update_fields=['username'])
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                if profile.avatar:
                    fname = os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(__file__))) + profile.avatar.url
                    if os.path.isfile(fname):
                        os.remove(fname)
                profile.avatar = profile_cd['avatar']
            profile.save()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误，请重新输入")
    #其实所有get方法中基本不需要传入表单对象，因为模板已经写好表单，也没有有用到表单对象
    elif request.method == "GET":
        profile_form = ProfileForm()
        context = {
            'profile_form': profile_form,
            'profile': profile,
            'user': user
        }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
