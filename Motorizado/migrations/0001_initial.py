# Generated by Django 5.0 on 2025-02-23 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Motorizados',
            fields=[
                ('id_motorizado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=300)),
                ('apellido', models.CharField(max_length=300)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_registro', models.DateTimeField()),
                ('sestado', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'motorizados',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PedidosMotorizado',
            fields=[
                ('id_pedido_motorizado', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('fecha_aceptacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'pedidos_motorizado',
                'managed': False,
            },
        ),
    ]
