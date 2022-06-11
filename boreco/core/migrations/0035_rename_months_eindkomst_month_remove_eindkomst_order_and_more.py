# Generated by Django 4.0 on 2022-05-17 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_accountstatusdeficittotal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eindkomst',
            old_name='months',
            new_name='month',
        ),
        migrations.RemoveField(
            model_name='eindkomst',
            name='order',
        ),
        migrations.AddField(
            model_name='eindkomst',
            name='quarter',
            field=models.IntegerField(default=0),
        ),
    ]
