# Generated by Django 2.2 on 2019-06-01 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_outwarehouse_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='inwarehouse',
            name='person_liable',
            field=models.CharField(default='未指定', max_length=128, verbose_name='负责人'),
        ),
        migrations.AddField(
            model_name='outwarehouse',
            name='person_liable',
            field=models.CharField(default='未指定', max_length=128, verbose_name='负责人'),
        ),
    ]