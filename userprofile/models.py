from django.db import models
from django.utils.translation import gettext_lazy as _
from core import User
# Create your models here.


class Profile(models.Model):
    """
    A users profile.
    """
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=50, null=False, blank=False)
    last_name = models.CharField(_("last name"), max_length=50, null=False, blank=False)

    def __str__(self):
        """
        return object in readable form.
        """
        return f"{self.first_name} {self.last_name}"


class Request(models.Model):
    """
    a request a user can make for a reference.
    """


class Response(models.Model):
    """
    answers saved from the reference.
    """
    pass

# define TrustedUser with a foreign relation to profile.