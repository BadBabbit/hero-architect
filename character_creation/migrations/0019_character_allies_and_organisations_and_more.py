# Generated by Django 5.0.1 on 2024-03-18 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_creation', '0018_character_boons_character_conditions'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='allies_and_organisations',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
