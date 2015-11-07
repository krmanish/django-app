# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgmnt', '0003_auto_20151107_0846'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='directors',
            unique_together=set([('full_name', 'is_active')]),
        ),
        migrations.AlterUniqueTogether(
            name='genres',
            unique_together=set([('genre', 'is_active')]),
        ),
    ]
