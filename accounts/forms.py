from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
        }

class PasswordChangeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # accept user
        super().__init__(*args, **kwargs)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        required=True,
        help_text="Enter your new password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        required=True,
        help_text="Confirm your new password"
    )

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        pwd_conf = cleaned_data.get("password_confirm")
        if pwd and pwd_conf and pwd != pwd_conf:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        if self.user:
            self.user.set_password(self.cleaned_data['password'])
            if commit:
                self.user.save()
        return self.user
