from django.shortcuts import render
# from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from profileapp.forms import UserForm, ProfileForm
from profileapp.models import Profile
from django.contrib import messages
from django.shortcuts import redirect
# import pdb
import pprint

@login_required
@transaction.atomic
def update_profile(request):
    profile_form = None
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if hasattr(request.user, 'profile'):
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
        else:
            profile_form = Profile.objects.create(user=request.user)
#        pdb.set_trace()
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('update_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        # pdb.set_trace()
        user_form = UserForm(instance=request.user)
        if hasattr(request.user, 'profile'):
            profile_form = ProfileForm(instance=request.user.profile)
        else:
            profile_form = Profile.objects.create(user=request.user)
    return render(request, 'profileapp/test_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@transaction.atomic
def create_profile(request):
    print("Create profile")
    profile_form = None
    if request.method == "GET":
        u_initial_values = {}
        p_initial_values = {}

        pprint.pprint(request.user)

        if request.user is not None and not request.user.is_anonymous:
            u_initial_values['first_name'] = request.user.first_name
            u_initial_values['last_name'] = request.user.last_name
            u_initial_values['username'] = request.user.username
            u_initial_values['email'] = request.user.email
            p_initial_values['discord_nickname'] = request.user.profile.discord_nickname
            p_initial_values['location'] = request.user.profile.location
            p_initial_values['record_date'] = request.user.profile.record_date
        return render(
            request, "profileapp/test_profile.html",
            {'user_form': UserForm(initial=u_initial_values),
             'profile_form': ProfileForm(initial=p_initial_values)}
        )

    elif request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        if hasattr(request.user, 'profile'):
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
        else:
            profile_form = Profile.objects.create(user=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            auth_login(request, user_form)
            return redirect('update_profile')

