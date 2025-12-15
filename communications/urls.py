from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    # Messages
    path('messages/', views.inbox_view, name='message_list'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('sent/', views.sent_messages_view, name='sent'),
    path('compose/', views.compose_message_view, name='compose'),
    path('create/', views.compose_message_view, name='message_create'),  # Alias
    path('message/<int:pk>/', views.message_detail_view, name='message_detail'),
    path('message/<int:pk>/delete/', views.delete_message_view, name='delete_message'),
    
    # Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/', views.notifications_view, name='notification_list'),  # Alias
    path('notification/<int:pk>/read/', views.mark_notification_read_view, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read_view, name='mark_all_notifications_read'),
]
