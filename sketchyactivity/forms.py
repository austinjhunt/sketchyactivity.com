from django import forms

class SignUpForm(forms.Form):
    first_name = forms.CharField(label="",max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label="",max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.CharField(label="",max_length=100, required=True,widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="",max_length=100, required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    phone = forms.CharField(label="",max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder': 'Phone (Not required)'}))

class LoginForm(forms.Form):
    email = forms.CharField(label="", max_length=100, required=True,
                            widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="", max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
