from django import forms
from django.contrib.auth.models import User
from profileapp.models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('discord_nickname', 'location', 'record_date')