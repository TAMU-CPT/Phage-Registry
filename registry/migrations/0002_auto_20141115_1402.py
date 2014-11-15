# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registryentry',
            name='exturl',
            field=models.CharField(unique=True, max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='registryentry',
            name='phagename',
            field=models.CharField(unique=True, max_length=50),
            preserve_default=True,
        ),
    ]
