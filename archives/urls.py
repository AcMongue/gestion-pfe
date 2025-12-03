from django.urls import path
from . import views

app_name = 'archives'

urlpatterns = [
    path('', views.archive_list_view, name='list'),
    path('<int:pk>/', views.archive_detail_view, name='detail'),
    path('archive/<int:project_id>/', views.archive_project_view, name='archive_project'),
    path('reports/', views.reports_view, name='reports'),
    path('reports/generate/', views.generate_report_view, name='generate_report'),
    path('reports/<int:pk>/', views.report_detail_view, name='report_detail'),
]
