# Generated by Django 5.0.7 on 2024-09-30 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_uni', '0007_tsmyeufuncao_tsmyeusetor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tsmyeusetor',
            name='cod_setor',
            field=models.CharField(max_length=13, primary_key=True, serialize=False),
        ),
    ]
