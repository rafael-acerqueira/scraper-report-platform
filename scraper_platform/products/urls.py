from django.urls import path
from .views import ProductListView, ProductDetailView, ProductExportView, ScrapeTriggerView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/export/', ProductExportView.as_view(), name='product-export'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('scrape/', ScrapeTriggerView.as_view(), name='scrape-trigger')
]