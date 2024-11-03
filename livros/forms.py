from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        labels = {
            'username': "Nome de usuário",
            'first_name': "Primeiro nome",
            'last_name': "Último nome",
            'email': "Endereço de e-mail",
        }
