import json
import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from Moviebook.models import *
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from WebProject.settings import MEDIA_ROOT, BASE_DIR
from .form import *

@login_required(login_url='/login/')
def logout_view(request):
    # print("khari")
    logout(request)
    # print("ridam2")
    return redirect('/login/')


def login_view(request):
    # print("ridam1")
    message = ''
    if request.method == "POST":

        form = LoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # user = authenticate(username=username, password=password)
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('/home/')
                else:
                    # not active user
                    message = "This user is deactivated"
            else:
                message = "Username or password is wrong"
        else:
            form = LoginForm()
    form = LoginForm()
    return render(request, "login.html", {
        'form': form,
        'message': message,
    })

def signup(request):
    message = ''
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            # print(request.FILES)
            new_user = form.save(commit=True)
            # new_user = Guest() #.objects.create_user(form.cleaned_data['username'],
            #                                      # form.cleaned_data['email'],
            #                                      # form.cleaned_data['password'])
            # new_user.username = form.cleaned_data['username']
            # # new_user.password = form.cleaned_data['password']
            # new_user.first_name = form.cleaned_data['first_name']
            # new_user.last_name = form.cleaned_data['last_name']
            # new_user.email = form.cleaned_data['email']
            # new_user.birthday = form.cleaned_data['birthday']
            # new_user.gender = form.cleaned_data['gender']
            # # print((form.cleaned_data['birthday'], new_user.birthday))
            # # try:
            new_user.set_password(form.cleaned_data['password'])
            # new_user.avatar = request.FILES['avatar']
            new_user.save()
            # except:
                # pass
            message = "Successfully created"
    else:
        form = SignupForm()
        message = "Unsuccessful creation"
    return render(request, "signup.html", {
        'form': form,
        'message': message,
    })

@login_required(login_url='/login/')
def home(request):
    current_user = Guest.objects.get(username=request.user.username)

    #una e ke followshun mikone
   # usr = request.user #not sure
    posts = Post.objects.all().order_by("-date")
    comments = Comment.objects.all().order_by("-date")
    likes = Like.objects.all()
    # for p in posts:
    #     comments = Comment.objects.filter(post=p).order_by("-date")
    #     dict[p.id] = comments.id
    # print(dict)
    return render(request, "home.html", {
        'posts': posts,
        'current_user': current_user,
        # 'dict': dict,
        'comments': comments,
        'likes': likes,
    })


def show_post(request, post_id):
    post = Post.objects.get(id=post_id)
    # post = Post.objects.filter(owner=usr).get(id)
    return render(request, "post.html", {
        'post': post,
    })



@login_required(login_url='/login/')
def movie_profile(request, movie_name):
    current_user = Guest.objects.get(username=request.user.username)
    try:
        mv = Movie.objects.get(name=movie_name)
        staring = Staring.objects.filter(movie=mv)
        print(mv.summary)
    except Movie.DoesNotExist:
        raise Http404

    return render(request, "movie_profile.html", {
        'movie_name': mv.name,
        'summary': mv.summary,
        'release': mv.release,
        'director': mv.director,
        'writers': mv.writers,
        'reviewers_number': mv.reviewers_number,
        'rate': (mv.rate * 2),
        'stars': (mv.stars * 2),
        'country': mv.country,
        'language': mv.language,
        'IMDB': mv.IMDB,
        'cover': mv.cover,
        'staring': staring,
        'logined_user': current_user
    })


@login_required(login_url='/login/')
def user_profile(request, user_name):
    current_user = Guest.objects.get(username=request.user.username)
    try:
        usr = Guest.objects.get(username = user_name)
        print(usr.first_name)
        followers = Follow.objects.filter(following = usr)
        following = Follow.objects.filter(follower = usr)
        posts = Post.objects.filter(owner = usr).order_by("date")
        temp1 = [x.follower.username for x in followers]
        temp2 = [x.following.username for x in following]
        print(temp1)
    except Guest.DoesNotExist:
        raise Http404

    return render(request, "user_profile.html", {
        'user': usr,
        'current_user': current_user,
        'follower': temp1,
        'following': temp2,
        'posts': posts
    })


def followers(request, user_name):
    usr = Guest.objects.get(username = user_name)
    followers = Follow.objects.filter(following = usr)
    temp = [x.follower for x in followers]
    return render(request, "users_list.html", {
        'list': temp
    })


def followings(request, user_name):
    usr = Guest.objects.get(username = user_name)
    followings = Follow.objects.filter(follower = usr)
    temp = [x.following for x in followings]
    return render(request, "users_list.html", {
        'list': temp
    })


@login_required(login_url='/login/')
def unfollow(request):
    print("got it!")
    if request.method == "POST":
        user_name = request.POST['user']
        print(user_name)
        usr = Guest.objects.get(username=user_name)
        current_user = Guest.objects.get(username=request.user.username)
        Follow.objects.filter(follower=current_user).filter(following=usr).delete()
        status = 1
        return HttpResponse(json.dumps(status), content_type="application/json")


@login_required(login_url='/login/')
def send_post(request):
    print("in viiiiiiew")
    print(request.POST)
    if request.method == "POST":
        myowner = Guest.objects.get(username=request.POST['owner'])
        mymovie_name = Movie.objects.get(name=request.POST['movie_name'])
        mydate = datetime.datetime.now()
        mytext = request.POST['text']
        print(myowner)
        print(mymovie_name)
        print(mydate)
        print(mytext)
        p = Post(date=mydate, owner=myowner, text=mytext, movie_name=mymovie_name)
        print("kdhsajhdskah")
        p.save()
        print("zende am")
        status = 1
        return HttpResponse(json.dumps(status), content_type="application/json")

@login_required(login_url='/login/')
def follow(request):
    if request.method == "POST":
        user_name = request.POST['user']
        print(user_name)
        usr = Guest.objects.get(username=user_name)
        current_user = Guest.objects.get(username=request.user.username)
        f = Follow()
        f.follower = current_user
        f.following = usr
        f.save()
        status = 1
        return HttpResponse(json.dumps(status), content_type="application/json")

#
# def forgot(request, hash):
#     if len(Guest.objects.filter(forgot_hash=hash)):
#         return render(request, 'fucking_template.html')
#
#
# import hashlib
#
# def create_hash(request):
#     email = request.POST['email']
#     sha1 = hashlib.sha1()
#     sha1.update('salam')
#     print(sha1.digest())