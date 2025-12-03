from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list_view, name='list'),
    path('<int:pk>/', views.project_detail_view, name='detail'),
    path('<int:pk>/update/', views.project_update_view, name='update'),
    path('<int:project_pk>/milestone/create/', views.milestone_create_view, name='milestone_create'),
    path('<int:project_pk>/deliverable/submit/', views.deliverable_submit_view, name='deliverable_submit'),
]
