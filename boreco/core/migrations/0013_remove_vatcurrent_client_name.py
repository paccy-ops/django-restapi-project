# Generated by Django 4.0 on 2022-04-18 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_client_owner_alter_clientassignment_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vatcurrent',
            name='client_name',
        ),
    ]
