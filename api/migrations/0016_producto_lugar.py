# Generated by Django 2.0.4 on 2018-04-25 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_producto_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='lugar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Lugar'),
        ),
    ]
