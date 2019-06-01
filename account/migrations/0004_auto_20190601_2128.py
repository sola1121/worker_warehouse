# Generated by Django 2.2 on 2019-06-01 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='action',
            field=models.CharField(choices=[('CREATE', '创建'), ('MODIFY', '修改'), ('DELETE', '删除'), ('FINISH', '完成')], max_length=16, verbose_name='用户活动描述'),
        ),
    ]
