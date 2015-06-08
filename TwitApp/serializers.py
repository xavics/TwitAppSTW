from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField
from models import Tweet, Favorites, UserProfile

class UserSerialize(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='user-detail')
    userprofile = HyperlinkedRelatedField(read_only=True, view_name='userProfile-detail')
    tweet = HyperlinkedRelatedField(many=True, read_only=True, view_name='tweet-detail')
    favorite = HyperlinkedRelatedField(many=True, read_only=True, view_name='favorite-detail')
    class Meta:
        model = User
        fields = ('url','username','first_name','last_name','email', 'userprofile','tweet', 'favorite')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='userProfile-detail')
    usr = HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    class Meta:
        model = UserProfile
        fields = ('url','usr','twitter_id','website', 'country', 'region', 'location', 'map', 'street', 'postalCode')

class TweetSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='tweet-detail')
    usr = HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    class Meta:
        model = Tweet
        fields = ('url', 'usr','tweet_str_id','screen_name','user_name','user_tweet_id',
                  'text','time','favorites_count','retweets_count')


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='favorite-detail')
    usr = HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    class Meta:
        model = Favorites
        fields = ('url','name','usr')