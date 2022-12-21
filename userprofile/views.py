from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404, request, response
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

from core.tokens import link
from userprofile.forms import ReferenceResponseForm, RequestForm, SignUpForm, PasswordChangeForm

from .models import *


# user related views

class HomeView(TemplateView):
    """
    Landing page view
    """
    template_name = "userprofile/home.html"


class SignUpView(FormView):
    """
    User sign up View
    """
    template_name = "userprofile/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("profile")

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
            return redirect("profile")

        return super(SignUpView, self).get(*args, **kwargs)


class UserLoginView(LoginView):
    """
    User Log in view
    """
    template_name = "userprofile/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("profile")


class UpdatePasswordView(PasswordChangeView):
    """
    View to update a users password redirect user to profile on success
    """
    form_class = PasswordChangeForm
    template_name = "userprofile/change_password.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "your password has been updated")
        return super(UpdatePasswordView, self).form_valid(form)


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    """
    This view is for deleting a pending ref_request object and 
    co-relating ref_response object.
    """
    model = User
    template_name = "userprofile/delete_account.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Your Account has been deleted. See Ya!")
        return super(DeleteAccountView, self).form_valid(form)

# end user related views

# object related views

class ProfileView(LoginRequiredMixin, ListView):
    """
    This view takes a users ref_request and ref_response data
    and gives a user access to it on a profile page.
    """
    model = Profile
    context_object_name = "profile"
    template_name = "userprofile/profile.html"

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
        context["comp_responses"] = context["profile"][0].refresponse_set.all(
        ).filter(ref_request__status="COMP")
        context["count_responses"] = context["comp_responses"].count()
        context["current_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return context

class CreateRequestView(LoginRequiredMixin, CreateView):
    """ 
    This view lets the user create a ref_request object.
    and sets the ref_request object to have a status of "pending"
    It also creates a ref_response object with some data from the 
    co-relating ref_request on it.
    """
    model = RefRequest
    template_name = "userprofile/send_request.html"
    form_class = RequestForm
    success_url = reverse_lazy("profile")

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs

    def form_valid(self, form):
        """
        If the create ref_request form is valid.
        Set the ref_request status to "pending"
        create a link based on the company name and ref_request id
        send the link in an email to the email provided in the form
        """
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

        email_subject = f"{user.profile} wants you as a reference"
        email_body = render_to_string("userprofile/emails/request_reference_email.html", {
            "date_from": form.instance.date_from,
            "date_to": form.instance.date_to,
            "company_name": form.instance.company_name,
            "name": user.profile,
            "domain": current_site.domain,
            "refid": link.encrypt_link(company_slug, response_id),
        })

        email = EmailMessage(
            email_subject,
            email_body,
            'hello@pytagora.com',
            [recipient],
            reply_to=['another@example.com'],
        )
        email.fail_silently = False
        email.send()
        return super(CreateRequestView, self).form_valid(form)


class DeleteRequestView(DeleteView):
    """
    This view is for deleting a pending ref_request object and 
    co-relating ref_response object.
    """
    model = RefRequest
    success_url = reverse_lazy("profile")

    def form_valid(self, form, **kwargs):

        ref_request = RefRequest.objects.get(pk=self.kwargs["pk"])
        messages.success(
            self.request, f"Reference request to {ref_request.to_email} at {ref_request.company_name} was successfully deleted.")
        return super(DeleteRequestView, self).form_valid(form)


class ResponseView(UpdateView):
    """
    This view is for the anonomous user. the reference that will update the 
    empty ref_response and complete it.
    This view also sets the co-relating ref_request to status "complete"
    """
    template_name = "userprofile/respond.html"
    success_url = reverse_lazy("home")
    form_class = ReferenceResponseForm

    def get_object(self, queryset=None):
        """
        1. decrypt reference ID
        2. Finds the specific reference object the user will respond to.
        3. render UpdateView for user response based on it's related request.

        """
        try:
            refid = link.decrypt_link(self.kwargs["token"])
            related_request = RefRequest.objects.get(pk=refid).refresponse.id
            reference_object = RefResponse.objects.get(pk=related_request)
        except ObjectDoesNotExist:
            raise Http404

        return reference_object

    def get(self, request, *args, **kwargs):
        """
            This method warns the updating user if the status of the ref_response is complete
            or if the ref_request object was deleted. (the user deleted the co-relating ref_request).
        """
        try:
            refid = link.decrypt_link(kwargs["token"])
            # Below I find the RefResponse ID through the request, issues when multiple users send requests
            related_request = RefRequest.objects.get(pk=refid)
            response_id = related_request.refresponse.id
            reference = RefResponse.objects.get(pk=response_id)
        except:
            messages.warning(
                request, "The person you were about to respond to has removed the reference request, thanks anyway!")
            return redirect("home")

        if reference.completed:
            messages.warning(
                request, "This reference request is already completed, thank you!")
            return redirect("home")

        return super(ResponseView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, set the co-relating 
        ref_request object status to "complete"
        Message the responder that the response has been saved. 
        """
        if form.instance.ref_request.status == "COMP":
            messages.warning(
                self.request, "This reference request is already completed, thank you!")
            return redirect("home")
        else:
            form.instance.ref_request.status = "COMP"
            form.instance.completed = True
            form.instance.ref_request.save()
            messages.success(
                self.request, "You did it! Thanks being a reference.")
            return super(ResponseView, self).form_valid(form)


class ReferenceDetailView(LoginRequiredMixin, DetailView):
    """
    This view is for viewing a specific reference in detail. 
    """
    model = RefResponse
    context_object_name = "response"
    template_name = "userprofile/response_detail.html"


class DeleteReferenceView(DeleteView):
    """
    This view is for deleting a ref_response and co-relating 
    ref_request object after it has been deleted.
    """
    model = RefResponse
    success_url = reverse_lazy("profile")

    def form_valid(self, form, **kwargs):

        reference = RefResponse.objects.get(pk=self.kwargs["pk"])
        messages.success(
            self.request, f"Reference from {reference.get_full_name()} at {reference.company_name} was deleted forever")
        return super(DeleteReferenceView, self).form_valid(form)
