from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import request, response
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView)

from userprofile.forms import RequestForm, SignUpForm

from .models import *


class HomeView(TemplateView):
    template_name = "userprofile/home.html"

""" class ProfileView(View):
    
    form_class = RequestForm

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=kwargs["pk"])
        form = self.form_class
        return render(
            self.request, 
            "userprofile/profile.html", 
            {
                "profile": profile,
                "form": form,
            })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save() """

class UserLoginView(LoginView):
    template_name ="userprofile/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("test_profile")

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


class SignUpView(CreateView):
    template_name = "userprofile/signup.html"
    form_class = SignUpForm


""" testing different, probably better approach """


class TestProfileView(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = "profile"
    template_name="userprofile/test_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = context["profile"].filter(user=self.request.user)
        context["requests"] = context["profile"][0].refrequest_set.all()
        context["comp_responses"] = context["profile"][0].refresponse_set.all().filter(ref_request__status="COMP")
        return context
     

    """ def get_context_data(self, **kwargs):
        reference_requests = RefRequest
        reference_response = RefResponse
        context = super(TestProfileView, self).get_context_data(**kwargs)
        context.update({
            "requests": reference_requests.objects.filter(user=self.request.profile.user),
            "responses": reference_response.objects.order_by("time_added"),
        })
        return context """

class TestReferenceDetailView(LoginRequiredMixin, DetailView):
    model = RefResponse
    context_object_name = "ref_response"
    template_name ="userprofile/test_response_detail.html"


class TestCreateRequestView(LoginRequiredMixin, CreateView):
    model = RefRequest
    template_name = "userprofile/test_ref_request.html"
    fields = "__all__"
    success_url = reverse_lazy("test_profile")