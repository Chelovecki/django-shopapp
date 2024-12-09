from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import gettext_lazy as _


def generate_profile_images_path(instance: "Profile", filename: str) -> str:
    return "users/{pk}/avatars/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ФИО
    first_name = models.CharField(max_length=15, blank=True, verbose_name=_('First name'))
    middle_name = models.CharField(max_length=15, blank=True, verbose_name=_('Middle name'))
    last_name = models.CharField(max_length=20, blank=True, verbose_name=_('Last name'))

    number = models.CharField(max_length=15, blank=True, verbose_name=_('Phone number'))

    bio = models.TextField(blank=True, verbose_name=_('Bio'))

    agree_save_data = models.BooleanField(default=True, verbose_name=_('Save personal data'))

    avatar = models.ImageField(null=True, blank=True, upload_to=generate_profile_images_path,
                               verbose_name=_('Avatar'))
