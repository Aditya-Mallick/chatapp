from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass']
        try:
            user = User.objects.filter(username=username)
            if not user:
                messages.error(request, ("User does not exist!"))
                return redirect('login')
            else:
                user = authenticate(request, username=username, password=password)
                if not user:
                    messages.error(request, ("Username/Password do not match!"))
                    return redirect('login')
                else:
                    login(request, user)
                    return redirect('home')
        except:
            messages.error(request, ("An error occured while logging in...", "Please Try Again"))
            return redirect('login')
                    
    return render(request, 'chat/loginPage.html')

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        username = request.POST['username']
        p1 = request.POST['password1']
        p2 = request.POST['password2']
        if p1 != p2:
            messages.error(request, ("Passwords do not match"))
            return redirect('register')
        try:
            user = User.objects.get(username=username)
            messages.error(request, ("User already exists"))
        except:
            user = User.objects.create_user(username=username, password=p1)
            user.save()
            login(request, user)
            return redirect('home')
    
    return render(request, 'chat/registerPage.html', {'form': form})

@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        temp = request.POST['temp']
        user = request.user
        msg = Message.objects.create(sender=user, body=temp)
        msg.save()
        return HttpResponse('Message Sent')
    msgs = Message.objects.all()
    context = {'msgs': msgs}
    return render(request, 'chat/temp-home.html', context)

@login_required(login_url='login')
def delete(request, pk):
    if request.method == "POST":
        msg = Message.objects.get(id=pk)
        if msg:
            msg.delete()
            return redirect('home')
    return render(request, 'chat/temp.html')

@login_required(login_url='login')
def profile(request, pk):
    msgs = Message.objects.all().filter(sender__id=pk)
    context = {'msgs': msgs, 'sender': User.objects.get(id=pk).username}
    return render(request, 'chat/profile.html', context)