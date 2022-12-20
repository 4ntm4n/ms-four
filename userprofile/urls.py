from django.urls import path

from userprofile.views import *

urlpatterns = [

    path("", HomeView.as_view(), name="home"),
    path("profile/", ProfileView.as_view(), name="test_profile"),
    path("profile/change-password/", UpdatePasswordView.as_view(), name="change_password"),
    path("send-request/", CreateRequestView.as_view(), name="send_request"),
    path("profile/reference/<int:pk>", ReferenceDetailView.as_view(), name="reference_detail"),
    path("respond/<uidb64>/", ResponseView.as_view(), name="respond"),
    path("<int:pk>/delete-request/", DeleteRequestView.as_view(), name="delete_request"),
    path("<int:pk>/delete-reference/", DeleteReferenceView.as_view(), name="delete_reference"),

    # user account related templates
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/change-password/", UpdatePasswordView.as_view(), name="change_password"),
]   


