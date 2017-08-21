from datetime import date
from django.db import models
from django.db.models import Sum, F
from decimal import Decimal


class City(models.Model):
    name = models.CharField(max_length=60)
    department = models.CharField(max_length=60)

    @property
    def count_clients(self):
        return self.client_set.count()

    @property
    def amount_invoiced(self):
        clients = self.client_set.all()
        total = Decimal('0.00')
        for client in clients:
            total = total + client.amount_invoiced
        return total

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=60)
    nit = models.CharField(max_length=60)
    city = models.ForeignKey(City)

    @property
    def count_invoiced(self):
        return self.invoice_set.count()

    @property
    def amount_invoiced(self):
        total = Decimal('0.00')
        for inv in self.invoice_set.all():
            total = total + inv.total
        return total

    @property
    def participation(self):
        total_all = get_total_invoiced()
        participation = (self.amount_invoiced / total_all) * 100
        return participation

    def __str__(self):
        return self.name

class SalesPerson(models.Model):
    name = models.CharField(max_length=60)
    nit = models.CharField(max_length=60)
    city = models.ForeignKey(City)

    @property
    def count_invoiced(self):
        return self.invoice_set.count()

    @property
    def amount_invoiced(self):
        total = Decimal('0.00')
        for inv in self.invoice_set.all():
            total = total + inv.total
        return total

    @property
    def participation(self):
        total_all = get_total_invoiced()
        participation = (self.amount_invoiced / total_all) * 100
        return participation
    
    @property
    def average_invoice(self):
        invoices = self.invoice_set.all()
        invoice_total = Decimal('0.00')
        for invoice in invoices:
            invoice_total += invoice.total

        if len(invoices) > 0:
            average = invoice_total / len(invoices)
        else:
            average = 0
        
        return average


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
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)

    # @property
    # def total(self):
    #     total = Decimal('0.00')
    #     for item in self.items.all():
    #         total = total + item.total
    #     return total

    def total_amount(self):
        return self.total()

    @property
    def total(self):
        return self.items.aggregate(total=Sum(F('unit_price') * F('quantity')))['total']

    def __str__(self):
        return self.number

class Product(models.Model):
    description = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    @property
    def total(self):
        total = self.invoiceitem_set.aggregate(total=Sum(F('unit_price') * F('quantity')))['total']    
        return total if total else 0

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

def get_total_invoiced():
    invoices = Invoice.objects.all()
    total = Decimal('0.00')
    for inv in invoices:
        total = total + inv.total
    return total
        