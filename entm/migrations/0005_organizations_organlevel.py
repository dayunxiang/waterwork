# Generated by Django 2.0 on 2018-11-29 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entm', '0004_auto_20181114_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizations',
            name='organlevel',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Level'),
        ),
    ]
