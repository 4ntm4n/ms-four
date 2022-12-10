from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

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
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = RefRequest
        fields = [ "company_name", "date_to", "date_from", "to_email"]


    def clean(self):
        cleaned_data = self.cleaned_data
        user = self.request.user
        to_email = cleaned_data.get("to_email")
        print(user.email)

        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
      
        if date_to is not None and date_from > date_to:
            msg1 = "you need an earlier date here"
            msg2 = "than here, if you want to send a request"

            self._errors["date_from"] = self.error_class([msg1])
            self._errors["date_to"] = self.error_class([msg2])

            del cleaned_data["date_from"]
            del cleaned_data["date_to"]
        
        if to_email == user.email:
            msg = "you cant request a reference from yourself."
            self._errors["to_email"] = self.error_class([msg])

        return cleaned_data
        
    

class ReferenceResponseForm(ModelForm):
    """
    form to respond to users reference requests.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        referee = self.instance.profile.first_name
        company = self.instance.company_name
        
        self.fields["title"].label = (
            _(f"Title / Role at {company}")
        )

        self.fields["company_name"].help_text = (
            _(f"Provided by {referee}")
        )

        self.fields["relation"].label = (
            _(f"work relation to {referee}")
        )
        
        self.fields["main_tasks"].label = (
            _(f"How would you describe {referee}'s role or main tasks at {company}")
        )

        self.fields["elaborate"].label = (
            _(f"Given the role you just provided, " 
            + f"how would describe {referee}'s performance? Please motivate")
        )

        self.fields["extra"].label = (
            _(f"Is there anything else you would like " 
            + f"to add that might help {referee} in the future?")
        )
        
        #self.fields['other_relation'].widget.attrs.update({"class": "hide"})
   
    class Meta:
        model = RefResponse
        fields = "__all__"
        exclude = ("ref_request", "profile", "email", "referee_first_name", "referee_last_name", "completed")

        labels = {
            "first_name":_("First Name"),
            "last_name":_("Last name"),
        }

       

    

    
 