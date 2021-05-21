from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('team/', views.team, name="team"),
    path('result/', views.result, name="result")
]
