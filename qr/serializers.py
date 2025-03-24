from rest_framework import serializers
from .models import QRCode

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'content', 'created_at', 'name', 'foreground_color', 
                  'background_color', 'box_size', 'border', 'view_count', 
                  'download_count', 'share_count']
        read_only_fields = ['id', 'created_at', 'view_count', 'download_count', 'share_count'] 