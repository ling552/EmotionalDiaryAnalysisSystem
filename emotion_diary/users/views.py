from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect, render

from diary.models import Diary


def login_view(request):
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

        messages.error(request, '用户名或密码错误，请重试。')

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        email = (request.POST.get('email') or '').strip()
        password1 = (request.POST.get('password1') or '').strip()
        password2 = (request.POST.get('password2') or '').strip()

        if not username:
            messages.error(request, '请输入用户名。')
        elif password1 != password2:
            messages.error(request, '两次输入的密码不一致。')
        elif len(password1) < 6:
            messages.error(request, '密码长度至少 6 位。')
        elif User.objects.filter(username=username).exists():
            messages.error(request, '该用户名已被注册。')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('index')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        request.user.email = email
        request.user.save(update_fields=['email'])
        messages.success(request, '个人信息已更新。')
        return redirect('profile')
    return render(request, 'profile.html')


@login_required
def password_change_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password') or ''
        new_password1 = request.POST.get('new_password1') or ''
        new_password2 = request.POST.get('new_password2') or ''

        if not request.user.check_password(old_password):
            messages.error(request, '原密码不正确。')
            return render(request, 'password_change.html')

        if new_password1 != new_password2:
            messages.error(request, '两次输入的新密码不一致。')
            return render(request, 'password_change.html')

        try:
            validate_password(new_password1, user=request.user)
        except Exception:
            messages.error(request, '新密码不符合安全要求，请尝试更复杂的密码。')
            return render(request, 'password_change.html')

        request.user.set_password(new_password1)
        request.user.save(update_fields=['password'])
        login(request, request.user)
        messages.success(request, '密码修改成功。')
        return redirect('profile')

    return render(request, 'password_change.html')


@login_required
def index_view(request):
    recent = list(Diary.objects.filter(user=request.user).order_by('-create_time')[:5])
    today = recent[0] if recent else None
    return render(
        request,
        'index.html',
        {
            'recent_diaries': recent,
            'today_diary': today,
        },
    )
