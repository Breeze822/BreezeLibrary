# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from django.db.models.signals import post_save

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        # group = request.POST.get['group']
        # print(group)
        if form.is_valid():
            group = form.cleaned_data.get("group")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Username or Password invalid'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})
#
# def create_user_callback(sender, **kwargs):
#     user = kwargs['instance']
#     if kwargs['created']:
#         user.is_staff = True
#         user.save()
#         g = Group.objects.get(name='teacher')
#         g.user_set.add(user)
#
#     else:
#         pass

# #创建User, save()完成前向create_user_callback函数发送信号
# post_save.connect(create_user_callback, sender=User)

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            group = form.cleaned_data.get("group")
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            user.active = True
            user.staff = False
            user.admin = False
            user.save()
            group = Group.objects.get(id=group)
            group.user_set.add(user)
            msg = 'User created - please <a href="../login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
