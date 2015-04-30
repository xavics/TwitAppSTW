from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField
from models import Tweet, Favorites, UserProfile

class UserSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='user-detail')
    usr = UserSerialize()
    class Meta:
        model = UserProfile
        fields = ('url','usr','twitter_id','website')

class TweetSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='tweet-detail')
    usr = CharField(read_only=True)
    class Meta:
        model = Tweet
        fields = ('url', 'usr','tweet_str_id','screen_name','user_name','user_tweet_id',
                  'text','time','favorites_count','retweets_count')


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='favorite-detail')
    usr = CharField(read_only=True)
    class Meta:
        model = Favorites
        fields = ('url','name','usr')