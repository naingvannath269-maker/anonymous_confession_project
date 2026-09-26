from django.urls import path
from . import views

urlpatterns = [
    path('', views.wall_view, name='wall'),
    path('upvote/<int:pk>/', views.upvote_confession, name='upvote'),
]