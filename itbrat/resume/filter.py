from django_filters import rest_framework as filters
from resume.models import ResumeModel, FavoritesResume


class ResumetFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ResumeModel
        fields = ['name'] 


class FavoriteFilter(filters.FilterSet):
    resume_name = filters.CharFilter(field_name='resume__name', lookup_expr='icontains')

    class Meta:
        model = FavoritesResume
        fields = ['resume_name'] 