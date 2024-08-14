from django_filters import rest_framework as filters
from resume.models import ResumeModel, FavoritesResume
from django.db.models import Q


class ResumetFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ResumeModel
        fields = ['name'] 


class FavoriteFilter(filters.FilterSet):
    resume_owner = filters.CharFilter(method='filter_by_full_name')

    class Meta:
        model = FavoritesResume
        fields = ['resume_owner'] 
    
    def filter_by_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(resume__owner__first_name__icontains=value) |
            Q(resume__owner__last_name__icontains=value)
        )