# Generated by Django 5.0.4 on 2024-05-12 07:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0005_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='products', to='ecommerceapp.store')),
            ],
            options={
                'unique_together': {('name', 'store')},
            },
        ),
    ]