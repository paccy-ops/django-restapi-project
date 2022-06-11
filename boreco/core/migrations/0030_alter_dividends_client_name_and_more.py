# Generated by Django 4.0 on 2022-04-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_dividends_client_responsible_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dividends',
            name='client_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='eindkomst',
            name='client_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='skattekonto',
            name='client_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]