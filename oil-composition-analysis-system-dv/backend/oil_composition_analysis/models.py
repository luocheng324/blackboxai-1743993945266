from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Component(models.Model):
    class Meta:
        app_label = 'oil_composition_analysis'
    COMPONENT_TYPES = [
        ('FILTER', 'Filter'),
        ('ANALYZER', 'Analyzer'),
        ('SENSOR', 'Sensor'),
        ('OUTPUT', 'Output'),
    ]
    
    type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    name = models.CharField(max_length=100)
    parameters = models.JSONField(default=dict)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

class ComponentConnection(models.Model):
    source = models.ForeignKey(Component, related_name='outputs', on_delete=models.CASCADE)
    target = models.ForeignKey(Component, related_name='inputs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'oil_composition_analysis'
        unique_together = ('source', 'target')

class AnalysisResult(models.Model):
    class Meta:
        app_label = 'oil_composition_analysis'
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    components = models.ManyToManyField(Component)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    results = models.JSONField(default=dict)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class UserUpload(models.Model):
    class Meta:
        app_label = 'oil_composition_analysis'
    file = models.FileField(upload_to='uploads/')
    upload_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analysis = models.ForeignKey(AnalysisResult, on_delete=models.SET_NULL, null=True, blank=True)