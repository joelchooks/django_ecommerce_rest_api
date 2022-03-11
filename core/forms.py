from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email address already registered.')
       

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user
