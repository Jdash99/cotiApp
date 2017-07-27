from datetime import date
from django.db import models
from decimal import Decimal

class City(models.Model):
    name = models.CharField(max_length=60)
    department = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=60)
    nit = models.CharField(max_length=60)
    city = models.ForeignKey(City)

    def __str__(self):
        return self.name

class SalesPerson(models.Model):
    name = models.CharField(max_length=60)
    nit = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    number = models.CharField(max_length=60)
    client = models.ForeignKey(Client)
    sales_person = models.ForeignKey(SalesPerson)
    invoice_date = models.DateField(default=date.today)
    due_date = models.DateField(blank=True, null=True)
    tax = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    terms = models.TextField(blank=True)

    @property
    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total
        return total

    def __str__(self):
        return self.number

class Product(models.Model):
    description = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.description

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items')
    product = models.ForeignKey(Product)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    @property
    def total(self):
        total = Decimal(str(self.unit_price * self.quantity))
        return total.quantize(Decimal('0.01'))

    def __str(self):
        return str(self.id)
    