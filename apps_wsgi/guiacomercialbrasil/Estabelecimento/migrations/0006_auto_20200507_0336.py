# Generated by Django 2.2.4 on 2020-05-07 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0005_auto_20200507_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fatoestabelecimento',
            name='telefone_contato_1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='fatoestabelecimento',
            name='telefone_contato_2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
