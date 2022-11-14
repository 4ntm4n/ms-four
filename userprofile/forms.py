from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User

class SignUpForm(UserCreationForm):
    """
    form to create a new user
    """
    class Meta:
        model = User
        fields = "__all__"

