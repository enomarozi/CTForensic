from django.urls import path
from . import views

urlpatterns = [
	path('',views.index, name='index'),
	path('settingData/<str:action>/<int:nilai>',views.settingData, name='settingData'),
	path('cleanData/',views.cleanData, name='cleanData'),
	path('getData/',views.getData, name='getData'),
	path('analisaData/<int:id_>/',views.analisaData, name='analisaData')
]