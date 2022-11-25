from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from core.models import User

from .models import Profile, RefRequest, RefResponse


class SignUpForm(UserCreationForm):
    """
    form to create a new user
    """
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class RequestForm(ModelForm):
    class Meta:
        model = RefRequest
        fields = ["company_name", "date_to", "date_from", "to_email"]