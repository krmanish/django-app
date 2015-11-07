# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgmnt', '0005_remove_movies_popularity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='genre',
            field=models.ManyToManyField(to='mgmnt.Genres', db_index=True),
        ),
    ]
