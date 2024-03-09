# Generated by Django 5.0.3 on 2024-03-09 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pagos',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tipopago', models.CharField(choices=[('H', 'H'), ('S', 'S'), ('T', 'T'), ('M', 'M')], max_length=1)),
                ('horadepago', models.DateTimeField()),
            ],
            options={
                'db_table': 'pagos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PagosEfectivo',
            fields=[
                ('id_pagoefectivo', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('X', 'X'), ('P', 'P')], max_length=1)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=9)),
                ('cantidadentregada', models.DecimalField(db_column='cantidadentregada', decimal_places=2, max_digits=9)),
                ('cambioeentregado', models.DecimalField(db_column='cambioeentregado', decimal_places=2, max_digits=9)),
                ('hora_de_pago', models.DateTimeField()),
            ],
            options={
                'db_table': 'pagosefectivo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PagosPasarela',
            fields=[
                ('id_pagopasarela', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('E', 'E'), ('C', 'C')], max_length=1)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=9)),
                ('hora_de_pago', models.DateTimeField()),
                ('codigo_unico', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'pagospasarela',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PagosTransferencia',
            fields=[
                ('id_pagotransferencia', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('E', 'E'), ('C', 'C')], max_length=1)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=9)),
                ('hora_de_pago', models.DateTimeField()),
                ('comprobante', models.BinaryField()),
                ('hora_confirmacion_pago', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'pagostransferencia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id_periodo', models.AutoField(primary_key=True, serialize=False)),
                ('rol', models.CharField(choices=[('X', 'X'), ('M', 'M'), ('D', 'D')], max_length=1)),
                ('desde', models.DateTimeField()),
                ('hasta', models.DateTimeField()),
            ],
            options={
                'db_table': 'periodo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tipopago',
            fields=[
                ('id_tipopago', models.AutoField(primary_key=True, serialize=False)),
                ('rol', models.CharField(choices=[('X', 'X'), ('M', 'M'), ('D', 'D')], max_length=1)),
                ('tipo_pago', models.CharField(choices=[('H', 'H'), ('S', 'S'), ('T', 'T'), ('M', 'M')], db_column='tipopago', max_length=1)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'db_table': 'tipopago',
                'managed': False,
            },
        ),
    ]
