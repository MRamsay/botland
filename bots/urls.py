from django.urls import path

from . import views

urlpatterns = [
    path('', views.dantebot, name='dantebot'),
]