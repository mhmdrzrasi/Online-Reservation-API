from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import Group, UserAdmin as BaseUserAdmin

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'address', 'birthday', 'password1', 'password2')

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
    password = ReadOnlyPasswordHashField(help_text='you can change password <a href=../password/> this form </a>.')

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'address', 'birthday', 'password', 'last_login')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["id", "email", "phone_number", "is_admin"]
    list_filter = ["is_admin"]

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Personal info', {'fields': ('full_name', 'address', 'birthday')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')})
    )
    add_fieldsets = (
        (None, {'fields': ('full_name', 'email', 'phone_number', 'address', 'birthday', 'password1', 'password2')}),
    )

    search_fields = ('full_name', 'email')
    ordering = ('full_name',)
    filter_horizontal = []


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
