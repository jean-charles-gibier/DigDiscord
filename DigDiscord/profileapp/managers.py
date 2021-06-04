from django.contrib.auth.base_user import BaseUserManager
import sys
from profileapp.models import Profile as prof, CustomUser as cu


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))  # noqa
        email = self.normalize_email(email)
        try:
            user = cu.objects.create(email=email, password=password, **extra_fields)

            pr = prof.objects.create(
                uzer=user,
                discord_nickname=extra_fields["discord_nickname"]
                if "discord_nickname" in extra_fields
                else "discord_nickname",
                location=extra_fields["location"]
                if "location" in extra_fields
                else "location",
                record_date=extra_fields["record_date"]
                if "record_date" in extra_fields
                else "2021-03-21",
            )

            pr.save()
            return pr

        except Exception:
            print("Erreur: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))  # noqa
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))  # noqa
        return self.create_user(email=email, password=password, **extra_fields)
