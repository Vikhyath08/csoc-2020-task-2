from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username != '' and password != '':
            user = authenticate(request, username = username, password = password)
            if user:
                login(request, user)
                return(redirect('/'))
            else:
                print("Wrong username/password")
                messages.error(request,'Wrong Username and/or Password')
        else:
            print("Fill all Fields")
            messages.error(request,'Please Fill Out All The Details')
    return render(request, 'authentication/login_page.html', {})

@login_required
def logoutView(request):
    logout(request)
    return(redirect('/'))

def registerView(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        conf_password = request.POST.get('confpass')
        # print("Password:", password)
        # print("conf_password:", conf_password)
        if username != '' and password != '' and conf_password != '' and first_name != '' and last_name != '' and email != '':
            if password == conf_password:
                try:
                    user = User.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        email = email,
                        username = username,
                        password = password
                    )
                    user.save()
                except:
                    messages.error(request,'Username already exists')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.success(request,'User Registered Successfully.')
            else:
                messages.error(request,'Passwords Do Not Match.')
        else:
            messages.error(request,'Please Fill Out All The Details')
    return render(request, 'authentication/register_page.html', {})