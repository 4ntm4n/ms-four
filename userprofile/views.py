from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import request, response
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView, View)

from core.tokens import account_activation_token
from userprofile.forms import RequestForm, SignUpForm

from .models import *


class HomeView(TemplateView):
    template_name = "userprofile/home.html"


class ProfileView(ListView):
    model = RefRequest

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=kwargs["pk"])
        requests = profile.refrequest_set.all()
        return render(
            self.request, 
            "userprofile/profile.html", 
            {
                "profile": profile,
                "requests": requests,
            })


""" testing different, probably better approach """

class SignUpView(FormView):
    template_name = "userprofile/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("test_profile")

    def form_valid(self, form):
        """
        Method that adds feature of logging in user, once user created.
        """
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUpView, self).form_valid(form)


    def get(self, *args, **kwargs):
        """
        Redirects user to its profile if user is already logged in.
        """
        if self.request.user.is_authenticated:
            return redirect("test_profile")

        return super(SignUpView, self).get(*args, **kwargs)


class UserLoginView(LoginView):
    template_name ="userprofile/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("test_profile")


class TestProfileView(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = "profile"
    template_name="userprofile/test_profile.html"

    def get_context_data(self, **kwargs):
        """ 
        Gets context data for profile view:
        1. filter out context to logged in user using profile model.
        2. get reference requests related to that profile.
        3. get reference response from related profile and
        filter them out based on completed requests.
        """
        context = super().get_context_data(**kwargs)
        context["profile"] = context["profile"].filter(user=self.request.user)
        context["requests"] = context["profile"][0].refrequest_set.all()
        context["comp_responses"] = context["profile"][0].refresponse_set.all(
        ).filter(ref_request__status="COMP")
        return context
     

class TestReferenceDetailView(LoginRequiredMixin, DetailView):
    model = RefResponse
    context_object_name = "ref_response"
    template_name ="userprofile/test_response_detail.html"


class TestCreateRequestView(LoginRequiredMixin, CreateView):
    model = RefRequest
    template_name = "userprofile/test_ref_request.html"
    fields = ["company_name", "date_from", "date_to", "to_email"]
    success_url = reverse_lazy("test_profile")

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.instance.status = "PEND"
        user = self.request.user
        # get the ref_request id before it is sent. 
        ref_request = form.save(commit=False)
        form.save()
        response_id = form.instance.refresponse.id

        current_site = get_current_site(self.request)

        recipient = form.instance.to_email
        
        email_body = render_to_string("userprofile/emails/request_reference_email.html", {
            "name":user.profile,
            "domain":current_site.domain,
            "refid": response_id, #urlsafe_base64_encode(force_bytes(ref_request_id))
            "token": account_activation_token.make_token(form.instance.refresponse),
            })

        email = EmailMessage(
            'email subject',
            email_body,
            'hello@pytagora.com',
            [recipient],
            reply_to=['another@example.com'],
)       
        email.fail_silently=False
        email.send()

        print("this form was sent to profile: ", self.request.user.profile)
        return super(TestCreateRequestView, self).form_valid(form)


from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode




class TestResponseView(UpdateView):
    model = RefResponse
    template_name = "userprofile/test_respond.html"
    fields = "__all__"
    success_url = reverse_lazy("home")
