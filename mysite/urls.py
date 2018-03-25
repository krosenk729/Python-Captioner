from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('captioner.urls')),
    # path('', RedirectView.as_view(url='/'))
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
