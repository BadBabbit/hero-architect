# Generated by Django 5.0 on 2024-02-02 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_creation', '0016_alter_weapon_damage_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weapon',
            name='versatile_damage_dice',
            field=models.CharField(blank=True, choices=[('D004', 'd4'), ('D006', 'd6'), ('D008', 'd8'), ('D010', 'd10'), ('D012', 'd12'), ('D020', 'd20'), ('D100', 'd100')], default='', max_length=4, null=True),
        ),
    ]