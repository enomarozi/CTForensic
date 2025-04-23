from django.urls import path
from . import views

urlpatterns = [
	path('',views.index, name='memory_forensics'),
]