from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    # Sujets
    path('', views.subject_list_view, name='list'),
    path('<int:pk>/', views.subject_detail_view, name='detail'),
    path('create/', views.subject_create_view, name='create'),
    path('<int:pk>/update/', views.subject_update_view, name='update'),
    path('<int:pk>/delete/', views.subject_delete_view, name='delete'),
    path('my-subjects/', views.my_subjects_view, name='my_subjects'),
    
    # Candidatures
    path('<int:subject_pk>/apply/', views.application_create_view, name='apply'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
    path('applications/<int:pk>/withdraw/', views.application_withdraw_view, name='application_withdraw'),
    path('<int:subject_pk>/applications/', views.subject_applications_view, name='subject_applications'),
    path('applications/<int:pk>/review/', views.application_review_view, name='application_review'),
]
