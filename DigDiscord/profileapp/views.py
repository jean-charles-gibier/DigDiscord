from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.decorators import login_required
from profileapp.forms import UzerForm, ProfileForm
from profileapp.models import Profile, CustomUser
from django.contrib import messages
from django.shortcuts import redirect

# import pdb
import pprint

import sys


@login_required
@transaction.atomic
def update_profile(request):
    # profile_form = None
    if request.method == "POST":
        user_form = UzerForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("update_profile")
        else:
            # messages.error(request, 'Please correct the error below.')
            print(
                "Erreur update_profile : [{}] [{}]".format(
                    sys.exc_info()[0], sys.exc_info()[1]
                )
            )
    else:
        user_form = UzerForm(instance=request.user)
        if hasattr(request.user, "profile"):
            profile_form = ProfileForm(instance=request.user.profile)
        else:
            profile_form = Profile.objects.create(**request.user.profile)
    return render(
        request,
        "profileapp/test_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
@transaction.atomic
def create_profile(request):
    # profile_form = None
    if request.method == "GET":
        u_initial_values = {}
        p_initial_values = {}

        if request.user is not None and not request.user.is_anonymous:
            u_initial_values["first_name"] = request.user.first_name
            u_initial_values["last_name"] = request.user.last_name
            u_initial_values["username"] = request.user.username
            u_initial_values["email"] = request.user.email
            p_initial_values["discord_nickname"] = request.user.profile.discord_nickname
            p_initial_values["location"] = request.user.profile.location
            p_initial_values["record_date"] = request.user.profile.record_date
            p_initial_values["date_debut"] = request.user.profile.date_debut
            p_initial_values["date_fin"] = request.user.profile.date_fin
            p_initial_values[
                "nb_min_user_messages"
            ] = request.user.profile.nb_min_user_messages
        return render(
            request,
            "profileapp/test_profile.html",
            {
                "user_form": UzerForm(initial=u_initial_values),
                "profile_form": ProfileForm(initial=p_initial_values),
            },
        )

    elif request.method == "POST":
        profile_form = ProfileForm(request.POST)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            # auth_login(request, user_form)
            return redirect("update_profile")
        else:
            print("profile_form.errors")
            print(profile_form.errors)
            print(
                "Erreur create_profile : [{}] [{}]".format(
                    sys.exc_info()[0], sys.exc_info()[1]
                )
            )
