# Generated by Django 2.2.4 on 2020-05-07 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0010_auto_20200507_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='numero',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
