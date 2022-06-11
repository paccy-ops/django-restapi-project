# Generated by Django 4.0 on 2022-05-17 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_accountstatusdeficit'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountStatusDeficitTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cvr', models.CharField(db_index=True, max_length=255)),
                ('total', models.CharField(db_index=True, max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'accountStatusDeficitTotal',
                'ordering': ('created_at',),
            },
        ),
    ]