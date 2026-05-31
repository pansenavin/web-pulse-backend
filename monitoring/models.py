from django.db import models
from django.conf import settings

class Website(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='websites')
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=2048)
    interval_minutes = models.IntegerField(default=5)
    is_paused = models.BooleanField(default=False)
    
    STATUS_CHOICES = (
        ('up', 'up'),
        ('down', 'down'),
        ('unknown', 'unknown'),
    )
    last_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unknown')
    last_http_code = models.IntegerField(null=True, blank=True)
    last_response_time = models.IntegerField(null=True, blank=True)
    last_check_time = models.DateTimeField(null=True, blank=True)
    uptime_pct = models.FloatField(default=100.0)
    
    email1 = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)
    email3 = models.EmailField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CheckLog(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='logs')
    check_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    response_time = models.IntegerField(null=True, blank=True)
    http_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.website.name} - {self.status} at {self.check_time}"
