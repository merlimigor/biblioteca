# Generated by Django 5.1.2 on 2024-11-03 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(choices=[('membro', 'Membro')], default='membro', max_length=50),
        ),
    ]
