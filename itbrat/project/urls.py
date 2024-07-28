from django.urls import path
from project.views import (
    ProjectCategoryView,
    ProjectsView,
    ProjectView,
    FavoritesProjectView,
    FavoriteProjectView,
)


urlpatterns = [
    path('project/category/', ProjectCategoryView.as_view()),
    path('project/', ProjectsView.as_view()),
    path('project/<int:pk>/', ProjectView.as_view()),
    # Favorite project
    path('project/favorite/', FavoritesProjectView.as_view()),
    path('project/favorite/<int:pk>/', FavoriteProjectView.as_view()),

]