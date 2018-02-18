from django import forms

from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.PasswordInput()

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user or not user.is_active():
            return forms.ValidationError("Пользователя с таким логином/паролем в системе нет.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        return user
