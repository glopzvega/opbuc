# Generated by Django 2.0.4 on 2018-04-29 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_lugar_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='lugar',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='lugar',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]