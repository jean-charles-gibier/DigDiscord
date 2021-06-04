from django.urls import re_path
from .views import update_profile, create_profile

urlpatterns = [
    re_path(r"update", update_profile, name="update_profile"),
    re_path(r"create", create_profile, name="create_profile"),
]
