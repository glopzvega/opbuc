# Generated by Django 2.0.4 on 2019-02-24 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190223_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='lugar',
            name='photoweb',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
