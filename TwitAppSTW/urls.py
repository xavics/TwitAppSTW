from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'TwitApp.views.welcome_view', name='welcome_page'),
    url(r'^base.html','TwitApp.views.base_html'),
    url(r'^index.html','TwitApp.views.index',name='index'),
    url(r'^register.html','TwitApp.views.register',name='register'),
    url(r'^login.html','TwitApp.views.user_login',name='login'),
    url(r'^logout/$','TwitApp.views.user_logout',name='logout'),
    url(r'^user/(\w+)/$','TwitApp.views.user_profile',),
    url(r'^edit/$','TwitApp.views.editprofile',name='edit'),
)
