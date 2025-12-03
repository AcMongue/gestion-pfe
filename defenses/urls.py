from django.urls import path
from . import views

app_name = 'defenses'

urlpatterns = [
    path('', views.defense_list_view, name='list'),
    path('calendar/', views.defense_calendar_view, name='calendar'),
    path('<int:pk>/', views.defense_detail_view, name='detail'),
    path('create/<int:project_id>/', views.defense_create_view, name='create'),
    path('<int:defense_id>/add-jury/', views.jury_member_add_view, name='add_jury_member'),
    path('<int:defense_id>/evaluate/', views.evaluation_create_view, name='create_evaluation'),
]
