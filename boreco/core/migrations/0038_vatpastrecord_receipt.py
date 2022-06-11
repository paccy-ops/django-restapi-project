# Generated by Django 4.0 on 2022-05-25 06:00

import boreco.azure_storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_alter_vatpastrecord_filing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='vatpastrecord',
            name='receipt',
            field=models.FileField(blank=True, null=True, storage=boreco.azure_storage.PrivateAzureStorage(), upload_to=''),
        ),
    ]
