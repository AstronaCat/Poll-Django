from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 회원가입 후 로그인 페이지로 리디렉션
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form, 'sub_title': '회원 가입'})
