# Generated by Django 2.0.4 on 2019-04-29 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_order_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invitados',
            field=models.IntegerField(default=1),
        ),
    ]