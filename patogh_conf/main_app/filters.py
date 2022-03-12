from django_filters import rest_framework as filters
from .models import PatoghInfo


class PatoghInfoFilter(filters.FilterSet):

    class Meta:
        model = PatoghInfo
        fields = ['name','city']
