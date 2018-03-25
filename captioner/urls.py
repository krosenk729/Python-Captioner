from django.urls import path
from . import views

urlpatterns = [
	path('home', views.home, name = 'home'),
	path('add_image/', views.add_image, name='add_image'),
	path('img/<int:image_id>', views.detail, name = 'detail'),
	path('img/<int:image_id>/add_caption', views.add_caption, name='add_caption'),
	path('user/<slug:username>/images', views.user_images, name="user_images"),
	path('user/<slug:username>/captions', views.user_captions, name="user_captions"),
	path('login', views.login_view, name = 'Login'),
	path('logout', views.logout_view, name = 'Logout'),
	path('register', views.register_view, name = 'Register'),
]