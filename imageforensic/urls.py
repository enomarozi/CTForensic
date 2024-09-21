from django.urls import path, include

urlpatterns = [
    path('', include('index.urls')),
    path('account/', include('account.urls')),
]
