# Generated by Django 2.0.5 on 2018-07-05 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='accounts.MyRoles', verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='user',
            name='belongto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='entm.Organizations', verbose_name='所属组织'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='expire_date',
            field=models.CharField(blank=True, max_length=30, verbose_name='授权截止日期'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='启停状态'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, verbose_name='手机'),
        ),
        migrations.AlterField(
            model_name='user',
            name='real_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='真实姓名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, max_length=30, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=30, unique=True, verbose_name='用户名'),
        ),
    ]