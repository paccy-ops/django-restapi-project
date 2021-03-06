# Generated by Django 4.0 on 2022-04-20 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_vatcurrent_filing_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Virkinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cvr', models.CharField(max_length=255)),
                ('client_name', models.CharField(blank=True, max_length=255, null=True)),
                ('managers', models.CharField(blank=True, max_length=255, null=True)),
                ('address1', models.CharField(blank=True, max_length=255, null=True)),
                ('address2', models.CharField(blank=True, max_length=255, null=True)),
                ('postcode', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('financial_year', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.client')),
            ],
            options={
                'db_table': 'virkinfo',
                'ordering': ('created_at',),
            },
        ),
    ]
