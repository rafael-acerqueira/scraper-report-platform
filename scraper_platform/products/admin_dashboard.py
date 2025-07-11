from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render

from .admin import ProductAdmin
from .models import Product

class CustomAdminSite(AdminSite):
    site_header = "Scraper Report Platform Admin"
    site_title = "Scraper Admin"
    index_title = "Welcome to Scraper Painel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        total_products = Product.objects.count()
        latest = Product.objects.order_by('-collected_at').first()
        last_collected = latest.collected_at if latest else "—"
        context = dict(
            self.each_context(request),
            total_products=total_products,
            last_collected=last_collected,
        )
        return render(request, "admin/dashboard.html", context)

admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(Product, ProductAdmin)