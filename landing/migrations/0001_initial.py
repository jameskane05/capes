# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import landing.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('notes', models.TextField(blank=True)),
                ('link', models.CharField(max_length=254)),
                ('exp_date', models.DateTimeField(default=landing.models.get_exp_date)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
