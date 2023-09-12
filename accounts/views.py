from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import UserRegisterForm,UserUpdateForm,UserLoginForm

# Create your views here.

def MainUser(request):
    # 로그아웃 상태면 로그인 화면으로
    if request.user.is_anonymous :
        return redirect('accounts:login')
    return render(request,'home.html')

# 회원가입
def RegisterUser(request):
    if request.method == "POST": # 회원가입 정보 POST로 받기
        form = UserRegisterForm(request.POST)
        if form.is_valid(): # 입력값이 맞으면 홈 화면 연결
            user = form.save(commit=False)
            user.set_password(request.POST['password']) # 비밀번호 암호화
            user.save()
            login(request, user)
            return redirect('home')
    else: # 회원가입 페이지 연결
        form = UserRegisterForm()
    return render(request, 'accounts/register.html',{'form':form})

# 로그아웃
def LogoutUser(request) :
    logout(request)
    return redirect('home')

# 로그인 
def LoginUser(request):
    #  로그인 정보를 POST로 받기
    if request.method == "POST": 
        form = UserLoginForm(request,request.POST)
        if form.is_valid() :
            login(request, form.get_user())
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form' : form})

# 회원탈퇴
def DeleteUser(request) :
    # 로그인 상태인지 확인
    if request.user.is_authenticated :
        request.user.delete() # 유저삭제
        logout(request) # 로그아웃     
    return redirect('accounts:login')

# 유저 정보 변경
def UpdateUser(request):
    # 로그아웃 상태면 로그인 화면으로
    if request.user.is_anonymous :
        return redirect('accounts:login')
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/update.html', {'form':form})

# 유저 비밀번호 변경
def ChangePWUser(request):
    # 로그아웃 상태면 로그인 화면으로
    if request.user.is_anonymous :
        return redirect('accounts:login')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/changePW.html', {'form':form})
