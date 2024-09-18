import django_filters
from .models import BookLog


class BookFilter(django_filters.FilterSet):
    publishers = django_filters.CharFilter(field_name='publishers', lookup_expr='iexact')
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')

    class Meta:
        model = BookLog
        fields = ['publishers', 'category']
