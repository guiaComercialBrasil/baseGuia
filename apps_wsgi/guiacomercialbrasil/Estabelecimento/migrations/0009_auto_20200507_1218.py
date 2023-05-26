# Generated by Django 2.2.4 on 2020-05-07 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0008_auto_20200507_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fatoestabelecimento',
            name='dados_divulgacao',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estabelecimento_dados_divulgacao', to='Estabelecimento.DadosDivulgacao'),
        ),
    ]
