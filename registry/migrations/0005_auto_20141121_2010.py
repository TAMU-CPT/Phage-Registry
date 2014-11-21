# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0004_auto_20141121_1932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registryentry',
            old_name='exturl',
            new_name='extid',
        ),
    ]
