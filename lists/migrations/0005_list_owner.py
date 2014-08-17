# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0004_auto_20140816_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
