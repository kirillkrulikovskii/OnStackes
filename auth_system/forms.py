from django import forms
from django.shortcuts import get_object_or_404
from .models import Accounts, Report

class LoginForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = Accounts.objects.get(email=email)
                if not user.check_password(password):
                    raise forms.ValidationError("Incorrect password.")
            except Accounts.DoesNotExist:
                raise forms.ValidationError("User with this email does not exist.")
        return cleaned_data

    class Meta:
        model = Accounts
        fields = ['email', 'password']

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    continue_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        continue_password = cleaned_data.get('continue_password')

        if password and continue_password and password != continue_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
    class Meta:
        model = Accounts
        fields = ['username', 'email', 'password', 'continue_password']

"""
class ReportForm(forms.ModelForm):
    reported_user = forms.ModelChoiceField(queryset=Accounts.objects.all(), label='Reported User')
    reason = forms.CharField(label='Reason', widget=forms.Textarea)

    class Meta:
        model = Report
        fields = ['reported_user', 'reason']

class MessageForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=Accounts.objects.all(), label='Recipient')
    message = forms.CharField(label='Message', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['recipient'].queryset = Accounts.objects.exclude(id=user.id)
    
    class Meta:
        model = Accounts
        fields = ['recipient', 'message']
""" # Keep code 

class ProfileEditedForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['username', 'email', 'display_name',
                  'bio', 'status', 'timestamp_status',
                  'num_phone', 'avatar', 'date_birth', 
                  'gender', 'following', 'timeout']