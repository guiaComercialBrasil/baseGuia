# Generated by Django 2.2.4 on 2020-06-01 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0015_impulsionamento_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatoestabelecimento',
            name='alcance_nacional',
            field=models.BooleanField(default=False),
        ),
    ]
