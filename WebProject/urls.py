from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()
from django.views.generic.base import TemplateView

__author__ = 'vaio'

from django.conf.urls import patterns, url
from Moviebook import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WebProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', views.home, name='home'), #on action
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^post/(\d+)/$', views.show_post, name='post'), #nearly done
    url(r'^user_profile/(\w+)/$', views.user_profile, name="user_profile"),
    url(r'^followers/(\w+)/$', views.followers, name="user_followers"), #done
    url(r'^followings/(\w+)/$', views.followings, name="user_followings"), #done
    url(r'^movie_profile/$', TemplateView.as_view(template_name='movie_profile.html'), name="movie_profile"),
    url(r'^search/$', TemplateView.as_view(template_name='search.html'), name='search'),
    # url(r'^forgot/(?P<hash>\w+)/$', views.forgot, name='forgot_password'),
)
