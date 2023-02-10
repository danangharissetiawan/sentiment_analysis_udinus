from django.contrib import admin

from .models import Broadcast


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'classification']
    list_filter = ['classification']
    search_fields = ['name', 'email', 'message']

# admin.site.register(Broadcast, BroadcastAdmin)