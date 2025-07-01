from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-collected_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    ordering_fields = ['price', 'collected_at']
    ordering = ['-collected_at']

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
