from django.urls import path, include
from . import views

urlpatterns = [
	path('masuk/',views.masuk, name='masuk'),
	path('registrasi/',views.registrasi, name='registrasi'),
	path('keluar/',views.keluar, name='keluar'),

]