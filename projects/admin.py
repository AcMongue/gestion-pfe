from django.contrib import admin
from .models import Project, Milestone, Deliverable, Comment, AcademicYear, ProjectTeam

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'start_date', 'end_date', 'thesis_submission_deadline', 'is_active']
    list_filter = ['is_active']
    search_fields = ['year']
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        """Assure qu'une seule année est active."""
        if obj.is_active:
            AcademicYear.objects.filter(is_active=True).exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)

@admin.register(ProjectTeam)
class ProjectTeamAdmin(admin.ModelAdmin):
    list_display = ['project', 'student1', 'student2', 'is_pair', 'created_at']
    list_filter = ['created_at']
    search_fields = ['project__title', 'student1__username', 'student2__username']
    readonly_fields = ['created_at']

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
