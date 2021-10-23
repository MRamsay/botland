from django.urls import path

from . import views

urlpatterns = [
    path('dantebot/', views.canto_index, name='index'),
    path('dantebot/<int:canto>/', views.dantebot, name='dantebot'),
]