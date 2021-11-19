import random
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from post_app.models import Post

def index(request):
    news = Post.objects.all()
    b_news = random.sample(list(news),4)
    carousel_news = random.sample(list(news),3)
    return render(request, 'index.html', {'date': date.today(),'news':news,'b_news':b_news,'aside': news[:4],'c_news':carousel_news})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username , password = password)

        if user is not None:
            login(request, user)
            url = request.GET.get('next')
           
            if url is not None:
                return redirect(url)
            else: 
                return redirect('index')
        
        else:
            messages.error(request,'Invalid Username or Password')
            return render(request, 'signin.html')
            
def signout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='signin')
def addpost(request):
    if request.method == 'GET':
        return render(request, 'addpost.html',{'date': date.today()})
    else:
        title = request.POST['title']
        body = request.POST['body']
        cat = request.POST['cat']
        file = request.FILES['image']

        item = Post.objects.create(post_title=title,post_body=body,category=cat,img=file,author = request.user)
        item.save()
        messages.success(request,'News added succesfully')
        return redirect('index')

def viewpost(request, id):
    item = Post.objects.get(id=id)
    return render(request, 'viewpost.html',{'item':item})

    
@login_required(login_url='signin')
def myaccount(request):
    return render(request, 'myaccount.html')

@login_required(login_url='signin')
def changepassword(requset):
    current_password = requset.POST['current_password']
    new_password = requset.POST['new_password']
    password = requset.user.password
    check = check_password(current_password, password)
    
    if check:
        u = User.objects.get(username=requset.user)
        u.set_password(new_password)
        u.save()
        return redirect('myaccount')
    else:
        return HttpResponse('FAKE PASSWORD')

@login_required(login_url='signin')
def mypost(request):
    news = Post.objects.filter(author = request.user)
    return render(request, 'mypost.html', {'news': news})

@login_required(login_url='signin')
def delete(request, id):
    news = Post.objects.get(id=id)
    news.delete()
    return redirect('mypost')