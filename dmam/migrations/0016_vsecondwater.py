# Generated by Django 2.0 on 2018-12-14 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entm', '0005_organizations_organlevel'),
        ('dmam', '0015_vpressure'),
    ]

    operations = [
        migrations.CreateModel(
            name='VSecondWater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='Name', max_length=64, null=True)),
                ('serialnumber', models.CharField(blank=True, db_column='SerialNumber', max_length=30, null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=30, null=True)),
                ('version', models.CharField(blank=True, db_column='version', max_length=30, null=True)),
                ('manufacturer', models.CharField(blank=True, db_column='Manufacturer', max_length=30, null=True)),
                ('lng', models.CharField(blank=True, db_column='Lng', max_length=30, null=True)),
                ('lat', models.CharField(blank=True, db_column='Lat', max_length=30, null=True)),
                ('coortype', models.CharField(blank=True, db_column='CoorType', max_length=30, null=True)),
                ('product_date', models.CharField(blank=True, db_column='product date', max_length=64, null=True)),
                ('artist', models.CharField(blank=True, db_column='artist', max_length=64, null=True)),
                ('artistPreview', models.CharField(blank=True, db_column='artistPreview', max_length=256, null=True)),
                ('belongto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entm.Organizations')),
            ],
            options={
                'db_table': 'vsecondwater',
                'managed': True,
            },
        ),
    ]
