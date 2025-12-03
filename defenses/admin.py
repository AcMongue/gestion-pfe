from django.contrib import admin
from .models import Defense, JuryMember, DefenseEvaluation

@admin.register(Defense)
class DefenseAdmin(admin.ModelAdmin):
    list_display = ['project', 'date', 'time', 'room', 'status', 'final_grade']
    list_filter = ['status', 'date']
    search_fields = ['project__title', 'room']

@admin.register(JuryMember)
class JuryMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'defense', 'role', 'grade']
    list_filter = ['role']

@admin.register(DefenseEvaluation)
class DefenseEvaluationAdmin(admin.ModelAdmin):
    list_display = ['defense', 'presentation_quality', 'content_mastery', 'technical_skills']
