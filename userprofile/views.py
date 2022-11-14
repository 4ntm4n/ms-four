from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from userprofile.forms import SignUpForm


class HomeView(TemplateView):
    template_name = "userprofile/home.html"
    form_class = SignUpForm

class SignUpView(CreateView):
    template_name = "userprofile/signup.html"
    form_class = SignUpForm