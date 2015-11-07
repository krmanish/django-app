# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Directors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_ts', models.DateTimeField(help_text=b'Created timespan for each record', auto_now_add=True)),
                ('updated_ts', models.DateTimeField(help_text=b'Updated timespan for each record', auto_now=True)),
                ('full_name', models.CharField(help_text=b'Directors full name', unique=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_ts', models.DateTimeField(help_text=b'Created timespan for each record', auto_now_add=True)),
                ('updated_ts', models.DateTimeField(help_text=b'Updated timespan for each record', auto_now=True)),
                ('genre', models.CharField(help_text=b'Genre Name', unique=True, max_length=25)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_ts', models.DateTimeField(help_text=b'Created timespan for each record', auto_now_add=True)),
                ('updated_ts', models.DateTimeField(help_text=b'Updated timespan for each record', auto_now=True)),
                ('popularity', models.DecimalField(help_text=b'99popularity', null=True, max_digits=4, decimal_places=2, blank=True)),
                ('imdb_score', models.DecimalField(decimal_places=1, max_digits=2, blank=True, help_text=b'IMDB scores', null=True, db_index=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('is_active', models.BooleanField(default=True, help_text=b'Flags to mark data as active or inactive')),
                ('is_deleted', models.BooleanField(default=False, help_text=b'Delete Flag')),
                ('created_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('director', models.ForeignKey(to='mgmnt.Directors')),
                ('genre', models.ManyToManyField(to='mgmnt.Genres', db_index=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='movies',
            unique_together=set([('director', 'name', 'is_deleted')]),
        ),
    ]
