# Generated by Django 5.0 on 2024-01-29 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_creation', '0006_remove_subrace_starting_proficiencies_subrace_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trait',
            name='races',
        ),
        migrations.RemoveField(
            model_name='trait',
            name='subraces',
        ),
        migrations.AddField(
            model_name='race',
            name='starting_proficiencies',
            field=models.ManyToManyField(blank=True, null=True, to='character_creation.proficiency'),
        ),
        migrations.AddField(
            model_name='race',
            name='traits',
            field=models.ManyToManyField(blank=True, null=True, to='character_creation.trait'),
        ),
        migrations.AddField(
            model_name='subrace',
            name='starting_proficiencies',
            field=models.ManyToManyField(blank=True, null=True, to='character_creation.proficiency'),
        ),
        migrations.AddField(
            model_name='subrace',
            name='traits',
            field=models.ManyToManyField(blank=True, null=True, to='character_creation.trait'),
        ),
    ]