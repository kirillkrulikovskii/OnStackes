from django import forms
from django.shortcuts import get_object_or_404
from .models import Accounts, Report

class LoginForm(forms.Form):
    username = forms.CharField(label='Username/Email', max_length=150)  # OR email
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        email = '@' in str(username) and username or None  # treat input as email if it contains @

        if username and password:
            # fetch the user without throwing Http404, so we can add a validation error
            user = None
            if email:
                try:
                    user = Accounts.objects.get(email=email)
                except Accounts.DoesNotExist:
                    pass
            else:
                try:
                    user = Accounts.objects.get(username=username)
                except Accounts.DoesNotExist:
                    pass

            if not user or not user.check_password(password):
                # either no such account or password mismatch
                raise forms.ValidationError("Invalid username/email and password combination.")
        return cleaned_data

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    continue_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username          = cleaned_data.get('username')
        email             = cleaned_data.get('email')
        password          = cleaned_data.get('password')
        continue_password = cleaned_data.get('continue_password')

        if Accounts.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")

        if Accounts.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.") # Fixed typo: "registed" to "registered"

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