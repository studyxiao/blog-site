from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout

from .forms import UserForm, UserProfileForm


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'portrait' in request.FILES:
                profile.portrait = request.FILES['portrait']
            profile.save()
            registered = True

        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'user/register.html',
                  dict(user_form=user_form, profile_form=profile_form, registered=registered))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('账户没有激活')

        else:
            return HttpResponse('账户信息错误')
    else:
        return render(request,'user/login.html', {})


def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')
