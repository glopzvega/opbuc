# Generated by Django 2.0.4 on 2018-07-08 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20180618_0209'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='like',
        ),
    ]
