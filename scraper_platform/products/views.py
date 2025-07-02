import csv
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

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


class ProductExportView(APIView):
    def get(self, request):
        export_format = request.query_params.get('export_format', 'json')
        queryset = Product.objects.all()
        filterset = ProductFilter(request.GET, queryset=queryset)
        products = filterset.qs

        serializer = ProductSerializer(products, many=True)
        data = serializer.data

        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="products.csv"'
            writer = csv.writer(response)
            writer.writerow(['id', 'title', 'price', 'collected_at'])
            for item in data:
                writer.writerow([item['id'], item['title'], item['price'], item['collected_at']])
            return response


        return Response(data, status=status.HTTP_200_OK)
