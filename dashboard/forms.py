from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Wybierz plik CSV')

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Potwierdź hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Nazwa użytkownika',
        }