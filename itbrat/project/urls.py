from django.urls import path
from project.views import (
    ProjectCategoryView,
    ProjectsView,
    ProjectView,
    FavoritesProjectView,
    FavoriteProjectView,
)


urlpatterns = [
    path('category/project/', ProjectCategoryView.as_view()),
    path('project/', ProjectsView.as_view()),
    path('project/<int:pk>/', ProjectView.as_view()),
    # Favorite project
    path('fovorite/project/', FavoritesProjectView.as_view()),
    path('favorite/project/<int:pk>/', FavoriteProjectView.as_view()),

]