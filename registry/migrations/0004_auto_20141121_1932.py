# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0003_registryentry_alias_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('template_url', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='registryentry',
            name='database',
            field=models.ForeignKey(blank=True, to='registry.DatabaseSource', null=True),
            preserve_default=True,
        ),
    ]
