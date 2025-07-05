from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    usage_count = models.IntegerField(default=0)

class ContextEntry(models.Model):
    content = models.TextField()
    source_type = models.CharField(max_length=50, choices=[('whatsapp', 'WhatsApp'), ('email', 'Email'), ('note', 'Note')])
    created_at = models.DateTimeField(auto_now_add=True)
    processed_insight = models.JSONField(null=True, blank=True)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority_score = models.IntegerField(default=1)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('done', 'Done')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
