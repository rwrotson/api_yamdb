from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'username', 'bio',
                  'email', 'role')
    #empty_value_display = 'empty'

admin.site.register(CustomUser, UserAdmin)
