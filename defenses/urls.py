from django.urls import path
from . import views

app_name = 'defenses'

urlpatterns = [
    path('', views.defense_list_view, name='list'),
    path('', views.defense_list_view, name='defense_list'),  # Alias
    path('calendar/', views.defense_calendar_view, name='calendar'),
    path('planning/', views.defense_planning_view, name='planning'),
    path('planning/', views.defense_planning_view, name='defense_planning'),  # Alias
    path('room-schedule/', views.room_schedule_view, name='room_schedule'),
    path('rooms/', views.room_list_view, name='room_list'),
    path('rooms/create/', views.room_create_view, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_edit_view, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete_view, name='room_delete'),
    path('<int:pk>/', views.defense_detail_view, name='detail'),
    path('create/<int:project_id>/', views.defense_create_view, name='create'),
    path('<int:pk>/update/', views.defense_update_view, name='update'),
    path('<int:defense_id>/add-jury/', views.jury_member_add_view, name='add_jury_member'),
    path('<int:defense_id>/evaluate/', views.evaluation_create_view, name='create_evaluation'),
    path('<int:defense_id>/request-change/', views.defense_change_request_create_view, name='request_change'),
    path('change-requests/<int:pk>/review/', views.defense_change_request_review_view, name='review_change_request'),
    path('<int:pk>/grade/', views.grade_defense_view, name='grade_defense'),
]
