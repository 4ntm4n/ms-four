from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import request, response
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView, View)

from core.tokens import link
from userprofile.forms import ReferenceResponseForm, RequestForm, SignUpForm

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

from datetime import datetime


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
        context["count_requests"] = context["requests"].count()
        print(context["requests"].count())
        context["comp_responses"] = context["profile"][0].refresponse_set.all(
        ).filter(ref_request__status="COMP")
        context["count_responses"] = context["comp_responses"].count()
        context["current_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return context
     

class TestReferenceDetailView(LoginRequiredMixin, DetailView):
    model = RefResponse
    context_object_name = "ref_response"
    template_name ="userprofile/test_response_detail.html"



class TestCreateRequestView(LoginRequiredMixin, CreateView):
    model = RefRequest
    template_name = "userprofile/send_request.html"
    fields = ["company_name", "date_from", "date_to", "to_email"]
    success_url = reverse_lazy("test_profile")

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.instance.status = "PEND"
        user = self.request.user
        # get the ref_request id before it is sent. 
        ref_request = form.save(commit=False)
        form.save()
        response_id = ref_request

        current_site = get_current_site(self.request)

        recipient = form.instance.to_email
        company_slug = form.instance.company_slug
        email_body = render_to_string("userprofile/emails/request_reference_email.html", {
            "name":user.profile,
            "domain":current_site.domain,
            "refid": link.encrypt_link(company_slug, response_id),
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

        print("this form was sent to profile: ", user.profile)
        return super(TestCreateRequestView, self).form_valid(form)


from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class TestResponseView(UpdateView):
    template_name = "userprofile/test_respond.html"
    success_url = reverse_lazy("home")
    form_class = ReferenceResponseForm

    def get_object(self): 
        """
        1. decrypt reference ID
        2. Finds the specific reference object the user will respond to.
        3. render UpdateView for user response based on it's related request.
        
        """
        refid = link.decrypt_link(self.kwargs["uidb64"])
       
        related_request = RefRequest.objects.get(pk=refid).refresponse.id
        reference_object = RefResponse.objects.get(pk=related_request)

        return reference_object

    def get(self, request, *args, **kwargs):

        refid = link.decrypt_link(kwargs["uidb64"])
        # Below I find the RefResponse ID through the request, issues when multiple users send requests
        related_request = RefRequest.objects.get(pk=refid)
        response_id = related_request.refresponse.id 
        reference = RefResponse.objects.get(pk=response_id)

        if reference.completed:
            messages.warning(request, "This reference request is already completed, thank you!")
            return redirect ("home")
        
        return super(TestResponseView, self).get(request, *args, **kwargs)
    
    def form_valid(self, form):
        request_status = form.instance.ref_request.status
        form.instance.ref_request.status = "COMP"
        form.instance.completed = True
        print(form.instance.completed)
        form.instance.ref_request.save()     
        messages.success(self.request, "You did it! Thanks for being awesome.")
        return super(TestResponseView, self).form_valid(form)