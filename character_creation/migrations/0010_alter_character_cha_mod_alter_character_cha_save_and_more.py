# Generated by Django 5.0.1 on 2024-03-12 13:53

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_creation', '0009_spell_character_acrobatics_prof_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='cha_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='cha_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='con_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='con_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='dex_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='dex_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='int_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='int_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='str_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='str_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='subrace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='character_creation.subrace'),
        ),
        migrations.AlterField(
            model_name='character',
            name='wis_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='wis_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
    ]