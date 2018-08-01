# Generated by Django 2.0.5 on 2018-08-01 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmam', '0002_auto_20180801_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='dmaid',
        ),
        migrations.AddField(
            model_name='station',
            name='dmaid',
            field=models.ManyToManyField(to='dmam.DMABaseinfo'),
        ),
    ]