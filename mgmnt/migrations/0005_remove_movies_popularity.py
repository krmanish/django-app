# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgmnt', '0004_auto_20151107_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='popularity',
        ),
    ]
