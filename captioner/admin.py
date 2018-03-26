from django.contrib import admin
from .models import Image, Caption, Rating, Vote

admin.site.register(Image)
admin.site.register(Caption)
admin.site.register(Vote)