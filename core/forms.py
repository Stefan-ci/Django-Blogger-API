from django import forms
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-sm",
                "placeholder": "john@doe.org",
                "autocomplete": "email"
            }
        )
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-sm",
            }
        )
    )



class CreateUserForm(forms.ModelForm):
    username = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm",
                # "pattern": "^[a-zA-Z0-9]{4,}$",
            }
        )
    )
    
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(
            attrs={ 
                "class": "form-control form-control-sm",
            }
        )
    )
    
    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-sm",
                # "pattern": "^(?=.*[a-z])(?=.*[A-Z]).{8,}$",
            }
        )
    )
    
    password2 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-sm",
                # "pattern": "^(?=.*[a-z])(?=.*[A-Z]).{8,}$",
            }
        )
    )
    
    
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        if cleaned_data["password"] != cleaned_data["password2"]:
            raise forms.ValidationError(_("Les deux mots de passe ne concordent pas!"))
    
    def save(self, *args, **kwargs) -> User:
        cleaned_data = super(CreateUserForm, self).clean()
        user = User.objects.create_superuser(
            email=cleaned_data["email"],
            username=cleaned_data["username"],
            password=cleaned_data["password"]
        )
        return user
