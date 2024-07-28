from django_filters import rest_framework as filters
from resume.models import ResumeModel


class ResumetFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ResumeModel
        fields = ['name'] 