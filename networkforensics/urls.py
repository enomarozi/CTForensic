from django.urls import path
from . import views, views_pcap

urlpatterns = [
	path('',views.index, name='network_forensics'),
	path('getData/',views.getData, name='getData'),
	path('deleteData/<int:id_>/',views.deleteData, name='deleteData'),
	path('checkPacket/', views_pcap.checkPacket, name='checkPacket'),
	path('analisapcap/<int:id_>/',views_pcap.analisaPCAP, name='analisaPCAP'),
	path('analisapcapng/<int:id_>/',views_pcap.analisaPCAP, name='analisaPCAPNG'),
]