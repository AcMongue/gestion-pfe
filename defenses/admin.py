from django.contrib import admin
from .models import Defense, JuryMember, DefenseEvaluation, DefenseChangeRequest
from django.utils.html import format_html

@admin.register(Defense)
class DefenseAdmin(admin.ModelAdmin):
    list_display = ['project', 'date', 'time', 'room_display', 'status', 'final_grade']
    list_filter = ['status', 'date', 'room_obj']
    search_fields = ['project__title', 'room']
    
    def room_display(self, obj):
        """Affiche la salle avec le bâtiment"""
        if obj.room_obj:
            return format_html('<strong>{}</strong> ({})', obj.room_obj.name, obj.room_obj.building)
        return obj.room or '-'
    room_display.short_description = 'Salle'

@admin.register(JuryMember)
class JuryMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'defense', 'role', 'grade']
    list_filter = ['role']

@admin.register(DefenseEvaluation)
class DefenseEvaluationAdmin(admin.ModelAdmin):
    list_display = ['defense', 'presentation_quality', 'content_mastery', 'technical_skills']

@admin.register(DefenseChangeRequest)
class DefenseChangeRequestAdmin(admin.ModelAdmin):
    list_display = ['defense', 'requested_by', 'status', 'created_at', 'reviewed_by']
    list_filter = ['status', 'created_at']
    search_fields = ['defense__project__title', 'requested_by__username', 'reason']
