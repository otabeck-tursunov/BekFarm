from django.contrib import admin
from django.urls import path
from mainApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DorilarView.as_view(), name='dorilar'),
    path('sotuvlar/', SotuvlarView.as_view(), name='sotuvlar'),
    # path('404/', NotFoundView.as_view(), name='404'),
]
