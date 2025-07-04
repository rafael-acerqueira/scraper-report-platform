from django.http import HttpResponse
import csv
import json

def export_products_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=products.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'price', 'collected_at'])
    for obj in queryset:
        writer.writerow([obj.id, obj.title, obj.price, obj.collected_at])
    return response
export_products_csv.short_description = "Export selected as CSV"

def export_products_json(modeladmin, request, queryset):
    data = list(queryset.values('id', 'title', 'price', 'collected_at'))
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=products.json'
    return response
export_products_json.short_description = "Export selected as JSON"