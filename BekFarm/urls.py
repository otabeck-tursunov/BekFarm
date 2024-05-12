from django.contrib import admin
from django.urls import path
from mainApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('dorilar/', DorilarView.as_view(), name='dorilar'),
    path('top-dorilar/', TopDorilarView.as_view(), name='top-dorilar'),
    path('dorilar/<int:id>/tasdiqlash/', DoriConfirmDeleteView.as_view()),
    path('dorilar/<int:id>/o\'chirish/', DoriDeleteView.as_view()),
    path('tavsiya/', TavsiyaView.as_view(), name='tavsiya'),
    path('sotuvlar/', SotuvlarView.as_view(), name='sotuvlar'),
]
