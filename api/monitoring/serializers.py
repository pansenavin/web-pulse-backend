from rest_framework import serializers
from monitoring.models import Website, CheckLog

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'
        read_only_fields = ['user', 'last_status', 'last_http_code', 'last_response_time', 'last_check_time', 'uptime_pct', 'created_at', 'updated_at']

class CheckLogSerializer(serializers.ModelSerializer):
    website_name = serializers.CharField(source='website.name', read_only=True)

    class Meta:
        model = CheckLog
        fields = ['id', 'website', 'website_name', 'check_time', 'status', 'response_time', 'http_code']
