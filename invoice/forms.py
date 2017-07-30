from django import forms
from django.forms.formsets import formset_factory
from .models import Product, Client, SalesPerson

class InvoiceItemForm(forms.Form):
    try:
        pquery = Product.objects.all().values_list('description', flat=True)
        choices = [('', '---------')] + [(id, id) for id in pquery]
    except:
        choices = [('', '---------')]    
    product = forms.ChoiceField(choices)
    unit_price = forms.DecimalField(max_digits=8, decimal_places=2,
                    widget=forms.TextInput(attrs={'placeholder': 'Precio', 'class': 'rate'}))
    quantity = forms.DecimalField(max_digits=8, decimal_places=2,
                widget=forms.TextInput(attrs={'placeholder': 'Cantidad', 'class':'quantity'}))


class InvoiceForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all().order_by('name'))
    sales_person = forms.ModelChoiceField(queryset=SalesPerson.objects.all().order_by('name'))
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}))
    invoice_date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'class':'datepicker'}))
    due_date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'class':'datepicker'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'materialize-textarea'}))
    terms = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'materialize-textarea'}))
    tax = forms.DecimalField(max_digits=8, decimal_places=2,
                widget=forms.TextInput(attrs={'class':'taxes', 'id':'tax'}))


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'nit', 'city')


class SalesPersonForm(forms.ModelForm):

    class Meta:
        model = SalesPerson
        fields = ('name', 'nit')


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('description', 'measurement_unit')

class ConexionForm(forms.Form):
    servidor = forms.CharField(widget=forms.TextInput())
    base_datos = forms.CharField(widget=forms.TextInput())
    usuario = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())