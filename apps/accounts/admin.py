from django.contrib import admin
from .models import AccountUser


class AccountUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(AccountUser, AccountUserAdmin)
