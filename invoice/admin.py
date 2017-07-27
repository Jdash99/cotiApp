from django.contrib import admin
from .models import Invoice, InvoiceItem, Product, City, Client, SalesPerson

class InvoiceItemInline(admin.TabularInline):
    readonly_fields = ('total',)
    fields = ('product', 'unit_price', 'quantity', 'total')
    model = InvoiceItem

class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    inlines = [InvoiceItemInline]

admin.site.register(City)
admin.site.register(Client)
admin.site.register(SalesPerson)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Product)
