# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0002_auto_20141115_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='registryentry',
            name='alias_list',
            field=models.CharField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
