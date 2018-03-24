from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Image(models.Model):
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created = models.DateField(auto_now_add=True)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('model-detail-view', args=[str(self.id)])

class Caption(models.Model):
	image = models.ForeignKey(Image, on_delete=models.CASCADE)
	text = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created = models.DateField(auto_now_add=True)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.text

class Rating(models.Model):
	image = models.ForeignKey(Image, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	value = models.PositiveSmallIntegerField(help_text="How non-glam is this photo? 10 = very normal, 0 = glamourous")
	def __str__(self):
		return self.value