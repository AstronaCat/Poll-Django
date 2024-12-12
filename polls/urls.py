from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('done/', views.done_page, name='done_page'),
    path('my/', views.my_page, name='my_page'),
    path('board/modify/<int:id>/', views.board_modify, name='board_modify'),
    path('board/vote/<int:id>/', views.board_vote, name='board_vote'),

    # 이후는 REST API 임.
    path('api/create_board/', views.api_create_board, name='api_create_board'),
    path('api/modify_board/', views.api_modify_board, name='api_modify_board'),
    path('api/create_question/', views.api_create_question, name='api_create_question'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
]
