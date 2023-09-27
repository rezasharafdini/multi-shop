from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import forms

from .models import User,Otp,AddressUser, EmailForNewLetter, PrimaryUserProfile


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['phone', 'full_name', 'email', 'is_admin', 'show_image']
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["phone", "password"]}),
        ("Personal info", {"fields": ['email', 'full_name', 'image']}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "full_name", "image", "email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", 'phone']
    ordering = ["phone"]
    filter_horizontal = []



# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Otp)
admin.site.register(AddressUser)
admin.site.register(EmailForNewLetter)
admin.site.register(PrimaryUserProfile)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
