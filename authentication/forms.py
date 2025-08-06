from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

CLASS_INPUT = "px-4 py-2 rounded-lg border border-purple-200 focus:outline-none focus:ring-1 focus:ring-purple-500 w-full"

class PswChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": CLASS_INPUT
            }) 

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  
     
    username = forms.CharField(widget=forms.TextInput(attrs={
        "id":"username",
        "placeholder":"Enter username...",
        "class":CLASS_INPUT
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "id":"email",
        "placeholder":"Email adress",
        "class":CLASS_INPUT
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"password1",
        "placeholder":"Password",
        "class":CLASS_INPUT
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"password2",
        "placeholder":"Confirm Password",
        "class":CLASS_INPUT
    }))

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password'] 
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        "id":"username",
        "placeholder":"Enter username...",
        "class":CLASS_INPUT
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"password",
        "placeholder":"password...",
        "class":CLASS_INPUT
    }))
