from django.urls import path

from . import views

urlpatterns = [
    path('', views.canto_index, name='inferno_index'),
    path('<int:canto>/', views.dantebot, name='inferno_canto'),
]