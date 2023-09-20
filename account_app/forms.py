from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from account_app.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['phone']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['phone', 'full_name', 'image', "email", "password", "is_active", "is_admin"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput({'placeholder': 'email or phone'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput({'placeholder': 'password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if '@' not in username and len(username) != 11:
            raise ValidationError('username or password is wrong.')

        return username


class RegisterForm(forms.Form):
    phone = forms.CharField(max_length=11, widget=forms.TextInput({'placeholder': 'phone'}))


class CheckOtp(forms.Form):
    randcode = forms.CharField(max_length=5, widget=forms.TextInput({'placeholder': 'code'}))


class ContactUsForm(forms.Form):
    subject = forms.CharField(max_length=200, widget=forms.TextInput({'placeholder': 'subject'}))
    message = forms.CharField(widget=forms.Textarea({'placeholder': 'message'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput({'placeholder': 'email'}))
