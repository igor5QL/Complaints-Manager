# Generated by Django 4.2.2 on 2023-07-13 22:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_ticket_complaint_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='complaint_date',
            field=models.DateField(default=datetime.datetime(2022, 3, 28, 6, 42, 31)),
        ),
    ]
