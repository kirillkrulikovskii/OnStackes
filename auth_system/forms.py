from django import forms
from .models import Accounts

class AccountsForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self): # Check if create is valid
        username = self.cleaned_data.get('username')
        if Accounts.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
    def clean_password(self): # Check if password is valid
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = Accounts.objects.get(username=username)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid username and password.")
            except Accounts.DoesNotExist:
                raise forms.ValidationError("Invalid username and password.")
    
    def login(self):
        username: str = self.cleaned_data.get('username')
        password: str = self.cleaned_data.get('password')
        try:
            user = Accounts.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                raise forms.ValidationError("Invalid username and password.")
        except Accounts.DoesNotExist:
            raise forms.ValidationError("Invalid username and password.")
    def signup(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password') 
        user = Accounts.objects.create_user(username=username, password=password)
        return user

    class Meta:
        model = Accounts
        fields = ['username', 'password']

class AccountsEditedForm(forms.ModelForm):
    
    class Meta:
        model = Accounts
        fields = ['bio', 'status', 'email', 'num_phone', 'avatar', 'date_birth', 'gender']

class AccountsPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if len(new_password) < 8:
            raise forms.ValidationError("New password must be at least 8 characters long.")
        return new_password

    def save(self, commit=True):
        new_password = self.cleaned_data.get('new_password')
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user
