from django import forms
import re



class LoginForm(forms.Form):
    login_id=forms.CharField(label="User Name",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    login_passwd=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'style':'width:300px','class':'form-control'}))
