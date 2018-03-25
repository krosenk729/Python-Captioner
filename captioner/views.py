from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Image, Caption, Rating
from .forms import ImageForm, CaptionForm


"""
_______________________________________________
Image Views
_______________________________________________
"""

def home (request):
	images = Image.objects.all()
	for i in images:
		i.captions = Caption.objects.all().filter(image=i.id)
		# i.avg_rating = Rating.objects.all().filter(image = i.id)
	return render(request, 'home.html', {'images': images})

def add_image (request):
	if request.method == 'POST':
		form = ImageForm(request.POST)
		if form.is_valid():
			image = form.save(commit=False)
			image.user = request.user
			image.save()
		return HttpResponseRedirect(reverse('detail', args=[image.id]))
	else:
		form = ImageForm()
	return render(request, 'add.html', {'form': form})

def detail (request, image_id):
	try:
		image = Image.objects.get(id=image_id)
	except Image.DoesNotExist:
		raise Http404('Nopers - that link does not work')
	else:
		captions = Caption.objects.all().filter(image=image_id)
		form = CaptionForm()
		# i.avg_rating = Rating.objects.all().filter(image = i.id)
	return render(request, 'detail.html', {'image': image, 'captions': captions, 'form': form})

def add_caption (request, image_id):
	image = get_object_or_404(Image, pk = image_id)
	if request.method == 'POST':
		form = CaptionForm(request.POST)
		if form.is_valid():
			caption = form.save(commit=False)
			caption.image = image
			caption.user = request.user
			caption.save()
	return HttpResponseRedirect('/captioner/img/'+ str(image.id))

def user_images (request, username):
	user = User.objects.get(username=username)
	form = CaptionForm()
	images = Image.objects.filter(user=user)
	for i in images:
		i.captions = Caption.objects.all().filter(image=i.id)
	return render(request, 'user.html', {'user': user, 'display_type': 'images', 'images': images, 'form': form})

def user_captions (request, username):
	user = User.objects.get(username=username)
	form = CaptionForm()
	user_captions = Caption.objects.filter(user=user)
	images = []
	for i in user_captions:
		image = Image.objects.filter(id=i.image)
		image.captions = Caption.objects.filter(image=image.id)
		images.append(image)
	return render(request, 'user.html', {'user': user, 'display_type': 'captions', 'images': images, 'form': form})


"""
_______________________________________________
User Auth Views 
_______________________________________________
"""

from .forms import LoginForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			u = form.cleaned_data['username']
			p = form.cleaned_data['password']
			user = authenticate(username = u, password = p)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('home'))
				else:
					print("The account has been disabled!")
			else:
				print("The username and password were incorrect.")
	else: 
		form = LoginForm()
		return render(request, 'login.html', {'form': form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/home')

def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('Login'))
	else:
		form = UserCreationForm()
		return render(request, 'register.html', {'form': form})