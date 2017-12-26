# -*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):

    usr = forms.CharField(label='Nombre Usuario')
    pwd = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

