# Generated by Django 5.0.7 on 2024-10-17 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controle_uni', '0009_tsmyeucolaboradores_candidato'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tsmyeuarquivo',
            old_name='id_aquivo',
            new_name='id_arquivo',
        ),
    ]
