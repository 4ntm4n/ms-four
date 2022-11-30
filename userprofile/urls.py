from django.urls import path

from userprofile.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/<int:pk>/", ProfileView.as_view(), name ="profile"),
    path("profile/<int:pk>/send-request", SendRequestView.as_view(), name ="send_request"),
]


