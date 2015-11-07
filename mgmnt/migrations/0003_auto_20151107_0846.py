# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgmnt', '0002_auto_20151107_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='genre',
            field=models.ManyToManyField(related_name='associated_genre', to='mgmnt.Genres', db_index=True),
        ),
    ]
