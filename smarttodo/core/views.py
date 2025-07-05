from django.shortcuts import render

from rest_framework import viewsets
from .models import Task, Category, ContextEntry
from .serializers import TaskSerializer, CategorySerializer, ContextEntrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ai_utils import generate_ai_suggestions
from .models import ContextEntry
from .serializers import TaskSerializer
from django.http import HttpResponse
import csv

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ContextEntryViewSet(viewsets.ModelViewSet):
    queryset = ContextEntry.objects.all().order_by('-created_at')
    serializer_class = ContextEntrySerializer

class TaskSuggestionAPIView(APIView):
    def post(self, request):
        task_data = request.data
        context_qs = ContextEntry.objects.all().order_by('-created_at')[:10]
        context_entries = [{"content": c.content, "source_type": c.source_type} for c in context_qs]

        suggestions = generate_ai_suggestions(task_data, context_entries)

        return Response({
            "priority_score": suggestions["priority"],
            "suggested_deadline": suggestions["deadline"],
            "enhanced_description": suggestions["enhanced_description"],
            "recommended_category": suggestions["category"]
        }, status=status.HTTP_200_OK)
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def export_tasks_csv(request):
    tasks = Task.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=\"tasks.csv\"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Deadline', 'Priority', 'Status', 'Category'])
    for t in tasks:
        writer.writerow([t.title, t.description, t.deadline, t.priority_score, t.status, t.category.name])

    return response
