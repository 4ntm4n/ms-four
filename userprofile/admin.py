from django.contrib import admin

from .models import Profile, RefRequest, RefResponse

# Register your models here.
admin.site.register(Profile)
admin.site.register(RefRequest)
admin.site.register(RefResponse)