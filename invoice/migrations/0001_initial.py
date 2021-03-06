# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-27 05:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('department', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('nit', models.CharField(max_length=60)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.City')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=60)),
                ('invoice_date', models.DateField(default=datetime.date.today)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('notes', models.TextField(blank=True)),
                ('terms', models.TextField(blank=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Client')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoice.Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('measurement_unit', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SalesPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('nit', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Product'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='sales_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.SalesPerson'),
        ),
    ]
