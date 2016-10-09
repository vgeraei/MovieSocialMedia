from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from ourapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MSN.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.my_login),
    url(r'^logout/$', views.my_logout),
    url(r'^signup/$', views.signup),
    url(r'^forgot/$', views.forgot),
    url(r'^reset/$', views.reset),
    url(r'^timeline/$', views.timeline),
    url(r'^timeline/(?P<post_id>\d+)/$', views.posts),
    url(r'^profile/(?P<username>\w+)/change/$', views.change),
    url(r'^profile/(?P<username>\w+)/$', views.profile),
    url(r'^movie/(?P<name>\w+)/$', views.movie),
    url(r'^comment/(?P<post_id>\d+)$', views.comment),
    url(r'^like/(?P<post_id>\d+)$', views.like),
    url(r'^post/(?P<name>\w+)/$', views.post),
    #url(r'^follow/$', views.follow),
    #url(r'^unfollow/$', views.unfollow),
    #url(r'^followers/$', views.followers),
    #url(r'^following/$', views.following),
    #url(r'^notification/$', views.notification),
    #url(r'^search/$', views.search),
    #url(r'^people_searched/$', views.people_searched),
    #url(r'^movies_searched/$', views.movies_searched),
    #url(r'^infinite_scroll/$', views.infinite_scroll),
)

urlpatterns += patterns('django.views.static', (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
                        )
urlpatterns += patterns('', url(r'^captcha/', include('captcha.urls')),)