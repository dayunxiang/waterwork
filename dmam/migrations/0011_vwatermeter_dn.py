# Generated by Django 2.0 on 2018-11-20 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmam', '0010_auto_20181120_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='vwatermeter',
            name='dn',
            field=models.CharField(blank=True, db_column='Dn', max_length=30, null=True),
        ),
    ]
