from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class QRCode(models.Model):
    """Model for storing QR code data"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qrcodes', null=True, blank=True)
    content = models.CharField(_('Content'), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(_('Name'), max_length=100, blank=True)
    
    # QR Code customization options
    foreground_color = models.CharField(_('Foreground Color'), max_length=7, default='#000000')
    background_color = models.CharField(_('Background Color'), max_length=7, default='#FFFFFF')
    box_size = models.PositiveIntegerField(_('Box Size'), default=10)
    border = models.PositiveIntegerField(_('Border Size'), default=4)
    
    # New fields for logo customization
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    logo_size = models.PositiveIntegerField(default=100)  # Size in pixels
    transparent_background = models.BooleanField(default=False)  # Transparent background option
    
    # New fields for additional customization
    logo_position = models.CharField(_('Logo Position'), max_length=20, choices=[
        ('center', _('Center')),
        ('top-left', _('Top Left')),
        ('top-right', _('Top Right')),
        ('bottom-left', _('Bottom Left')),
        ('bottom-right', _('Bottom Right')),
    ], default='center')
    
    border_style = models.CharField(_('Border Style'), max_length=20, choices=[
        ('solid', _('Solid')),
        ('dashed', _('Dashed')),
        ('dotted', _('Dotted')),
    ], default='solid')
    
    # For analytics
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    download_count = models.PositiveIntegerField(_('Download Count'), default=0)
    share_count = models.PositiveIntegerField(_('Share Count'), default=0)
    
    class Meta:
        verbose_name = _('QR Code')
        verbose_name_plural = _('QR Codes')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name or self.content[:20]}"
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def increment_download_count(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    def increment_share_count(self):
        self.share_count += 1
        self.save(update_fields=['share_count'])

class UserPreference(models.Model):
    """Model for storing user preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    language = models.CharField(_('Language'), max_length=10, default='en')
    default_qr_foreground = models.CharField(_('Default QR Foreground'), max_length=7, default='#000000')
    default_qr_background = models.CharField(_('Default QR Background'), max_length=7, default='#FFFFFF')
    
    class Meta:
        verbose_name = _('User Preference')
        verbose_name_plural = _('User Preferences')
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
