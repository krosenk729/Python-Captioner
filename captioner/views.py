from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Image, Caption, Rating, Vote
from .forms import ImageForm, CaptionForm


"""
_______________________________________________
Image Views
_______________________________________________
"""

def home (request):
	images = Image.objects.all()
	form = CaptionForm()
	images = build_images_out(images)
	return render(request, 'index.html', {'images': images, 'form': form})

def detail (request, image_id):
	try:
		images = Image.objects.get(id=image_id)
		images = build_images_out([images])
	except Image.DoesNotExist:
		raise Http404('Nopers - that link does not work')
	else:
		form = CaptionForm()
	return render(request, 'detail.html', {'image': images[0], 'form': form})

def user_images (request, username):
	user = User.objects.get(username=username)
	form = CaptionForm()
	images = build_images_out(Image.objects.filter(user=user))
	return render(request, 'index.html', {'display_type': 'images', 'images': images, 'form': form})

def user_captions (request, username):
	user = User.objects.get(username=username)
	form = CaptionForm()
	user_captions = Caption.objects.filter(user=user)
	images = []
	for i in user_captions:
		image = Image.objects.get(id=i.image.id)
		images.append(image)
	images = build_images_out(images)
	return render(request, 'index.html', {'display_type': 'captions', 'images': images, 'form': form})

def user_vote (request):
	caption = Caption.objects.get( id = request.POST.get('caption_id', None) )
	user = User.objects.get( id = request.POST.get('user_id', None) )
	value = request.POST.get('vote_val', None)
	vote, created = Vote.objects.get_or_create(caption=caption, user=user)
	vote.value = value
	vote.save()

	new_vote_avg = 0
	votes = Vote.objects.all().filter(caption=caption)
	votes_len = len(votes)
	for v in votes:
		new_vote_avg += v.value / votes_len
	return HttpResponse(new_vote_avg);

"""
_______________________________________________
Utility Functions
_______________________________________________
"""
def build_images_out (image_list):
	for i in image_list:
		i.captions = Caption.objects.all().filter(image=i.id)
		for c in i.captions:
			c.u_votes = []
			c.u_vote_avg = 0
			votes = Vote.objects.all().filter(caption=c.id)
			votes_len = len(votes)
			for v in votes:
				c.u_votes.append(v)
				c.u_vote_avg += v.value / votes_len
		# i.avg_rating = Rating.objects.all().filter(image = i.id)
	return image_list

"""
_______________________________________________
Post-Only Endpoints
_______________________________________________
"""

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

def add_caption (request, image_id):
	image = get_object_or_404(Image, pk = image_id)
	if request.method == 'POST':
		form = CaptionForm(request.POST)
		if form.is_valid():
			caption = form.save(commit=False)
			caption.image = image
			caption.user = request.user
			caption.save()
	return HttpResponseRedirect('/img/'+ str(image.id))


"""
_______________________________________________
User Auth Views 
_______________________________________________
"""

from .forms import LoginForm, RegisterForm
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
					return HttpResponseRedirect(reverse('Login'))
			else:
				print("The username and password were incorrect.")
				return HttpResponseRedirect(reverse('Login'))
	else: 
		form = LoginForm()
		return render(request, 'login.html', {'form': form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))

def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('Login'))
	else:
		form = RegisterForm()
		return render(request, 'register.html', {'form': form})