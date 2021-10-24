from django.urls import path

from . import views

urlpatterns = [
    path('inferno/', views.canto_index, name='inferno_index'),
    path('inferno/<int:canto>/', views.dantebot, name='inferno_canto'),
]