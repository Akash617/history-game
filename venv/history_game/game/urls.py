from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
    path('won_game/', views.won_game, name='won_game'),
    path('lost_game/', views.lost_game, name='lost_game'),
]
