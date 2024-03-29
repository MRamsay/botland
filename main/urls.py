from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('blog/<str:location>', views.blog_post, name='blog_post'),
]