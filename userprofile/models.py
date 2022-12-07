from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext as _
# 3rd party dependencies
from partial_date import PartialDateField

from core.models import User  # imported user override


class Profile(models.Model):
    """                                                          
    A users profile.
    """
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=50, null=False, blank=False)
    last_name = models.CharField(_("last name"), max_length=50, null=False, blank=False)

    def __str__(self):
        """
        return object in readable form.
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(
                user=instance,
                first_name = instance.first_name,
                last_name = instance.last_name,
            )
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class RefRequest(models.Model):
    """
    a request a user can make for a reference.
    """
    profile = models.ForeignKey(Profile, verbose_name=_("profile"), on_delete=models.CASCADE)
    company_name = models.CharField(_("company name"), max_length=100, null=True, blank=True)
    company_slug = models.SlugField(_("company_slug"), null=True, blank=True, unique=False, max_length=150)
    date_from = PartialDateField( verbose_name=_("date from"))
    date_to = PartialDateField(verbose_name=_("date to"))
    to_email = models.EmailField(_("to email"), max_length=254, null=True, blank=True)
    

    UNINITIATED = "UNIN"
    PENDING = "PEND"
    COMPLETE = "COMP"

    STATUS_CHOICES = [
        (UNINITIATED, "Uninitiated"),
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
    ]
    status = models.CharField(_("status"), max_length=4, choices=STATUS_CHOICES, default=UNINITIATED,)
    time_sent = models.DateTimeField(_("time_sent"), auto_now_add=True, null=True)


    def save(self, *args, **kwargs):
        slug = self.company_name[0:100]
        self.company_slug = slugify(slug, allow_unicode=False)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Reference request"
        verbose_name_plural = "Reference requests"




class RefResponse(models.Model):
    """
    answers saved from the reference.
    """
    # response relations to user profile
    ref_request = models.OneToOneField(RefRequest, verbose_name=_("request to"), on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name=_("profile"), on_delete=models.CASCADE, null=True, blank=True)

    # info about reference
    first_name = models.CharField(_("first name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, null=True, blank=True)
    company_name = models.CharField(_("company name"), max_length=50, null=True, blank=True)
    title = models.CharField(_("title"), max_length=50)

    BOSS = "BOSS"
    COLLEAGUE = "COLL"
    CONSULTANT = "CONS"
    OTHER = "OTH"

    RELATION_CHOICES = [
        (BOSS, "Boss to referee"),
        (COLLEAGUE, "Colleague to referee"),
        (CONSULTANT, "referee was consultant"),
        (OTHER, "Other")
    ]

    relation = models.CharField(_("relation to referee"), choices=RELATION_CHOICES, default=BOSS, max_length=4)
    other_relation = models.CharField(_("if Other, please specify"), max_length=80, null=True, blank=True)

    #reference output about referee
    main_tasks = models.TextField(_("describe main tasks"))
    elaborate = models.TextField(_("elaborate"))
    extra = models.TextField(_("extra"))

    email = models.EmailField(_("your email"), max_length=254)

    # info about user who sent request.
    referee_first_name = models.CharField(_("referee first name"), max_length=50)
    referee_last_name = models.CharField(_("referee last name"), max_length=50)
    

    completed = models.BooleanField(_("is completed"), default=False)
    time_added = models.DateTimeField(_("time added"), auto_now=True)

    

    def get_profile(self):
        """
        returns profile related to response
        """
        return self.ref_request.profile

    
    def get_full_name(self):
        """
        returns reference's full name
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        returns context string for which the response is made from and to.
        """
        return f"From: {self.company_name} To: {self.get_profile()}"


    class Meta:
        verbose_name = "Reference response"
        verbose_name_plural = "Reference responses"
        ordering = ["ref_request"]


    @receiver(post_save, sender=RefRequest)
    def create_ref_response(sender, instance, created, **kwargs):
        if created:
            RefResponse.objects.create(
                ref_request=instance,
                profile = instance.profile,
                email = instance.to_email,
                company_name = instance.company_name,
                referee_first_name = instance.profile.first_name,
                referee_last_name = instance.profile.last_name,
            )
            instance.save()
    
    

# define TrustedUser with a foreign relation to profile.