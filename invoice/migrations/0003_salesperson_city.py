# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-17 04:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20170815_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesperson',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='invoice.City'),
            preserve_default=False,
        ),
    ]
