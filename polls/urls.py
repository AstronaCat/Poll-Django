from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('done/', views.done_page, name='done_page'),
    path('my/', views.my_page, name='my_page'),
    path('create_board/', views.create_board, name='create_board'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
]
