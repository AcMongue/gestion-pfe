from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list_view, name='list'),
    path('', views.project_list_view, name='project_list'),  # Alias
    path('create/', views.project_create_view, name='create'),
    path('create/', views.project_create_view, name='project_create'),  # Alias
    path('my-projects/', views.my_projects_view, name='my_projects'),
    
    # Nouvelles vues pour l'encadreur
    path('supervisor/students/', views.supervisor_students_view, name='supervisor_students'),
    path('supervisor/student/<int:student_id>/', views.supervisor_student_detail_view, name='supervisor_student_detail'),
    path('<int:pk>/evaluate/', views.project_evaluate_view, name='evaluate'),
    
    # Réunion de cadrage
    path('<int:project_id>/kickoff/', views.project_kickoff_view, name='kickoff'),
    
    path('<int:pk>/', views.project_detail_view, name='detail'),
    path('<int:pk>/update/', views.project_update_view, name='update'),
    path('<int:project_pk>/milestone/create/', views.milestone_create_view, name='milestone_create'),
    path('milestone/<int:milestone_pk>/update/', views.milestone_update_view, name='milestone_update'),
    path('milestone/<int:milestone_pk>/validate/', views.milestone_validate_view, name='milestone_validate'),
    path('<int:project_pk>/deliverable/create/', views.deliverable_create_view, name='deliverable_create'),
    path('<int:project_pk>/deliverable/submit/', views.deliverable_submit_view, name='deliverable_submit'),
    path('deliverable/<int:deliverable_pk>/review/', views.deliverable_review_view, name='deliverable_review'),
]
