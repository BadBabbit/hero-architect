# Generated by Django 5.0.1 on 2024-03-19 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_creation', '0021_alter_characterspell_prepared_alter_spell_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spell',
            name='desc',
            field=models.TextField(blank=True, default=''),
        ),
    ]
