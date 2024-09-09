from django.contrib import admin
from project.models import Project, CategoriyaProject, FavoritesProject, Notification

admin.site.register(Project)
admin.site.register(CategoriyaProject)
admin.site.register(FavoritesProject)

admin.site.register(Notification)
