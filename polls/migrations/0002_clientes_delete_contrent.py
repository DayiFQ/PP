# Generated by Django 4.2.1 on 2023-05-25 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('No_de_orden', models.CharField(max_length=50)),
                ('Documento_identidad', models.CharField(max_length=125)),
                ('Nombre', models.CharField(max_length=125)),
                ('Apellidos', models.CharField(max_length=255)),
                ('Ciudadano', models.CharField(max_length=125)),
                ('Fecha_nacimiento', models.DateField()),
                ('Estado', models.CharField(max_length=125)),
                ('Fecha_entrada', models.DateField()),
                ('Fecha_salida', models.DateField()),
                ('Cantid_noches', models.IntegerField()),
                ('Objeto_arrendamiento', models.CharField(max_length=125)),
                ('Recibo_pago', models.IntegerField()),
                ('Info_registro', models.IntegerField()),
                ('Ingreso_arrendamiento', models.FloatField()),
                ('Ingreso_desayuno', models.FloatField()),
                ('Ingreso_almuerzo', models.FloatField()),
                ('Ingreso_total', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='contrent',
        ),
    ]