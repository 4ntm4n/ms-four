from django.urls import path

from userprofile.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", TestProfileView.as_view(), name="test_profile"),
    path("send-request/", TestCreateRequestView.as_view(), name="send_request"),
    path("profile/reference/<int:pk>", TestReferenceDetailView.as_view(), name="reference_detail"),
    path("profile/<int:pk>/", ProfileView.as_view(), name ="profile"),
    
    # path("profile/<int:pk>/send-request", SendRequestView.as_view(), name ="send_request"),
]


