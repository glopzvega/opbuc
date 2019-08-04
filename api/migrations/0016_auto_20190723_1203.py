# Generated by Django 2.0.4 on 2019-07-23 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_category_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status_entrega',
            field=models.CharField(choices=[('draft', 'Pendiente'), ('open', 'En Proceso'), ('done', 'Entregada'), ('cancel', 'Cancelada')], default='draft', max_length=255),
        ),
    ]