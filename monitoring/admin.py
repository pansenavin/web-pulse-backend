from django.contrib import admin
from .models import Website, CheckLog

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'user', 'last_status', 'is_paused', 'created_at')
    list_filter = ('last_status', 'is_paused')
    search_fields = ('name', 'url')

@admin.register(CheckLog)
class CheckLogAdmin(admin.ModelAdmin):
    list_display = ('website', 'status', 'check_time', 'response_time', 'http_code')
    list_filter = ('status',)
    search_fields = ('website__name',)
