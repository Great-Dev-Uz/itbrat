from django.urls import path
from resume.views import (
    HeadingView,
    ResumesView,
    ResumeView,
    FavoritesResumeView,
    FavoriteResumeView,
)


urlpatterns = [
    path('heading/resume/', HeadingView.as_view()),
    path('resume/', ResumesView.as_view()),
    path('resume/<int:pk>/', ResumeView.as_view()),
    # Favorite Resume
    path('favorite/resume/', FavoritesResumeView.as_view()),
    path('favorite/resume/<int:pk>/', FavoriteResumeView.as_view()),

]