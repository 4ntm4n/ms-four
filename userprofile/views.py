from django.http import request, response
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView
from django.views.generic.detail import DetailView

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


class ProfileView(ListView):
    model = RefRequest
    form_class = RequestForm

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=kwargs["pk"])
        form = self.form_class
        requests = profile.refrequest_set.filter(status="PEND")
        return render(
            self.request, 
            "userprofile/profile.html", 
            {
                "profile": profile,
                "form": form,
                "requests": requests,
            })




class SignUpView(CreateView):
    template_name = "userprofile/signup.html"
    form_class = SignUpForm



