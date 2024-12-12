from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='유효한 이메일 주소를 입력하세요.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
