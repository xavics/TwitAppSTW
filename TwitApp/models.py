from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    twitter_id = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Favorites(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30, unique = True)

    def __unicode__(self):
        return '%s' % self.name

class Tweet(models.Model):
    user = models.ForeignKey(User)
    tweet_str_id = models.CharField(max_length = 100, unique = True)
    screen_name = models.CharField(max_length = 100)
    user_name = models.CharField(max_length = 100)
    user_tweet_id = models.CharField(max_length = 100)
    text = models.CharField(max_length=140)
    time = models.TextField()
    favorites_count = models.IntegerField()
    retweets_count = models.IntegerField()
