from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomAuthenticationForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["username"].widget.attrs.update({"class":"form-control","maxlength":20,"placeholder":"Username"})
		self.fields["password"].widget.attrs.update({"class":"form-control","maxlength":30,"placeholder":"Password"})

class RegistrasiForm(forms.ModelForm):
	username = forms.CharField(label="Username", max_length=20, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Username"}))
	email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}))
	password1 = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))
	password2 = forms.CharField(label="Konfirm Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Konfirm Password"}))

	class Meta:
		model = User
		fields = ['username','email','password1','password2']