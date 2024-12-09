from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),                    
    path('create_board/', views.create_board, name='create_board'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
]
