# Generated by Django 3.2 on 2023-05-29 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20230529_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='objeto_arrendamiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.rooms'),
        ),
    ]
