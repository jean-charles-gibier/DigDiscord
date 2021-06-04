from django import forms
from profileapp.models import Profile, CustomUser


class UzerForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "uzer",
            "discord_nickname",
            "location",
            "record_date",
            "date_debut",
            "date_fin",
            "nb_min_user_messages",
        )
