from django.contrib import admin

from .admin_actions import export_products_csv, export_products_json

class PriceRangeFilter(admin.SimpleListFilter):
    title = 'price range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('0-20', '0 - 20'),
            ('20-50', '20 - 50'),
            ('50+', '50+'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-20':
            return queryset.filter(price__gte=0, price__lte=20)
        if self.value() == '20-50':
            return queryset.filter(price__gt=20, price__lte=50)
        if self.value() == '50+':
            return queryset.filter(price__gt=50)
        return queryset


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'formatted_price', 'collected_at')
    search_fields = ('title',)
    list_filter = ('collected_at', PriceRangeFilter)
    ordering = ('-collected_at',)
    date_hierarchy = 'collected_at'
    actions = [export_products_csv, export_products_json]
    readonly_fields = ('collected_at',)
    list_per_page = 20

    def formatted_price(self, obj):
        return f"USD {obj.price:.2f}"