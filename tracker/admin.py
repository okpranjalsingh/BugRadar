from django.contrib import admin
from .models import Project, Bug, Priority, Status

# register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'levels')   
    search_fields = ('levels',)


@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', 'status', 'priority', 'reported_by', 'created_at')
    search_fields = ('title', 'project__name', 'reported_by__username')
    list_filter = ('status', 'priority', 'created_at')
    ordering = ('-created_at',)
    autocomplete_fields = ('project', 'status', 'priority', 'reported_by')
