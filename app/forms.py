from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User
from django import forms
from app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("Ten email jest już zajęty.")
        return email

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('gender','phone_number','birth_date')
