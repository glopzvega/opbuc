# Generated by Django 2.0.4 on 2019-04-22 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_config_mensaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]