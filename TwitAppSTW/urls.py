from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from TwitApp.views import APIUserList, APIUserDetail, APITweetList, APITweetDetail, APIFavoriteDetail, APIFavoriteList, APIUserProfileDetail, APIUserProfileList
from rest_framework.urlpatterns import format_suffix_patterns
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
    url(r'^edit/$', 'TwitApp.views.edit_profile',name='edit'),
    #Tweet funcionality URL
    url(r'^view_tweets.html','TwitApp.views.get_tweets_view',name='view_tweets'),
    url(r'^add_favorites/$','TwitApp.views.add_favorite',name='add_favorites'),
    url(r'^search/$','TwitApp.views.search_twits',name='search_twits'),
    url(r'^user_twitter_view/$', 'TwitApp.views.user_twitter_view',name='search_twits'),
    url(r'^delete_favorites/$','TwitApp.views.delete_favorite',name='delete_favorites'),
    url(r'^save_tweet/$','TwitApp.views.save_tweet',name='save_tweet'),
    url(r'^delete_tweet/$','TwitApp.views.delete_tweet',name='delete_tweet'),
    url(r'^twits/$','TwitApp.views.saved_twits',name='twits'),
    url(r'^favorite_user_tweets/$', 'TwitApp.views.favorite_user_twits',name='favorite_user_twits'),
    #Media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.BASE_DIR+'/TwitApp'+settings.MEDIA_URL}),
    #API Rest
    url(r'^api/users/$',APIUserList.as_view(),name='user-list'),
    url(r'^api/users/(?P<pk>\d+)/$',APIUserDetail.as_view(),name='user-detail'),
    url(r'^api/userProfiles/$',APIUserProfileList.as_view(),name='userProfile-list'),
    url(r'^api/userProfiles/(?P<pk>\d+)/$',APIUserProfileDetail.as_view(),name='userProfile-detail'),
    url(r'^api/tweets/$',APITweetList.as_view(),name='tweet-list'),
    url(r'^api/tweets/(?P<pk>\d+)/$',APITweetDetail.as_view(),name='tweet-detail'),
    url(r'^api/favorites/$',APIFavoriteList.as_view(),name='favorite-list'),
    url(r'^api/favorites/(?P<pk>\d+)/$',APIFavoriteDetail.as_view(),name='favorite-detail')
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json','html','xml','api'])