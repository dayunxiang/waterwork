# Generated by Django 2.0 on 2018-10-18 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmam', '0003_auto_20181017_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='vcommunity',
            name='commutid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
