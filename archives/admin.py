from django.contrib import admin
from .models import ArchivedProject, Report

@admin.register(ArchivedProject)
class ArchivedProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'year', 'semester', 'final_grade', 'archived_at', 'is_public']
    list_filter = ['year', 'semester', 'is_public']
    search_fields = ['project__title', 'keywords']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'period_start', 'period_end', 'generated_at']
    list_filter = ['type', 'generated_at']
