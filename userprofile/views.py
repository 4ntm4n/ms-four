from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from userprofile.forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm