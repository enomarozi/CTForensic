from django.urls import path
from . import views_jpg, views_png

urlpatterns = [
	path('',views_jpg.index, name='index'),
	path('cleanData/',views_jpg.cleanData, name='cleanData'),
	path('getData/',views_jpg.getData, name='getData'),
	path('analisajpg/<int:id_>/',views_jpg.analisaJPG, name='analisaJPG'),
	path('analisapng/<int:id_>/',views_png.analisaPNG, name='analisaPNG'),
	path('deleteData/<int:id_>/',views_jpg.deleteData, name='deleteData'),
]