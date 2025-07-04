from django.contrib import admin

from .admin_actions import export_products_csv, export_products_json
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'collected_at')
    search_fields = ('title',)
    list_filter = ('collected_at', 'price')
    ordering = ('-collected_at',)
    date_hierarchy = 'collected_at'
    actions = [export_products_csv, export_products_json]
    readonly_fields = ('collected_at',)


admin.site.site_header = "Scraper Report Platform Admin"
admin.site.site_title = "Scraper Admin"
admin.site.index_title = "Welcome to Scraper Painel"