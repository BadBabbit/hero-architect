# Generated by Django 5.0.1 on 2024-03-12 11:51

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_creation', '0008_remove_conversation_messages_message_conversation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='')),
                ('desc', models.CharField(blank=True, default='')),
                ('concentration', models.BooleanField()),
                ('ritual', models.BooleanField()),
                ('level', models.SmallIntegerField(default=0)),
                ('range', models.CharField(blank=True, default='')),
                ('casting_time', models.CharField()),
                ('duration', models.CharField()),
                ('components', models.CharField()),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='acrobatics_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='acrobatics_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='age',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='alignment',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='animal_handling_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='animal_handling_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='arcana_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='arcana_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='armour_class',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='character',
            name='athletics_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='athletics_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='attacks',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='backstory',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='bonds',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='cantrips',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='character',
            name='cha_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(-10)]),
        ),
        migrations.AddField(
            model_name='character',
            name='cha_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(-30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='cha_score',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='character_class_and_level',
            field=models.CharField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='character',
            name='con_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(-10)]),
        ),
        migrations.AddField(
            model_name='character',
            name='con_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(-30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='con_score',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='cp',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='current_hp',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='character',
            name='death_save_fails',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AddField(
            model_name='character',
            name='death_save_passes',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AddField(
            model_name='character',
            name='deception_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='deception_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='dex_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(-10)]),
        ),
        migrations.AddField(
            model_name='character',
            name='dex_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(-30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='dex_score',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='equipment',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='eyes',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='features_and_traits',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='flaws',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='gp',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='hair',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='height',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='history_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='history_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='hit_dice',
            field=models.CharField(blank=True, choices=[('D004', 'd4'), ('D006', 'd6'), ('D008', 'd8'), ('D010', 'd10'), ('D012', 'd12'), ('D020', 'd20'), ('D100', 'd100')], default='', max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='ideals',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='initiative_mod',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='insight_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='insight_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='int_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(-10)]),
        ),
        migrations.AddField(
            model_name='character',
            name='int_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(-30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='int_score',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='intimidation_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='intimidation_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='investigation_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='investigation_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_1_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_1_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_2_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_2_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_3_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_3_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_4_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_4_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_5_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_5_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_6_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_6_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_7_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_7_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_8_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_8_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_9_slots_expended',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='lvl_9_slots_total',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='max_hp',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='character',
            name='medicine_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='medicine_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='nature_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='nature_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='passive_wis',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='perception_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='perception_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='performance_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='performance_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='personality_traits',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='persuasion_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='persuasion_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='profs_and_langs',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='religion_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='religion_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='skin',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='sleight_of_hand_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='sleight_of_hand_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='sp',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='speed',
            field=models.PositiveSmallIntegerField(default=30),
        ),
        migrations.AddField(
            model_name='character',
            name='spell_attack_bonus',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='spell_save_dc',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='spellcaster',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='spellcasting_ability',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='stealth_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='stealth_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='str_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(-10)]),
        ),
        migrations.AddField(
            model_name='character',
            name='str_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(-30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='str_score',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='survival_prof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='survival_val',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='temp_hp',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='weight',
            field=models.CharField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='wis_mod',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(-10)]),
        ),
        migrations.AddField(
            model_name='character',
            name='wis_save',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(-30)]),
        ),
        migrations.AddField(
            model_name='character',
            name='wis_score',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='character_level',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='inventory',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
        migrations.CreateModel(
            name='CharacterSpell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prepared', models.BooleanField()),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character_creation.character')),
                ('spell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character_creation.spell')),
            ],
        ),
    ]