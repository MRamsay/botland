from django.urls import path

from . import views

urlpatterns = [
    path('divine', views.canto_index, name='inferno_index'),
    path('divine/<int:canto>/', views.dantebot, name='inferno_canto'),
    path('midwit-jwst', views.jwst_index, name='jwst_index'),
]