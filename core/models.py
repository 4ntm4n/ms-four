from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

# the UserManager is created in a separate file and imported here
from core.managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(_("email adress"), max_length=254, unique=True)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=True)
    is_recruiter = models.BooleanField(_("recruiter"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("user")

    def __str__(self):
        """
        returns readable instance name.
        """
        return self.email


    def get_full_name(self):
        """
        returns the string 'first_name last_name' of user.
        """
        return f"{self.first_name} {self.last_name}"


    def get_short_name(self):
        """
        returns the users first_name
        """
        return self.first_name


    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        sends email to this user.
        """
        send_mail(subject,message,from_email, [self.email], **kwargs)
    