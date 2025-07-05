from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, ContextEntryViewSet, TaskSuggestionAPIView ,export_tasks_csv

router = DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('categories', CategoryViewSet)
router.register('context', ContextEntryViewSet)

urlpatterns = [
    path('suggest-task/', TaskSuggestionAPIView.as_view(), name='task-suggest'),
    path('', include(router.urls)),
    path("tasks/export/", export_tasks_csv)
]
