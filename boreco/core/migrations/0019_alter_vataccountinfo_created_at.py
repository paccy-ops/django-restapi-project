# Generated by Django 4.0 on 2022-04-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_accountstatus_client_name_vataccountinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vataccountinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
