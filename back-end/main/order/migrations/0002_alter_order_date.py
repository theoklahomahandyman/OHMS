# Generated by Django 5.1 on 2024-10-04 02:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.date(2024, 10, 4)),
            preserve_default=False,
        ),
    ]
