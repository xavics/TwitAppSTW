from django.contrib.auth.models import User
from models import UserProfile
from django import forms
from django.forms.models import model_to_dict, fields_for_model

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')

class UserProfileForm(forms.ModelForm):
    def __init__(self, instance=None, *args, **kwargs):
        _fields = ('username','password','first_name', 'last_name', 'email',)
        _initial = model_to_dict(instance.user, _fields) if instance is not None else {}
        super(UserProfileForm, self).__init__(initial=_initial, instance=instance, *args, **kwargs)
        self.fields.update(fields_for_model(User, _fields))

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.username = self.cleaned_data['username']
        u.password = self.cleaned_data['password']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(UserProfileForm, self).save(*args,**kwargs)
        return profile
