import django_filters
from backend.models import Book


class BookFilter(django_filters.FilterSet):
    publishers = django_filters.CharFilter(field_name='publishers', lookup_expr='iexact')
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')

    class Meta:
        model = Book
        fields = ['publishers', 'category']
