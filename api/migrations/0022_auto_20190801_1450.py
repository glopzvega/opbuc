# Generated by Django 2.0.4 on 2019-08-01 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_cobro_payment_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cobro',
            name='total',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cobro',
            name='total_porcentaje',
            field=models.FloatField(),
        ),
    ]
