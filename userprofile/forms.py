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
    class Meta:
        model = RefRequest
        fields = ["company_name", "date_to", "date_from", "to_email"]
       
       
        """ def clean(self):
            cleaned_data = super().clean()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            date_from = cleaned_data.get("date_from").date()
            date_to = cleaned_data.get("date_to").date()

            if date_from > date_to:
                raise ValidationError(
                "did you put a later from-date than end-date?"
                ) """
   


class ReferenceResponseForm(ModelForm):
    """
    form to respond to users reference requests.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        referee = self.instance.profile.first_name
        company = self.instance.company_name

        
        self.fields["title"].label = (
            _(f"what is your title at {company}")
        )
        self.fields["relation"].label = (
            _(f"What was your relation to {referee} at {company}")
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
            "first_name":_("Please enter your First name"),
            "last_name":_("Last name"),
            "title":_("What is your title/ role at {{company_name}}"),
        }

        help_texts = {
            'first_name': _('Some useful help text.'),
        }

    

    
 