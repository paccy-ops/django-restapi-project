# Generated by Django 4.0 on 2022-04-28 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_vataccountinfo_refund_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientassignment',
            name='client_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
