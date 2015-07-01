from django.conf.urls import patterns, include, url
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib import admin
from WebProject import settings

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
    url(r'^home/$', views.home, name='home'), #done
    url(r'^login/$', views.login_view, name='login'), #Error chapcha
    url(r'^signup/$', views.signup, name='signup'), # Email zadan
    url(r'^post/(\d+)/$', views.show_post, name='post'), #
    url(r'^user_profile/(\w+)/$', views.user_profile, name="user_profile"), #
    url(r'^followers/(\w+)/$', views.followers, name="user_followers"), #done
    url(r'^followings/(\w+)/$', views.followings, name="user_followings"), #done
    url(r'^movie_profile/(\w+)/$', views.movie_profile, name="movie_profile"), #done
    url(r'^search/$', TemplateView.as_view(template_name='search.html'), name='search'),
    url(r'^logout/$', views.logout_view , name='logout'), #done
    url(r'^follow/$', views.follow, name= 'follow'), #done
    url(r'^unfollow/$', views.unfollow, name= 'unfollow'), #done
    url(r'^sendpost/$', views.send_post, name= 'sendpost'), #done
    url(r'^likethis/$', views.like_post, name= 'likethis'), #done
    url(r'^commentthis/$', views.comment_post, name= 'commentthis'), #done
    url(r'^clearnotif/$', views.clear_notif, name= 'clearnotif'), #done
    url(r'^settings/$', views.settings , name='settings'), #done
    url(r'^newpassword/$', views.send_new_password, name="sendnewpass"),

    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    # url(r'^forgot/(?P<hash>\w+)/$', views.forgot, name='forgot_password'),

)
urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
)
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += patterns('',
#     url(r'^captcha/', include('captcha.urls')),
# )
