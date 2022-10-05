from cmath import log
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.
def userRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        resim = request.FILES['resim']
        tel = request.POST['tel']
        sifre1 = request.POST['password1']
        sifre2 = request.POST['password2']

        if sifre1 == sifre2:
            if User.objects.filter(username = username).exists():
                messages.error(request,'Bu kullanıcı adı kullanımda.')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'E-posta adresi kullanımda.')
                return redirect('register')
            elif username in sifre1:
                messages.error(request, 'Kullanıcı adı ve şifre benzer olamaz.')
                return redirect('register')
            elif len(sifre1)<6:
                messages.error(request, 'Şifreniz en az altı karakter olmalıdır.')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, email = email, password = sifre1)
                Account.objects.create(
                    user = user,
                    resim = resim,
                    tel = tel,
                )
                user.save()
                messages.success(request, 'Kullanıcı oluşturuldu.')
                return redirect('index')
        else:
            messages.error(request, 'Şifreler aynı olmalı.')
            return redirect('register')

    return render(request, 'user/register.html')

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        sifre = request.POST['password']

        user = authenticate(request, username = username, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş yapıldı.')
            return redirect('profiles')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
            return redirect('login')
    return render(request, 'user/login.html')

def userLogout(request):
    logout(request)
    messages.success(request, 'Çıkış başarılı.')
    return redirect('index')

def profile(request):
    profiles = Profile.objects.filter(user = request.user)
    context = {
        'profiles' : profiles
    }
    return render(request, 'browse.html', context)

def createProfile(request):
    form = ProfileForm()
    profile = Profile.objects.filter(user = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if len(profile) < 4:
            if form.is_valid():
                profil = form.save(commit = False)
                profil.user = request.user
                profil.save()
                messages.success(request, 'Profil Oluşturuldu')
                return redirect('profiles')
        else:
            messages.error(request, 'Profil sayısı 4ten fazla olamaz.')
            return redirect('profile')
    
    contex = {
        'form' : form,
    }
    return render(request, 'user/createProfile.html', contex)

def hesap(request):
    user = request.user.account
    context = {
        'user' : user,
    }
    return render(request, 'user/hesap.html', context)

def userDelete(request):
    user = request.user
    user.delete(request, user)
    messages.success(request, 'Kullanıcı silindi')
    return redirect('index')

def update(request):
    user = request.user.account
    form = AccountForm(instance = user)
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil güncellendi.')
            return redirect('hesap')
    context = {
        'form' : form,
    }
    return render(request, 'user/update.html', context)