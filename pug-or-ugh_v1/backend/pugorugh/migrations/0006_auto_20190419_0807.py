# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-04-19 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0005_auto_20190419_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='dog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dog_user_relation', to='pugorugh.Dog'),
        ),
    ]
