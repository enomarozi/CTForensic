from django.urls import path
from . import views, views_jpg, views_png, views_bmp, views_pcap, views_zip

urlpatterns = [
	path('',views.index, name='index'),
	path('cleanData/',views.cleanData, name='cleanData'),
	path('getData/',views.getData, name='getData'),
	path('checkPacket/', views_pcap.checkPacket, name='checkPacket'),
	path('deleteData/<int:id_>/',views.deleteData, name='deleteData'),
	path('analisajpg/<int:id_>/',views_jpg.analisaJPG, name='analisaJPG'),
	path('analisapng/<int:id_>/',views_png.analisaPNG, name='analisaPNG'),
	path('analisabmp/<int:id_>/',views_bmp.analisaBMP, name='analisaBMP'),
	path('analisapcap/<int:id_>/',views_pcap.analisaPCAP, name='analisaPCAP'),
	path('analisapcapng/<int:id_>/',views_pcap.analisaPCAP, name='analisaPCAPNG'),
	path('analisazip/<int:id_>/',views_zip.analisaZIP, name='analisaZIP'),
]