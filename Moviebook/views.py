from Moviebook.models import *
from django.http import Http404
from django.shortcuts import render

def user_profile(request, user_name):
    try:
        usr = Guest.objects.get(username = user_name)
        print(usr)
        followers = len(Follow.objects.filter(following = usr))
        following = len(Follow.objects.filter(follower = usr))
        posts = Post.objects.filter(owner = usr)

    except Guest.DoesNotExist:
        raise Http404

    return render(request, "user_profile.html", {
        'user': usr,
        'follower' : followers,
        'following' : following,
        'posts' : posts
    })


def followers(request, user_name):
    usr = Guest.objects.get(username = user_name)
    followers = Follow.objects.filter(following = usr).values_list("follower", flat=True)
    print(len(followers))
    return render(request, "users_list.html", {
        'list': followers
    })


def followings(request, user_name):
    usr = Guest.objects.get(username = user_name)
    followings = Follow.objects.filter(follower = usr).values_list("following", flat=True)
    return render(request, "users_list.html", {
        'list': followings
    })
