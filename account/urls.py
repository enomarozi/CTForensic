from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
	path('masuk/',views.masuk, name='masuk'),
	path('registrasi/',views.registrasi, name='registrasi'),
	path('keluar/',views.keluar, name='keluar'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)