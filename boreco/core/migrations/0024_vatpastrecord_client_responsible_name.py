# Generated by Django 4.0 on 2022-04-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_virkinfo_cvr'),
    ]

    operations = [
        migrations.AddField(
            model_name='vatpastrecord',
            name='client_responsible_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
