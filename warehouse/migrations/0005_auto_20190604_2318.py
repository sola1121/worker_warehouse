# Generated by Django 2.2.2 on 2019-06-04 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_auto_20190601_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inwarehouse',
            name='good_id',
            field=models.CharField(db_index=True, max_length=32, verbose_name='储物编号'),
        ),
        migrations.AlterField(
            model_name='outwarehouse',
            name='good_id',
            field=models.CharField(db_index=True, max_length=32, verbose_name='储物编号'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='good_id',
            field=models.CharField(db_index=True, max_length=32, verbose_name='商品编号'),
        ),
    ]