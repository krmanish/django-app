# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgmnt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='directors',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'Flags to mark data as active or inactive'),
        ),
        migrations.AddField(
            model_name='genres',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'Flags to mark data as active or inactive'),
        ),
    ]
