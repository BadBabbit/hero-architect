# Generated by Django 5.0.1 on 2024-03-15 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_creation', '0011_remove_character_cantrips'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='size',
            field=models.CharField(choices=[('T', 'Tiny'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('H', 'Huge'), ('G', 'Gargantuan')], default='M', max_length=1),
        ),
    ]
