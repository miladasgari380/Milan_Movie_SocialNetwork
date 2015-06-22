from Moviebook.models import *
from django.http import Http404
from django.shortcuts import render

def home(request):
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

def user_profile(request, user_name):
    try:
        usr = Guest.objects.get(username = user_name)
        followers = len(Follow.objects.filter(following = usr))
        following = len(Follow.objects.filter(follower = usr))
        posts = Post.objects.filter(owner = usr).order_by("date")

    except Guest.DoesNotExist:
        raise Http404

    return render(request, "user_profile.html", {
        'user': usr,
        'follower': followers,
        'following': following,
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
