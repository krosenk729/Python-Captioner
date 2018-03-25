from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image, Caption, Rating

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ['name', 'url']

class CaptionForm(forms.ModelForm):
	class Meta:
		model = Caption
		fields = ['text']

# class ImageForm(forms.Form):
# 	name = forms.CharField(label='Name', max_length=100)
# 	url = forms.CharField(label='Image location', max_length=255)

# class CaptionForm(forms.Form):
# 	text = forms.CharField()

class RatingForm(forms.Form):
	value = forms.IntegerField(min_value=0, max_value=10)

class LoginForm(forms.Form):
	username = forms.CharField(label='User Name', max_length=64)
	password = forms.CharField(widget=forms.PasswordInput())

# class UserCreationForm(forms.Form):
# 	username = forms.CharField(label='User Name', max_length=64)
# 	email = forms.CharField(label='Email Address', widget=forms.EmailField())
# 	password = forms.CharField(widget=forms.PasswordInput())
# 	passwordconfirm = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(UserCreationForm):
	email = forms.EmailField(label='Email Address', required=True)
	first_name = forms.CharField(label='First Name')
	last_name = forms.CharField(label='Last Name')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		for fieldname in ['username', 'email', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user