# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

list_of_choices = (
    (1, 'Student'),
    (2, 'Teacher'),
    (3, 'Admin'),
)

class LoginForm(forms.Form):
    group = forms.ChoiceField(
        choices=list_of_choices,
        )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    class Meta:
        model = User
        fields = ('group', 'username', 'password')

class SignUpForm(UserCreationForm):

    group = forms.ChoiceField(
        choices=list_of_choices,
        )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "ID",
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "FistName",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "LastName",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('group','username', 'first_name', 'last_name','password1', 'password2')
