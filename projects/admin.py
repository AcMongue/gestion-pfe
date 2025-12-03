from django.contrib import admin
from .models import Project, Milestone, Deliverable, Comment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'assignment', 'status', 'progress_percentage', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'due_date', 'validated_by_supervisor']
    list_filter = ['status', 'validated_by_supervisor']
    search_fields = ['title', 'description']

@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'type', 'status', 'version', 'submitted_at']
    list_filter = ['type', 'status']
    search_fields = ['title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'project', 'created_at', 'is_private']
    list_filter = ['is_private', 'created_at']
