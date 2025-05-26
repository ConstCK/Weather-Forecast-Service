from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
        )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
