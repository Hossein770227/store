# Generated by Django 5.2.1 on 2025-06-07 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_otpcode_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 7, 7, 55, 29, 863000, tzinfo=datetime.timezone.utc)),
        ),
    ]
