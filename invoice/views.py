from django.shortcuts import render, redirect
from invoice.forms import InvoiceForm, InvoiceItemForm, ClientForm, SalesPersonForm, ProductForm, ConexionForm
from django.forms import formset_factory, modelformset_factory
from .models import Invoice, InvoiceItem, Product, Client, SalesPerson, City
from django.http import JsonResponse
from django.core import serializers
from decimal import Decimal

# Create your views here.
def index(request):
    return render(request, "index.html", {})

def conexion(request):
    form = ConexionForm()
    return render(request, "conexion.html", {'form': form})

def register_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_client')
    else:
        form = ClientForm()
    return render(request, 'client.html', {'form': form})

def register_salesperson(request):
    if request.method == "POST":
        form = SalesPersonForm(request.POST)
        print(form)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('register_salesperson')
    else:
        form = SalesPersonForm()    
    return render(request, 'salesperson.html', {'form': form})

def register_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_product')
    else:    
        form = ProductForm()
    return render(request, 'product.html', {'form': form})


def invoice(request):
    InvoiceFormSet = formset_factory(InvoiceItemForm)
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        formset = InvoiceFormSet(request.POST)
        if invoice_form.is_valid():
            number = invoice_form.cleaned_data['number']
            client = invoice_form.cleaned_data['client']
            sales_person = invoice_form.cleaned_data['sales_person']
            invoice_date = invoice_form.cleaned_data['invoice_date']
            paid_date = invoice_form.cleaned_data['due_date']
            tax = invoice_form.cleaned_data['tax']
            terms = invoice_form.cleaned_data['terms']
            notes = invoice_form.cleaned_data['notes']
            invoice = Invoice(number=number,
                              client=client,
                              sales_person=sales_person,
                              invoice_date=invoice_date,
                              due_date=paid_date,
                              tax=tax,
                              terms=terms,                              
                              notes=notes
                              )
            invoice.save()

            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        product_str = form.cleaned_data['product']
                        product = Product.objects.filter(description=product_str).first()
                        price_str = form.cleaned_data['unit_price']
                        quantity_str = form.cleaned_data['quantity']                        
                        inv_item = InvoiceItem(invoice=invoice,
                                               product=product,
                                               unit_price=Decimal(price_str),
                                               quantity=Decimal(quantity_str)
                                               )
                        inv_item.save()                        

        return redirect('invoice')
    else:
        invoice_form = InvoiceForm()
        formset = InvoiceFormSet()
    return render(request, "invoice.html", {'invoice_form':invoice_form, 'formset': formset})


def get_products(request):
    products = list(Product.objects.all().values_list('description'))
    return JsonResponse({'products': products})

def get_city(request):
    clientID = request.GET.get('client')
    try:
        city = Client.objects.get(pk=clientID).city.name
    except:
        city = None
    return JsonResponse({'city': city})

## REPORTES
def report_clients(request):
    clients = Client.objects.all()
    return render(request, 'reporte_clientes.html', {'clients': clients})

def report_salespersons(request):
    salespersons = SalesPerson.objects.all()
    return render(request, 'reporte_vendedores.html', {'salespersons': salespersons})

def report_products(request):
    products = Product.objects.all()
    return render(request, 'reporte_productos.html', {'products': products})

def report_cities(request):
    cities = City.objects.all()
    return render(request, 'reporte_ciudades.html', {'cities': cities})

def dashboard(request):
    clients = Client.objects.count()
    invoices = Invoice.objects.all()
    total_invoiced = Decimal('0.00')
    for inv in invoices:
        total_invoiced = total_invoiced + inv.total
    total_invoiced = round(total_invoiced / Decimal(1e6))
    invoice_count = Invoice.objects.count()

    return render(request, 'dashboard.html', {'clients': clients, 'total_invoiced': total_invoiced, 'invoice_count': invoice_count})

# DASHBOARD REQUESTS
def get_city_data(request):
    citydata = []
    cities = City.objects.all()

    for city in cities:
        citydata.append([city.name, city.amount_invoiced])
    
    return JsonResponse({'citydata': citydata})


def get_total_month(request):
    invoices = Invoice.objects.all()
    monthdata = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    for inv in invoices:
        if inv.invoice_date.year == 2017:
            monthdata[inv.invoice_date.month] += inv.total
    
    return JsonResponse({'monthdata': list(monthdata.values())})


def get_top_products(request):
    products = Product.objects.all()
    sorted_products = sorted(products, key=lambda t: t.total, reverse=True)
    productdata = []
    for product in sorted_products:
        productdata.append([product.description, product.total])
    
    return JsonResponse({'productdata': productdata})

def get_top_clients(request):
    clients = Client.objects.all()
    sorted_clients = sorted(clients, key=lambda t: t.amount_invoiced, reverse=True)
    clientdata = []
    for client in sorted_clients:
        clientdata.append([client.name, client.amount_invoiced])
    
    return JsonResponse({'clientdata': clientdata})

def get_top_salespersons(request):
    salesperson = SalesPerson.objects.all()
    sorted_salesperson = sorted(salesperson, key=lambda t: t.amount_invoiced, reverse=True)
    salespersondata = []
    for salesperson in sorted_salesperson:
        salespersondata.append([salesperson.name, salesperson.amount_invoiced])
    
    return JsonResponse({'salespersondata': salespersondata})