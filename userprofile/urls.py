from django.contrib import admin
from django.urls import path
from userprofile.views import HomeView, SignUpView
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),

]
