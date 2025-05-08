from django.urls import path
from .views import home, upload_csv, dashboard, register

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_csv, name='upload_csv'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'), 
]
