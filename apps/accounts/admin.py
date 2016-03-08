from django.contrib import admin
from .models import AccountUser


class AccountUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_activated", "is_staff")

admin.site.register(AccountUser, AccountUserAdmin)
