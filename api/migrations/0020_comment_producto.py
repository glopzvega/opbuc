# Generated by Django 2.0.4 on 2018-04-28 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20180428_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Producto'),
        ),
    ]