from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-collected_at')
    serializer_class = ProductSerializer
