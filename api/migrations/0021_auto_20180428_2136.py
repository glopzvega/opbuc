# Generated by Django 2.0.4 on 2018-04-28 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_comment_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='producto_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Producto'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='lugar_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.Lugar'),
        ),
    ]
