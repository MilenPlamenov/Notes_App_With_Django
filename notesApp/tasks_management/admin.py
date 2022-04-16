from django.contrib import admin

from notesApp.tasks_management.models import Task


@admin.register(Task)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("name", "text")
    search_fields = ("name",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
