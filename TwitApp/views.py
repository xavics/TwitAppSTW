import ast
import sys

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer
from django.template import RequestContext

from forms import *
from Twitter import *

# API imports
from serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


def base_html(request):
    return render(request, 'base.html', {})


def welcome_view(request):
    form = UserForm()
    if request.user.is_active:
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'index.html', {'sign_up_form': form,})

@login_required
def index(request):
    form = UserForm()
    return render(request, 'mainpage.html', {
        'search_form': form
    })


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/login.html')
        else:
            return HttpResponse(user_form.errors)
    else:
        user_form = UserForm()
        return render(request, 'register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # User exist in our database
        if user:
            # Is active
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index.html')
            else:
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid log details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid log details")
    # si la request no es un HTTP POST se mostre el loguin form.
    else:
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login.html')

@login_required
def user_profile(request, username):
    if request.method=='POST':
        twitter_id = request.POST.get('twitter_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        location = request.POST.get('location')
        userProfile = request.user.userprofile
        userdata = request.user
        if first_name != "":
            userdata.first_name = first_name
        if last_name != "":
            userdata.last_name = last_name
        if email != "":
            userdata.email = email
        if twitter_id != "":
            userProfile.twitter_id = twitter_id
        if website != "":
            userProfile.website = website
        if location != "":
            userProfile.location = location
        userProfile.save()
        userdata.save()
        return render(request, 'user.html', {'user_info': request.user.userprofile})
    return render(request, 'user.html', {'user_info': User.objects.get(username=username).userprofile,
                                         'user_form': UserProfileForm()})

@login_required
def edit_profile(request):
    return render(request,'editprofile.html',{'user_info': request.user.userprofile})

@login_required
def get_tweets_view(request):
    auth = get_oauth()
    topics = get_trendy_topics(auth)
    trendy_topics = select_trendy_topics(topics)
    saved_tweets = Tweet.objects.filter(usr=request.user).values_list('tweet_str_id', flat=True)
    favorites_user = Favorites.objects.filter(usr=request.user).values_list('name', flat=True)
    print favorites_user
    return render(request, 'view_tweets.html', {'saved_tweets':saved_tweets,
                                                'trendy_topics': trendy_topics,
                                                'favorites_user': favorites_user})

@login_required
def add_favorite(request):
    if request.method == 'GET':
        favorite = request.GET.get('screenname')
        entry = Favorites(usr=request.user, name=favorite)
        entry.save()
        return HttpResponse("Delete Favorite")
    return HttpResponse('<h1>Adding tweet bad method<h1>')

@login_required
def delete_favorite(request):
    if request.method == 'GET':
        favorite = request.GET.get('screenname')
        type = request.GET.get('type')
        entry = Favorites.objects.filter(name=favorite)
        try:
            entry.delete()
        except:
            print "Delete error", sys.exc_info()
            raise
        if type == 'search':
            return HttpResponse("Add Favorite")
        else:
            return HttpResponse("deleted")
    return HttpResponse('<h1>Delete favorite bad method<h1>')

@login_required
def save_tweet(request):
    if request.method == 'GET':
        data = request.GET.get('tweet')
        item = ast.literal_eval(data)
        tweet_id = unicode(item[u'twit_id'])
        user_id = unicode(item[u'user_id'])
        name = unicode(item[u'name'])
        screen_name = unicode(item[u'screen_name'])
        time = unicode(item[u'time'])
        favorites = unicode(item[u'favorites'])
        retweets = unicode(item[u'retweets'])
        text = unicode(item[u'text'])
        try:
            entry = Tweet(usr=request.user, tweet_str_id=tweet_id, user_name=name, user_tweet_id=user_id,
                          favorites_count=int(favorites), retweets_count=int(retweets), time=time,
                          screen_name=screen_name, text= text)
        except:
            print "Error making entry", sys.exc_info()
            raise
        try:
            entry.save()
        except:
            print "Saving Error", sys.exc_info()
            raise
        response = HttpResponse()
        response.write("Delete Tweet")
        return response
    return HttpResponse("<h1>Save tweet bad method<h1>")

@login_required
def delete_tweet(request):
    if request.method == 'GET':
        data = request.GET.get('tweet')
        type = request.GET.get('type')
        if type == "myTwits":
            tweet_id = data
        else:
            item = ast.literal_eval(data)
            t_id = unicode(item[u'twit_id'])
            tweet_id = str(t_id)
        entry = Tweet.objects.filter(usr=request.user).filter(tweet_str_id=tweet_id)
        try:
            entry.delete()
        except:
            print "Deleting Error", sys.exc_info()
            raise
        return HttpResponse("Save tweet")
    return HttpResponse('<h1>Delete tweet bad method<h1>')

@login_required
def search_twits(request):
    auth = get_oauth()
    saved_tweets = Tweet.objects.filter(usr=request.user).values_list('tweet_str_id', flat=True)
    if request.method == 'GET':
        if request.GET.has_key('query'):
            query = request.GET.get('query')
            count = request.GET.get('count')
            data = get_tweets_search(auth,query,count)
            r = select_search_tweets(data)
            tweets = show_tweets(r)
            if tweets:
                return render(request, 'search_twits.html', {'tweets': tweets,
                                                            'saved_tweets': saved_tweets})
            else:
                return render(request, 'search_twits.html', {'errors': {'type': "search", 'data': query}})
        else:
            screen_user = request.GET.get('screen_user')
            count = request.GET.get('count')
            r = get_tweets(auth, screen_user, count)
            data = load_json_object(r)
            tweets = show_tweets(data)
            if tweets:
                return render(request, 'search_twits.html', {'tweets': tweets,
                                                            'saved_tweets': saved_tweets})
            else:
                return render(request, 'search_twits.html', {'errors': {'type': "user", 'data': screen_user}})
    return HttpResponse("<h1>Search tweet bad method<h1>")

@login_required
def user_twitter_view(request):
    if request.method == 'GET':
        auth = get_oauth()
        name = request.GET.get('data')
        r = get_user_information(auth, name)
        data = load_json_object(r)
        info_user = make_user_information(data)
        favorites = Favorites.objects.filter(usr=request.user).values_list('name', flat=True)
        return render(request, 'twitterUser_info.html', {'screen_user': name,
                                                 'infouser': info_user,
                                                 'favorites': favorites})
    return HttpResponse("<h1>Ger user Twitter bad method<h1>")

@login_required
def favorite_user_twits(request):
    if request.method == 'GET':
        auth = get_oauth()
        name = request.GET.get('data')
        r = get_user_information(auth, name)
        data = load_json_object(r)
        info_user = make_user_information(data)
        tweets = Tweet.objects.filter(usr=request.user).filter(screen_name=info_user['screen_name'])
        return render(request, 'favorite_user_twits.html', {'infouser': info_user,
                                                            'tweets':tweets})

@login_required
def saved_twits(request):
    saved_tweets = Tweet.objects.filter(usr=request.user)
    favorites = Favorites.objects.filter(usr=request.user).values_list('name', flat=True)
    return render(request, 'saved_twits.html', {'tweets': saved_tweets,
                                                'favorites': favorites})

class CustomTemplateHTMLRenderer(TemplateHTMLRenderer):

    def resolve_context(self, data, request, response):
        if response.exception:
            data['status_code'] = response.status_code
        data = {'data': data}
        return RequestContext(request, data)

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API
    """
    return Response({
        'users': reverse('user-list', request=request),
        'tweets': reverse('tweet-list', request=request),
    })


class APIUserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialize
    template_name = 'api_list.html'
    renderer_classes = (BrowsableAPIRenderer,CustomTemplateHTMLRenderer,JSONRenderer,XMLRenderer)


class APIUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialize
    template_name = 'api_detail.html'
    renderer_classes = (BrowsableAPIRenderer,CustomTemplateHTMLRenderer,JSONRenderer,XMLRenderer)


class APIUserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    renderer_classes = (BrowsableAPIRenderer,CustomTemplateHTMLRenderer,JSONRenderer,XMLRenderer)
    template_name = 'api_list.html'


class APIUserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    renderer_classes = (BrowsableAPIRenderer,CustomTemplateHTMLRenderer,JSONRenderer,XMLRenderer)
    template_name = 'api_detail.html'


class APITweetList(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    renderer_classes = (BrowsableAPIRenderer,CustomTemplateHTMLRenderer,JSONRenderer,XMLRenderer)
    template_name = 'api_list.html'


class APITweetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    renderer_classes = (BrowsableAPIRenderer,CustomTemplateHTMLRenderer,JSONRenderer,XMLRenderer)
    template_name = 'api_detail.html'


class APIFavoriteList(generics.ListCreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    renderer_classes = (BrowsableAPIRenderer,CustomTemplateHTMLRenderer,JSONRenderer,XMLRenderer)
    template_name = 'api_list.html'


class APIFavoriteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    renderer_classes = (BrowsableAPIRenderer,CustomTemplateHTMLRenderer,JSONRenderer,XMLRenderer)
    template_name = 'api_detail.html'
