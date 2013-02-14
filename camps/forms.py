from django import forms
from myproject.camps.models import *
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from django.contrib.auth.models import User
import datetime
import re


class UserForm(forms.ModelForm):
    password2 = forms.CharField(max_length=20, required=True, widget=forms.widgets.PasswordInput())
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {
            'password': forms.widgets.PasswordInput()
        }

    def clean(self):
        super(UserForm, self).clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if not re.search(r'^[\w\.@-_]+$', username):
            raise forms.ValidationError('Username is invalid. Only use letters, numbers or these symbols: @ - _')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('User with that e-mail address already exists.')
        if password != password2:
            raise forms.ValidationError('Passwords do not match.')
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class OrganizationForm(forms.ModelForm):
    phone = USPhoneNumberField()
    zip_code = USZipCodeField()

    class Meta:
        model = Organization
        exclude = ['user']
        widgets = {
            'organization': forms.widgets.TextInput(attrs={'class': 'span6'}),
            'address': forms.widgets.TextInput(attrs={'class': 'span6'}),
        }


class CampForm(forms.ModelForm):
    class Meta:
        model = Camp
        exclude = ['organization', 'last_updated']
        widgets = {
            'camp_name': forms.widgets.TextInput(attrs={'class': 'span8'}),
            'info': forms.widgets.Textarea(attrs={'rows': 4, 'class': 'span8'}),
            'address': forms.widgets.TextInput(attrs={'class': 'span6'}),
            'cost': forms.widgets.TextInput(attrs={'class': 'span6'}),
            'min_age': forms.widgets.TextInput(attrs={'class': 'span2'}),
            'max_age': forms.widgets.TextInput(attrs={'class': 'span2'}),
            'vacancies': forms.widgets.TextInput(attrs={'class': 'span2'}),
            'start_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}, format='%m/%d/%Y'),
            'end_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}, format='%m/%d/%Y'),
            'venue': forms.widgets.TextInput(attrs={'class': 'span6'}),
            'times': forms.widgets.TextInput(attrs={'class': 'span6'}),
        }

    def clean(self):
        super(CampForm, self).clean()
        min_age = self.cleaned_data.get('min_age')
        max_age = self.cleaned_data.get('max_age')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if min_age > max_age:
            raise forms.ValidationError("Min. age can't be higher than max age.")
        if start_date > end_date:
            raise forms.ValidationError("End date can't be before start date.")
        if start_date < datetime.date.today():
            raise forms.ValidationError("Camp cannot begin in the past.")
        return self.cleaned_data


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=20, required=True, widget=forms.widgets.PasswordInput())
    password2 = forms.CharField(max_length=20, required=True, widget=forms.widgets.PasswordInput())

    def clean(self):
        super(ChangePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords do not match.')
        return self.cleaned_data
