# Generated by Django 4.0 on 2022-04-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_virkinfo_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virkinfo',
            name='cvr',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]