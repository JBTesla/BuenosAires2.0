# Generated by Django 4.1.9 on 2023-05-24 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Historial_Compra',
            fields=[
                ('id_historic', models.IntegerField(primary_key=True, serialize=False)),
                ('usuario', models.IntegerField()),
                ('fecha_compra', models.DateField(auto_now_add=True)),
                ('estado_despacho', models.CharField(max_length=500)),
                ('total', models.IntegerField()),
            ],
            options={
                'db_table': 'db.Historial_Compra',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('Id_Producto', models.IntegerField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=50)),
                ('Stock', models.IntegerField()),
                ('Descripcion', models.TextField()),
                ('Imagen', models.ImageField(upload_to='')),
                ('Precio', models.IntegerField()),
            ],
            options={
                'db_table': 'db.Producto',
            },
        ),
        migrations.CreateModel(
            name='Tipo_Producto',
            fields=[
                ('Id_Tipo_Producto', models.IntegerField(primary_key=True, serialize=False)),
                ('Tipo_Producto', models.CharField(max_length=50)),
                ('Descripcion', models.TextField()),
            ],
            options={
                'db_table': 'db.Tipo_Producto',
            },
        ),
        migrations.CreateModel(
            name='Solicitud_Servicio',
            fields=[
                ('Id_solicitud', models.IntegerField(primary_key=True, serialize=False)),
                ('usuario', models.IntegerField()),
                ('Descripcion', models.TextField()),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_servicio', models.DateField()),
                ('Producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
            options={
                'db_table': 'db.Solicitud_Servicio',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='Tipo_Producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tipo_producto'),
        ),
        migrations.CreateModel(
            name='items_carrito',
            fields=[
                ('id_carrito', models.IntegerField(primary_key=True, serialize=False)),
                ('usuario', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('total', models.IntegerField()),
                ('productos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Historial_Servicio',
            fields=[
                ('id_historic2', models.IntegerField(primary_key=True, serialize=False)),
                ('usuario', models.IntegerField()),
                ('fecha_solicitud', models.DateField(auto_now_add=True)),
                ('estado', models.CharField(max_length=30)),
                ('fecha_modificacion', models.DateField(auto_now=True)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.solicitud_servicio')),
            ],
            options={
                'db_table': 'db.Historial_Servicio',
            },
        ),
        migrations.CreateModel(
            name='Boleta_Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('id_compra', models.IntegerField()),
                ('productos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
            options={
                'db_table': 'db.Boleta_Compra',
            },
        ),
    ]