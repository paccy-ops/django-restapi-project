# Generated by Django 4.0 on 2022-05-25 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_vatpastrecord_filing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vatpastrecord',
            name='filing_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
