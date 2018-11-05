from django.contrib import admin
from crm import models

# Register your models here.

admin.site.register((models.UserProfile, models.Customer, models.ClassList, models.Campuses))
