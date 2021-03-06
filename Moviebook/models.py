from django.db import models
from django.contrib.auth.models import User, AbstractUser



class Guest(User):
    # user = models.OneToOneField(User)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    avatar = models.ImageField(upload_to="img/users/", blank=True, null=True)
    # forgot_hash = models.CharField(max_length=100, default='')

#####another way####
# class Guest(models.Model):
#     user  = models.OneToOneField(User)
#     .....


class Follow(models.Model):
    follower = models.ForeignKey(Guest, related_name="follower")
    following = models.ForeignKey(Guest, related_name="following")


class Movie(models.Model):
    name = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    release = models.DateField() #we need year of that
    director = models.CharField(max_length=100)
    writers = models.CharField(max_length=100)
    reviewers_number = models.IntegerField()
    rate = models.FloatField(default=0.0)
    stars = models.FloatField(default=0.0)
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    IMDB = models.CharField(max_length=100)
    cover = models.ImageField(upload_to="img/movies/", blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    movie_name = models.ForeignKey(Movie)
    owner = models.ForeignKey(Guest)
    date = models.DateTimeField()
    text = models.CharField(max_length=1000)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return str(self.owner.first_name + " " + self.owner.last_name + " about " + self.movie_name.name)

class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(Guest)
    date = models.DateTimeField()
    text = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name + " about " + self.post.movie_name.name)

class Like(models.Model):
    user = models.ForeignKey(Guest)
    post = models.ForeignKey(Post)

class Cast(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.name)

class Staring(models.Model):
    actor = models.ForeignKey(Cast)
    movie = models.ForeignKey(Movie)
    role = models.CharField(max_length=100)

    def __str__(self):
        return str(self.actor.name + " stars in " + self.movie.name)

class Message(models.Model):
    from_msg = models.ForeignKey(Guest, related_name="From")
    to_msg = models.ForeignKey(Guest, related_name="To")
    msg = models.CharField(max_length=100)
    time = models.DateTimeField()

    def __str__(self):
        return str("from: " + self.from_msg + " to: " + self.to_msg)

possible_msg=(
    (0, "like your post!"),
    (1, "comment on your post"),
    (2, "start following you!"),
    (3, "also comment on...")
)

class Notification(models.Model):
    forUser = models.ForeignKey(Guest, related_name="foruser", null=True)
    fromUser = models.ForeignKey(Guest, related_name="fromuser", null=True)
    msg = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name + " " + self.msg)
