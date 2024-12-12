from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('done/', views.done_page, name='done_page'),
    path('my/', views.my_page, name='my_page'),

    # 이후는 REST API 임.
    path('api/create_board/', views.api_create_board, name='api_create_board'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
]
