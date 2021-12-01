import random
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from post_app.models import Post,Comment
from worldvision_django import settings


def index(request):
    news = Post.objects.all()
    b_news = random.sample(list(news), 4)
    carousel_news = random.sample(list(news), 3)
    world_news = Post.objects.filter(
        category='World').order_by('-date_added')[:4]
    business_news = Post.objects.filter(
        category='Business').order_by('-date_added')[:4]
    sports_news = Post.objects.filter(
        category='Sports').order_by('-date_added')[:4]
    params = {'date': date.today(), 'news': news, 'b_news': b_news,
              'aside': random.sample(list(news), 6)[:6], 'c_news': carousel_news, 'world_news': world_news, 'business_news': business_news, 'sports_news': sports_news,
              'latest_news': news.order_by('-date_added')[:4], 'popular_news': random.sample(list(news), 4), 'pnews': news[random.randint(0, len(news))]}

    return render(request, 'index.html', params)


def signin(request):
    ip_address = request.META.get('REMOTE_ADDR')
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            url = request.GET.get('next')
            sub = 'Login'
            msg = f'Dear {request.user.first_name} {request.user.last_name}, did you just login in World Vision from this {ip_address}. If not please change your password. Thank you'
            email_from = settings.EMAIL_HOST_USER
            email_to = [request.user.email]
            send_mail(sub, msg, email_from, email_to)

            if url is not None:
                return redirect(url)
            else:
                return redirect('index')

        else:
            messages.error(request, 'Invalid Username or Password')
            return render(request, 'signin.html')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('index')


@login_required(login_url='signin')
def addpost(request):
    if request.method == 'GET':
        return render(request, 'addpost.html', {'date': date.today()})
    else:
        title = request.POST['title']
        body = request.POST['body']
        cat = request.POST['cat']
        file = request.FILES['image']

        item = Post.objects.create(
            post_title=title, post_body=body, category=cat, img=file, author=request.user)
        item.save()
        messages.success(request, 'News added succesfully')
        return redirect('index')


def viewpost(request, id):
    item = Post.objects.get(id=id)
    you_may_like_news = random.sample(list(Post.objects.all()[:3]), 2)
    comments = Comment.objects.filter(post=item)

    if request.method == 'GET':
        return render(request, 'viewpost.html', {'item': item, 'you_may_like_news': you_may_like_news, 'comments': comments})
    else:
        comment = request.POST['comment']
        create = Comment.objects.create(
            comment=comment, author=request.user, post=item)
        create.save()
        return render(request, 'viewpost.html', {'item': item, 'you_may_like_news': you_may_like_news, 'comments': comments})


@login_required(login_url='signin')
def myaccount(request):

    news = Post.objects.filter(author=request.user)
    return render(request, 'myaccount.html', {'news': news})


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
def delete(request, id):
    news = Post.objects.get(id=id)
    news.delete()
    return redirect('mypost')


def catpage(request, slug):
    news = reversed(Post.objects.filter(category=slug))
    print(news)
    return render(request, 'catpage.html', {'slug': slug, 'news': news})


@login_required(login_url='signin')
def create(request):
    if request.method == 'GET':
        return render(request, 'createaccount.html')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create(
            first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.save()

        return redirect('index')


def search(request):
    query = request.GET['query']
    result_title = Post.objects.filter(post_title__contains=query)
    result_body = Post.objects.filter(post_body__contains=query)
    result = result_title.union(result_body)
    return render(request, 'search.html', {"result": result, "query": query, 'len': len(result)})


@login_required(login_url='signin')
def edit(request, id):
    post = Post.objects.get(id=id)

    if request.method == 'GET':
        return render(request, 'edit.html', {'news': post})
    else:
        post.post_title = request.POST['title']
        post.post_body = request.POST['body']
        post.category = request.POST['cat']
        post.img = request.FILES['image']

        post.save()
        messages.success(request, 'News added succesfully')
        return redirect('index')
