from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


# Create your views here.

def register(request):
    if request.method == 'POST':
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        userName = request.POST['user_name']
        email = request.POST['email']
        password = request.POST['password1']
        password1 = request.POST['password2']
        valid = validate(firstName, lastName, userName, email, password, password1)
        if valid[0]:
            user = User.objects.create_user(username=userName, email=email, password=password, first_name=firstName,
                                            last_name=lastName)
            user.save()
            return HttpResponseRedirect(reverse('users:login'))
        else:
            for msg in valid[1]:
                messages.info(request, msg)
    return render(request, 'users/registration.html')


def validate(firstName, lastName, userName, email, password, password1):
    flag = [True, []]
    if password != password1:
        flag[1].append("password doesn't match")
        flag[0] = False
    if User.objects.filter(username=userName).exists():
        flag[0] = False
        flag[1].append(' username already exist')
    if len(password) < 8:
        flag[0] = False
        flag[1].append('password is short')
    return flag


def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=name, password=password)
        if user is not None:
            auth.login(request, user)
            print("successfully logind")
            return HttpResponseRedirect(reverse('log_keepers:index'))
        else:
            messages.info(request, 'wrong crendentials')
    return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('log_keepers:index'))
