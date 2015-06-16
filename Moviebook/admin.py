from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Cast)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Guest)
admin.site.register(Like)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Post)
admin.site.register(Staring)
admin.site.register(Movie)