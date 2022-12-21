from django.urls import path

from userprofile.views import *

urlpatterns = [
    # home and profile view
    path("", HomeView.as_view(), name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    
    # creates a reqest and a semi-empty response object through django signals CRUD -create
    path("send-request/", CreateRequestView.as_view(), name="send_request"),
    
    # lets anonymous user update the response object related to the user request CRUD -update
    path("respond/<token>/", ResponseView.as_view(), name="respond"),

    # ability to delete a pending request
    path("<int:pk>/delete-request/", DeleteRequestView.as_view(), name="delete_request"),

    # Detail view for reference where user also can delete CRUD -read and CRUD -delete
    path("profile/reference/<int:pk>", ReferenceDetailView.as_view(), name="reference_detail"),
    path("<int:pk>/delete-reference/", DeleteReferenceView.as_view(), name="delete_reference"),

    # user account related templates
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/change-password/", UpdatePasswordView.as_view(), name="change_password"),
    path("profile/<int:pk>/delete-account/", DeleteAccountView.as_view(), name="delete_account"),

]   

