from django.contrib import admin
from rbac import models


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'menu', 'name', 'parent']
    list_editable = ['url', 'name', 'parent']


admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role)
admin.site.register(models.User)
admin.site.register(models.Menu)