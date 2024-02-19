# Generated by Django 5.0.2 on 2024-02-19 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Codigosri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_factura_desde', models.CharField(max_length=9)),
                ('numero_factura_hasta', models.CharField(max_length=9)),
            ],
            options={
                'db_table': 'codigosri',
                'managed': False,
            },
        ),
    ]
