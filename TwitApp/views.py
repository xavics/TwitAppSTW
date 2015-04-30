from django.shortcuts import render, get_object_or_404, render_to_response
from models import *
from forms import *
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from Twitter import *
# API imports
# from serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer

def base_html(request):
    return render(request, 'base.html', {})


def welcome_view(request):
    form = UserForm()
    if request.user.is_active:
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'index.html', {'sign_up_form': form,})


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
        userProfile.save()
        userdata.save()
        return render(request, 'user.html', {'user_info': request.user.userprofile})
    return render(request, 'user.html', {'user_info': User.objects.get(username=username).userprofile,
                                         'user_form': UserProfileForm()})

@login_required
def editprofile(request):
    return render(request,'editprofile.html',{'user_info': request.user.userprofile})
