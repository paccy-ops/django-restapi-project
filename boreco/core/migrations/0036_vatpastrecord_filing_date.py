# Generated by Django 4.0 on 2022-05-25 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_rename_months_eindkomst_month_remove_eindkomst_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vatpastrecord',
            name='filing_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
