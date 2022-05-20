from django.contrib import admin

# Register your models here.
from .models import Terrorist, Passport

admin.site.register(Terrorist)
admin.site.register(Passport)