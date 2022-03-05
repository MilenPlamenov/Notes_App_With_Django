from django.contrib import admin

from notesApp.notes_management.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("subject", "text", "date")
    search_fields = ("subject", "date")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
