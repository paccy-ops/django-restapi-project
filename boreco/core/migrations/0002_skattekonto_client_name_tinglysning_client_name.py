# Generated by Django 4.0 on 2022-04-18 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skattekonto',
            name='client_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tinglysning',
            name='client_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]