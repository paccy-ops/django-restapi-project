# Generated by Django 4.0 on 2022-04-21 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_rename_filling_date_vatpastrecord_filing_deadline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vatpastrecord',
            name='filing_deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
