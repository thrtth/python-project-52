from django.urls import path
from django_filters.views import FilterView

from task_manager.tasks import views
from task_manager.tasks.filters import TaskFilter


urlpatterns = [
    path('', FilterView.as_view(filterset_class=TaskFilter), name='tasks'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', views.TaskView.as_view(), name='task_view'),
]
