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



BOSS = "BOSS"
COLLEAGUE = "COLL"
CONSULTANT = "CONS"
OTHER = "OTH"

class ReferenceResponseForm(ModelForm):
    """
    form to respond to users reference requests.
    """

    RELATION_CHOICES = [
        (BOSS, "Boss to referee"),
        (COLLEAGUE, "Colleague to referee"),
        (CONSULTANT, "referee was consultant"),
        (OTHER, "Other")
    ]

    relation = forms.MultipleChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=RELATION_CHOICES
    )

    class Meta:
        model = RefResponse
        fields = "__all__"
        exclude = ("ref_request", "profile", "email", "referee_first_name", "referee_last_name", "completed")

 