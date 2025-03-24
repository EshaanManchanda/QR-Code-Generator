from django.contrib import admin
from .models import QRCode, UserPreference

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'user', 'created_at', 'view_count', 'download_count', 'share_count')
    list_filter = ('created_at', 'user')
    search_fields = ('name', 'content', 'user__username')
    readonly_fields = ('view_count', 'download_count', 'share_count')
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'content', 'created_at')
        }),
        ('Customization', {
            'fields': ('foreground_color', 'background_color', 'box_size', 'border'),
        }),
        ('Analytics', {
            'fields': ('view_count', 'download_count', 'share_count'),
        }),
    )

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'default_qr_foreground', 'default_qr_background')
    search_fields = ('user__username',)
