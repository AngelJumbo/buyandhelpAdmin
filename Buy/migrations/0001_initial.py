# Generated by Django 2.1.7 on 2019-08-07 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id_articulo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=10)),
                ('descrip', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ArticuloPedido',
            fields=[
                ('id_articulo_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('id_articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Articulo')),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('id_estado_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id_publicacion', models.AutoField(primary_key=True, serialize=False)),
                ('id_articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Articulo')),
            ],
        ),
        migrations.CreateModel(
            name='PuntuacionVendedor',
            fields=[
                ('id_asignacion', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id_tipo_pago', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('cedula', models.CharField(max_length=10)),
                ('contrasenia', models.CharField(max_length=20)),
                ('nombres', models.CharField(max_length=20)),
                ('apellidos', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=40)),
                ('id_rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Rol')),
            ],
        ),
        migrations.AddField(
            model_name='puntuacionvendedor',
            name='id_comprador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='comprador', to='Buy.Usuario'),
        ),
        migrations.AddField(
            model_name='puntuacionvendedor',
            name='id_vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendedor', to='Buy.Usuario'),
        ),
        migrations.AddField(
            model_name='publicacion',
            name='id_vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Usuario'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='id_comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Usuario'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='id_estado_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.EstadoPedido'),
        ),
        migrations.AddField(
            model_name='pago',
            name='id_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Pedido'),
        ),
        migrations.AddField(
            model_name='pago',
            name='id_tipo_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.TipoPago'),
        ),
        migrations.AddField(
            model_name='articulopedido',
            name='id_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Pedido'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='id_categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Categoria'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buy.Usuario'),
        ),
    ]
