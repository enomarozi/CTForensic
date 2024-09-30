from django.urls import path
from . import views, views_jpg, views_png

urlpatterns = [
	path('',views.index, name='index'),
	path('cleanData/',views.cleanData, name='cleanData'),
	path('getData/',views.getData, name='getData'),
	path('deleteData/<int:id_>/',views.deleteData, name='deleteData'),
	path('analisajpg/<int:id_>/',views_jpg.analisaJPG, name='analisaJPG'),
	path('analisapng/<int:id_>/',views_png.analisaPNG, name='analisaPNG'),
]