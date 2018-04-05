# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-05 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0019_extra_charge_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra_charge',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Booking'),
        ),
    ]
