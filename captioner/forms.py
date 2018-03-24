from django import forms
from django.contrib.admin import widgets
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