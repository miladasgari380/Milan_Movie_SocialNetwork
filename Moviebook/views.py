import json
import datetime
import random
import string
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from Moviebook.models import *
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from WebProject.settings import MEDIA_ROOT, BASE_DIR
from .form import *
from itertools import chain

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def send_new_password(request):
    form = ResetPass(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        usr = Guest.objects.get(email=email)
        print(usr.username)
        new_pass = id_generator(10)
        usr.set_password(new_pass)
        usr.save()
        msg = "Your new password:"
        msg += str(new_pass)
        msg += "\n\n"
        msg += "As you ordered"
        msg += "\n\n"
        msg += "If that wasn't you, login to your account and change it immediately"
        subject = "Password Reset"
        sender = "moviebookteam@gmail.com"
        recipients = [usr.email]
        send_mail(subject, msg, sender, recipients)
        return redirect('/login/')


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')


def login_view(request):
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
            return redirect('/login/')
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
    base_elements = make_base(current_user)

    if not request.method == "POST":
        return render_to_response("home.html", {
            'base_elements': base_elements,
            'current_user': current_user
        }, context_instance=RequestContext(request))
        # return render(request, "home.html", {
        #     'base_elements': base_elements,
        #     'current_user': current_user,
        # })

    flw = Follow.objects.filter(follower=current_user)
    ls = Post.objects.filter(owner=current_user).order_by("-date")
    for fw in flw:
        ls = list(chain(ls, Post.objects.filter(owner = fw.following)))

    ls.sort(key=lambda x: x.date, reverse=True)
    print(len(ls))
    for p in ls:
        print(p.owner.username)
    print("khar jan")
    print(request.POST)
    #     make Posts
    xfrom = int(request.POST['xfrom'])
    xto = int(request.POST['xto'])
    if len(ls) < (xto - xfrom):
        print("al of this")
        posts = ls[:]
    elif xfrom > len(ls):
        print("iam hrerE222")
        posts = ls[len(ls) - 5:]
    elif xto > len(ls):
        print("khar khar")
        posts = ls[len(ls) - 5:]
        print("an")
    else:
        print("iam hrerE333k2lk ")
        posts = ls[xfrom:xto]

    print(len(posts))
    for p in posts:
        print(p.owner.username)
    print("dskhaljdksalkjd")

    # make comments
    comments = []
    likes = []
    for i, p in enumerate(posts):
        posts[i].cnums = len(Comment.objects.filter(post = p))
        posts[i].lnums = len(Like.objects.filter(post=p))
        for c in Comment.objects.filter(post = p):
            comments.append(c)
        for l in Like.objects.filter(post=p):
            likes.append(l)
        if not Like.objects.filter(post=p, user=current_user):
            posts[i].userLike = False
        else:
            posts[i].userLike = True

    comments.sort(key=lambda x: x.date, reverse=False)
    print("khAli khari ")

    for p in posts:
        print(p.owner.username)
    for p in comments:
        print(p.user.username)
    for p in likes:
        print(p.user.username)

    dt = Context({
        "status": 1,
        "posts": posts,
        "comments": comments,
        "likes": likes,
    })
    template = loader.get_template("page.html")
    print("bade home")

    return HttpResponse(template.render(dt))
    # return HttpResponse(json.dumps(dt), content_type="application/json", mimetype="application/json")
    # return render_to_response('home.html', dt)
    # return render_to_json_response

def show_post(request, post_id):
    post = Post.objects.get(id=post_id)
    current_user = Guest.objects.get(username=request.user.username)
    base_elements = make_base(current_user)
    post.cnums = len(Comment.objects.filter(post = post))
    post.lnums = len(Like.objects.filter(post=post))
    comments = Comment.objects.filter(post = post)
    likes = Like.objects.filter(post=post)
    if not Like.objects.filter(post=post, user=current_user):
        post.userLike = False
    else:
        post.userLike = True
    return render(request, "post.html", {
        'base_elements': base_elements,
        'post': post,
        'current_user': current_user,
        'comments': comments,
        'likes': likes
    })



@login_required(login_url='/login/')
def movie_profile(request, movie_name):
    current_user = Guest.objects.get(username=request.user.username)
    base_elements = make_base(current_user)
    try:
        mv = Movie.objects.get(name=movie_name)
        staring = Staring.objects.filter(movie=mv)
        print(mv.summary)
    except Movie.DoesNotExist:
        raise Http404

    return render(request, "movie_profile.html", {
        'base_elements': base_elements,
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
    base_elements = make_base(current_user)
    try:
        usr = Guest.objects.get(username = user_name)
        followers = Follow.objects.filter(following = usr)
        following = Follow.objects.filter(follower = usr)
        temp1 = [x.follower.username for x in followers]
        temp2 = [x.following.username for x in following]

        posts = Post.objects.filter(owner=usr).order_by("-date")
        comments = []
        likes = []
        for i, p in enumerate(posts):
            posts[i].cnums = len(Comment.objects.filter(post = p))
            posts[i].lnums = len(Like.objects.filter(post=p))
            for c in Comment.objects.filter(post = p):
                comments.append(c)
            for l in Like.objects.filter(post=p):
                likes.append(l)
            if not Like.objects.filter(post=p, user=current_user):
                posts[i].userLike = False
            else:
                posts[i].userLike = True
    except Guest.DoesNotExist:
        raise Http404

    return render(request, "user_profile.html", {
        'base_elements': base_elements,
        'user': usr,
        'current_user': current_user,
        'follower': temp1,
        'following': temp2,
        'posts': posts,
        'comments': comments,
        'likes': likes
    })

def followers(request, user_name):
    usr = Guest.objects.get(username = user_name)
    base_elements = make_base(usr)
    followers = Follow.objects.filter(following = usr)
    temp = [x.follower for x in followers]
    return render(request, "users_list.html", {
        'base_elements': base_elements,
        'list': temp
    })


def followings(request, user_name):
    usr = Guest.objects.get(username = user_name)
    base_elements = make_base(usr)
    followings = Follow.objects.filter(follower = usr)
    temp = [x.following for x in followings]
    return render(request, "users_list.html", {
        'base_elements': base_elements,
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
        myrate = request.POST['rate']
        print(myowner)
        print(mymovie_name)
        print(mydate)
        print(mytext)
        print(myrate)
        p = Post(date=mydate, owner=myowner, text=mytext, movie_name=mymovie_name, rate=myrate)
        print("kdhsajhdskah")
        p.save()
        print("zende am")
        status = 1
        return HttpResponse(json.dumps(status), content_type="application/json")

@login_required(login_url='/login/')
def follow(request):
    if request.method == "POST":
        user_name = request.POST['user']
        usr = Guest.objects.get(username=user_name)
        current_user = Guest.objects.get(username=request.user.username)
        f = Follow()
        f.follower = current_user
        f.following = usr
        f.save()
        n = Notification(fromUser=current_user, forUser=usr, msg="start following you!", link="/user_profile/" + current_user.username, read=False)
        n.save()
        status = 1
        return HttpResponse(json.dumps(status), content_type="application/json")

@login_required(login_url='/login/')
def like_post(request):
    print("in like this")
    if request.method == "POST":
        type = request.POST['type']
        username = request.POST['user']
        post_id = request.POST['l_post_id'][4:]

        user = Guest.objects.get(username=username)
        post = Post.objects.get(id=post_id)
        if type == "add":
            l = Like(user=user, post=post)
            l.save()
            n = Notification(fromUser=user, forUser=post.owner, msg="like your post!", link="/post/" + post_id, read=False)
            n.save()
        else:
            Like.objects.filter(user=user, post=post).delete()
        status = 1
        return HttpResponse(json.dumps(status), content_type="application/json")

@login_required(login_url='/login/')
def comment_post(request):
    print("in comment this")
    if request.method == "POST":
        user_name = request.POST['user']
        post_id = request.POST['comment_post_id'][7:]
        text = request.POST['text']

        print(user_name)
        print(text)
        print(post_id)

        user = Guest.objects.get(username=user_name)
        post = Post.objects.get(id=post_id)

        c = Comment(post=post, user=user, text=text, date=datetime.datetime.now())
        c.save()
        n = Notification(fromUser=user, forUser=post.owner, msg="comment on your post", link="/post/" + post_id, read=False)
        n.save()
        status = 1
        return HttpResponse(json.dumps(status), content_type="application/json")

@login_required(login_url='/login/')
def clear_notif(request):
    if request.method == "POST":
        nf_link = request.POST['nf_link']
        print(nf_link)
        nf = Notification.objects.get(id=nf_link)
        print(nf.link)
        print(nf.read)
        nf.read = True
        nf.save()
        print(nf.read)
        status = 1
        return HttpResponse(json.dumps(status), content_type="application/json")

def make_base(current_user):
    user = Guest.objects.filter(username=current_user)
    base_elements = Notification.objects.filter(read=False, forUser=user)
    base_elements.adv_users = Guest.objects.all().order_by('?')[:3]
    base_elements.adv_movies = Movie.objects.all().order_by('?')[:2]
    base_elements.usr = current_user
    return base_elements


@login_required(login_url='/login/')
def settings(request):
    base_elements = make_base(request.user.username)
    current_user = Guest.objects.get(username=request.user.username)
    if request.method == "POST":
        form = SettingForm(request.POST)
        # if form.is_valid():
        print(request.POST)
        # if not new_user.avatar == None:
        #     current_user.avatar = new_user.avatar
        if not request.POST['first_name'] == '':
            current_user.first_name = request.POST['first_name']
        if not request.POST['last_name'] == '':
            current_user.last_name = request.POST['last_name']
        if not request.POST['email'] == '':
            current_user.email = request.POST['email']
        if not request.POST['password'] == '':
            current_user.set_password(request.POST['password'])
        # if not request.POST['birthday'] == '':
        #     current_user.birthday = request.POST['birthday']
        current_user.save()
        print(current_user.first_name)
        return redirect('/home/')

    form = SettingForm()
    return render(request, "settings.html", {
        'base_elements': base_elements,
        'current_user': current_user,
        'form': form,
    })


def get_options(request):
    print("khar jaaaan")
    if request.method == "POST":
        ans = []
        for us in Guest.objects.all():
            ans.append(us.first_name)
            ans.append(us.last_name)
        for mv in Movie.objects.all():
            ans.append(mv.name)

        return HttpResponse(json.dumps(ans), content_type="application/json")


@login_required(login_url='/login/')
def search(request):
    base_elements = make_base(request.user.username)
    if request.method == "POST":
        elem = request.POST['currency']
        fmovies = Movie.objects.filter(Q(name=elem) | Q(director=elem))
        for fm in fmovies:
            fm.rate = fm.rate * 2
        fusers = Guest.objects.filter(Q(username=elem) | Q(first_name=elem) | Q(last_name=elem))
        for fu in fusers:
            fl = Follow.objects.filter(following=fu)
            fu.followers = []
            for l in fl:
                fu.followers.append( l.follower.username )
            print(fu.followers)
        current_user = Guest.objects.get(username=request.user.username)
        return render(request, "search.html", {
            'base_elements': base_elements,
            'fmovies': fmovies,
            'fusers': fusers,
            'current_user': current_user
        })

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