"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
# from apps.projects.views.projects import ProjectListCreateView, ProjectDetailView  # get_all_projects
# from apps.tasks.views import get_all_tasks, get_task_by_id
# from apps.tasks.views import (get_all_tags, get_tag_by_id, update_required_tag,
#                                    create_tag, delete_required_tag)
from apps.tasks.views import TaskListCreateViewSet, TaskDetailViewSet, TaskViewSet
from apps.projects.views import ProjectFileViewSet
from apps.users.views import UserViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')
router.register('project-files', ProjectFileViewSet, basename='project_files')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

]
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('projects/', get_all_projects),
#     path('projects/', ProjectListCreateView.as_view(), name='list_create_project'),
#     path('projects/<int:project_id>/', ProjectDetailView.as_view(), name='detail_project'),
#     path('tasks/', get_all_tasks),
#     path('tasks/<int:task_id>/', get_task_by_id),
#     path('tags/', get_all_tags, name='all_tags'),
#     path('tags/<int:tag_id>/', get_tag_by_id),
#     path('tags/<int:tag_id>/update/', update_required_tag, name='change_tag_name'),
#     path('tags/create/', create_tag),
#     path('tags/<int:tag_id>/delete/', delete_required_tag),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



"""
для объединения адресов из разных АПП в один

from django.urls import path, include
urlpatterns = [
    path('tasks/', include('apps.tasks.urls')),
    path('projects/', include('apps.projects.urls')), # NEW
]


"""