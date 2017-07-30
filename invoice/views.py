from django.shortcuts import render, redirect
from invoice.forms import InvoiceForm, InvoiceItemForm, ClientForm, SalesPersonForm, ProductForm, ConexionForm
from django.forms import formset_factory, modelformset_factory
from .models import Invoice, InvoiceItem, Product, Client
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
        print("is valid: ", invoice_form.is_valid())
        print(invoice_form.errors)
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
