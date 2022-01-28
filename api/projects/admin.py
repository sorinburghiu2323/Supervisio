from django.contrib import admin

from api.projects.models import Project, ProjectApplication


admin.site.register(Project)
admin.site.register(ProjectApplication)
