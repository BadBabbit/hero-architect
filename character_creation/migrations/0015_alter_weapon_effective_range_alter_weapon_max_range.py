# Generated by Django 5.0 on 2024-02-01 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_creation', '0014_remove_armour_description_alter_armour_ac_dex_bonus_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weapon',
            name='effective_range',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='max_range',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]