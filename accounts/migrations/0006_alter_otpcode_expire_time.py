# Generated by Django 5.2.1 on 2025-05-31 08:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_otpcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 31, 8, 21, 17, 421649, tzinfo=datetime.timezone.utc)),
        ),
    ]
