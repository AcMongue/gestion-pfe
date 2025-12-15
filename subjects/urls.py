from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    # Sujets
    path('', views.subject_list_view, name='list'),
    path('', views.subject_list_view, name='subject_list'),  # Alias
    path('<int:pk>/', views.subject_detail_view, name='detail'),
    path('create/', views.subject_create_view, name='create'),
    path('create/', views.subject_create_view, name='subject_create'),  # Alias
    path('<int:pk>/update/', views.subject_update_view, name='update'),
    path('<int:pk>/edit/', views.subject_update_view, name='subject_edit'),  # Alias
    path('<int:pk>/delete/', views.subject_delete_view, name='delete'),
    path('my-subjects/', views.my_subjects_view, name='my_subjects'),
    
    # Candidatures
    path('<int:subject_pk>/apply/', views.application_create_view, name='apply'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
    path('applications/<int:pk>/withdraw/', views.application_withdraw_view, name='application_withdraw'),
    path('<int:subject_pk>/applications/', views.subject_applications_view, name='subject_applications'),
    path('applications/<int:pk>/review/', views.application_review_view, name='application_review'),
    
    # Affectations (Admin)
    path('assignments/', views.assignments_manage_view, name='assignments_manage'),
    path('assignments/<int:pk>/', views.assignment_detail_view, name='assignment_detail'),
    path('assignments/create/<int:application_pk>/', views.assignment_create_view, name='assignment_create'),
    path('assignments/<int:pk>/cancel/', views.assignment_cancel_view, name='assignment_cancel'),
    
    # Propositions d'étudiants
    path('proposals/create/', views.student_proposal_create_view, name='proposal_create'),
    path('proposals/my-proposals/', views.student_proposal_list_view, name='my_proposals'),
    path('proposals/', views.supervisor_proposals_view, name='supervisor_proposals'),
    path('proposals/<int:pk>/', views.proposal_detail_view, name='proposal_detail'),
    path('proposals/<int:pk>/accept/', views.proposal_accept_view, name='proposal_accept'),
    path('proposals/<int:pk>/reject/', views.proposal_reject_view, name='proposal_reject'),
]
