# Generated by Django 2.0.4 on 2019-08-01 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_cobro_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cobro',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]