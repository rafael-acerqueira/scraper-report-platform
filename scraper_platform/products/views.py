import csv

from django.core.management import call_command
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from scraper.registry import get_scraper
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
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

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


class ScrapeTriggerView(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        scraper_name = request.data.get('scraper')
        if not scraper_name:
            return Response({"error": "Missing 'scraper' parameter."}, status=400)

        try:
            import scraper.book_scraper
            get_scraper(scraper_name)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        try:
            call_command('collect_products', f'--scraper={scraper_name}')
            return Response({"status": "success", "message": f"Scraper '{scraper_name}' executed."})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)