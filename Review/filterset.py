from django_filters import rest_framework as filters
from .models import Product , Review , Category

from django_filters import rest_framework as filters
from django.db.models import Avg
from .models import Product

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'description']


class ReviewFilter(filters.FilterSet):
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr='lte')
    comment = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Category
        fields = ['name']