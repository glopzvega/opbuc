# Generated by Django 2.0.4 on 2018-06-17 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20180429_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
