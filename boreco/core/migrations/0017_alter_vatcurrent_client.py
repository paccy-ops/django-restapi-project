# Generated by Django 4.0 on 2022-04-19 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_filing_deadline_vatpastrecord_filling_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vatcurrent',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.client'),
        ),
    ]