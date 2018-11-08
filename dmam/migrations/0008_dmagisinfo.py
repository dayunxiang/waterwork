# Generated by Django 2.0 on 2018-11-05 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmam', '0007_auto_20181101_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='DmaGisinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dma_no', models.CharField(max_length=50, unique=True, verbose_name='分区编号')),
                ('polygonpath', models.TextField(blank=True)),
                ('strokeColor', models.CharField(blank=True, max_length=100, null=True)),
                ('fillColor', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'dmagisinfo',
                'managed': True,
            },
        ),
    ]