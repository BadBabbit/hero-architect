from django.db import models
from accounts.models import HA_User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from polymorphic.models import PolymorphicModel


def validate_mod_five(value):
    if value % 5 != 0:
        raise ValidationError(str(value) + " is not valid; input must be a multiple of 5.")


class Sizes:
    SIZE_CHOICES = {
        "T": "Tiny",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
        "H": "Huge",
        "G": "Gargantuan"
    }

    @staticmethod
    def get_size_choices():
        return Sizes.SIZE_CHOICES


class Dice():
    DICE = {
        "D004": "d4",
        "D006": "d6",
        "D008": "d8",
        "D010": "d10",
        "D012": "d12",
        "D020": "d20",
        "D100": "d100"
    }

    @staticmethod
    def get_dice():
        return Dice.DICE


class DamageTypes:
    DAMAGE_TYPES = {
        "FI": "fire",
        "BL": "bludgeoning",
        "RA": "radiant",
        "NE": "necrotic",
        "PS": "psychic",
        "CO": "cold",
        "FO": "force",
        "EL": "elemental",
        "LI": "lightning",
        "PI": "piercing",
        "TH": "thunder",
        "AC": "acid",
        "PO": "poison",
        "SL": "slashing",
        "PH": "physical"
    }

    @staticmethod
    def get_types():
        return DamageTypes.DAMAGE_TYPES


class EquipmentTypes:
    EQUIPMENT_TYPES = {
        "ADG": "Adventuring Gear",
        "AMM": "Ammunition",
        "AFO": "Arcane Foci",
        "ARM": "Armour",
        "ART": "Artisan's Tools",
        "DFO": "Druidic Foci",
        "EQP": "Equipment Packs",
        "GSE": "Gaming Sets",
        "HAR": "Heavy Armour",
        "HSY": "Holy Symbols",
        "KIT": "Kits",
        "LVH": "Land Vehicles",
        "LAR": "Light Armour",
        "MMW": "Martial Melee Weapons",
        "MRW": "Martial Ranged Weapons",
        "MWE": "Martial Weapons",
        "MAR": "Medium Armour",
        "MEW": "Melee Weapons",
        "MOA": "Mounts and other Animals",
        "MAV": "Mounts and Vehicles",
        "MIS": "Musical Instruments",
        "OTL": "Other Tools",
        "POT": "Potion",
        "RWE": "Ranged Weapons",
        "RNG": "Ring",
        "ROD": "Rod",
        "SCR": "Scroll",
        "SHI": "Shields",
        "SMW": "Simple Melee Weapons",
        "SRW": "Simple Ranged Weapons",
        "SWE": "Simple Weapons",
        "STA": "Staff",
        "STG": "Standard Gear",
        "THD": "Tack, Harness, and Drawn Vehichles",
        "TOO": "Tools",
        "WND": "Wand",
        "WBV": "Waterborne Vehicles",
        "WPN": "Weapon",
        "WDI": "Wondrous Items"
    }

    @staticmethod
    def get_equipment_types():
        return EquipmentTypes.EQUIPMENT_TYPES


class Ability(models.Model):
    name = models.CharField(unique=True)
    abbreviation = models.CharField(max_length=3)
    description = models.CharField()

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(unique=True)
    desc = models.TextField(default="")
    ability = models.ForeignKey(Ability, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class SavingThrow(models.Model):
    name = models.CharField(unique=True)
    ability = models.ForeignKey(Ability, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class SkillProficiency(models.Model):
    name = models.CharField(unique=True)
    skill = models.ForeignKey(Skill, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class SavingThrowProficiency(models.Model):
    name = models.CharField(unique=True)
    saving_throw = models.ForeignKey(SavingThrow, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class AbilityScoreBonus(models.Model):
    ability = models.ForeignKey(Ability, on_delete=models.RESTRICT)
    bonus = models.PositiveSmallIntegerField(default=1, blank=False, null=False)

    def __str__(self):
        return self.ability.name + " " + str(self.bonus)


class Proficiency(PolymorphicModel):
    proficiency_name = models.CharField()
    description = models.TextField()


class ProficiencyOption(models.Model):
    """Model that describes one option from a choice that a player may make. Can contain references to items, skill
    proficiencies, languages, ability score increases, and more."""
    proficiency = models.ManyToManyField(Proficiency, help_text="description of the contents of this option")


class ProficiencyChoice(models.Model):
    """Model that descibes a choice between proficiencies which a player may have to make. For example, players choosing
     to make a Dwarf character must choose between proficiency in smith's tools, brewer's supplies, or masons's tools."""
    desc = models.TextField(help_text="description of the choice to be made")
    options = models.ManyToManyField(ProficiencyOption)


class Language(models.Model):
    STANDARD = "S"
    EXOTIC = "E"
    type_choices = {
        STANDARD: "Standard",
        EXOTIC: "Exotic"
    }

    name = models.CharField(null=False, default="ERR_NO_NAME", unique=True)
    type = models.CharField(choices=type_choices)
    typical_speakers = models.CharField(default="")
    script = models.CharField(default="")

    def __str__(self):
        return self.name


class LanguageChoice(models.Model):
    description = models.CharField()
    language_option = models.ManyToManyField(Language)


class Trait(models.Model):
    """
    Traits pertain exclusively to races and subraces; they do not apply to classes or backgrounds.

    Traits have a m2m relationship with races and subraces; one such example of this is Darkvision, which is a trait
    held by most races.
    """
    name = models.CharField(unique=True)
    desc = models.TextField()

    def __str__(self):
        return self.name


class Race(models.Model):
    """Model that describes how races are stored in the database."""
    name = models.CharField(unique=True)
    size = models.CharField(max_length=1, choices=Sizes.get_size_choices())
    size_desc = models.TextField(default="")
    ability_score_bonuses = models.ManyToManyField(AbilityScoreBonus)
    alignment_desc = models.TextField(default="")
    speed_walking = models.PositiveSmallIntegerField(validators=[validate_mod_five], default=30)
    speed_flying = models.PositiveSmallIntegerField(validators=[validate_mod_five], default=0)
    speed_burrowing = models.PositiveSmallIntegerField(validators=[validate_mod_five], default=0)
    speed_swimming = models.PositiveSmallIntegerField(validators=[validate_mod_five], default=0)
    speed_climbing = models.PositiveSmallIntegerField(validators=[validate_mod_five], default=0)
    age_desc = models.CharField()
    traits = models.ManyToManyField(Trait, blank=True)
    starting_proficiencies = models.ManyToManyField(Proficiency, blank=True)
    languages = models.ManyToManyField(Language)
    language_desc = models.TextField(default="")

    def __str__(self):
        return self.name


class Subrace(models.Model):
    name = models.CharField(unique=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    desc = models.TextField(blank=True, default="")
    ability_score_bonuses = models.ManyToManyField(AbilityScoreBonus)
    traits = models.ManyToManyField(Trait, blank=True)
    starting_proficiencies = models.ManyToManyField(Proficiency, blank=True)
    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    """Model that describes how player character information is stored. Many-to-one relationship with User. A character
    can belong to many classes (through multi-classing)."""
    dice_choices = Dice.get_dice()
    damage_type_choices = DamageTypes.get_types()
    size_choices = Sizes.get_size_choices()

    # Core information
    user = models.ForeignKey(HA_User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, blank=True, default="")
    character_class_and_level = models.CharField(blank=True, default="")
    character_class = models.CharField(default="")
    inventory = models.TextField(blank=True, default="")
    race = models.ForeignKey(Race, on_delete=models.RESTRICT)
    subrace = models.ForeignKey(Subrace, on_delete=models.RESTRICT, null=True)

    # Ability scores, modifiers, and saving throws
    str_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], default=1)
    str_mod = models.SmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)], default=0)
    str_save = models.BooleanField(default=False)
    dex_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], default=1)
    dex_mod = models.SmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)], default=0)
    dex_save = models.BooleanField(default=False)
    con_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], default=1)
    con_mod = models.SmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)], default=0)
    con_save = models.BooleanField(default=False)
    int_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], default=1)
    int_mod = models.SmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)], default=0)
    int_save = models.BooleanField(default=False)
    wis_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], default=1)
    wis_mod = models.SmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)], default=0)
    wis_save = models.BooleanField(default=False)
    cha_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], default=1)
    cha_mod = models.SmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)], default=0)
    cha_save = models.BooleanField(default=False)

    # Skills
    proficiency_bonus = models.SmallIntegerField(default=2)

    acrobatics_prof = models.BooleanField(default=False)
    acrobatics_exp = models.BooleanField(default=False)

    animal_handling_prof = models.BooleanField(default=False)
    animal_handling_exp = models.BooleanField(default=False)

    arcana_prof = models.BooleanField(default=False)
    arcana_exp = models.BooleanField(default=False)

    athletics_prof = models.BooleanField(default=False)
    athletics_exp = models.BooleanField(default=False)

    deception_prof = models.BooleanField(default=False)
    deception_exp = models.BooleanField(default=False)

    history_prof = models.BooleanField(default=False)
    history_exp = models.BooleanField(default=False)

    insight_prof = models.BooleanField(default=False)
    insight_exp = models.BooleanField(default=False)

    intimidation_prof = models.BooleanField(default=False)
    intimidation_exp = models.BooleanField(default=False)

    investigation_prof = models.BooleanField(default=False)
    investigation_exp = models.BooleanField(default=False)

    medicine_prof = models.BooleanField(default=False)
    medicine_exp = models.BooleanField(default=False)

    nature_prof = models.BooleanField(default=False)
    nature_exp = models.BooleanField(default=False)

    perception_prof = models.BooleanField(default=False)
    perception_exp = models.BooleanField(default=False)

    performance_prof = models.BooleanField(default=False)
    performance_exp = models.BooleanField(default=False)

    persuasion_prof = models.BooleanField(default=False)
    persuasion_exp = models.BooleanField(default=False)

    religion_prof = models.BooleanField(default=False)
    religion_exp = models.BooleanField(default=False)

    sleight_of_hand_prof = models.BooleanField(default=False)
    sleight_of_hand_exp = models.BooleanField(default=False)

    stealth_prof = models.BooleanField(default=False)
    stealth_exp = models.BooleanField(default=False)

    survival_prof = models.BooleanField(default=False)
    survival_exp = models.BooleanField(default=False)

    passive_wis = models.SmallIntegerField(default=0, validators=[MinValueValidator(-30), MaxValueValidator(30)])

    # Other quantitative modifiers
    armour_class = models.PositiveSmallIntegerField(default=10)
    initiative_mod = models.SmallIntegerField(default=0)
    size = models.CharField(max_length=1, choices=size_choices, default="M")
    speed = models.PositiveSmallIntegerField(default=30)
    max_hp = models.PositiveSmallIntegerField(default=1)
    current_hp = models.SmallIntegerField(default=1)
    temp_hp = models.SmallIntegerField(default=0)
    hit_dice = models.CharField(max_length=4, choices=dice_choices, blank=True, null=True, default="")
    hit_dice_remaining_and_total = models.CharField(default="1/1")
    death_save_fails = models.SmallIntegerField(validators=[MaxValueValidator(3)], default=0)
    death_save_passes = models.SmallIntegerField(validators=[MaxValueValidator(3)], default=0)

    # Weapon attacks
    attacks = models.TextField(blank=True, null=True, default="")

    # Other proficiencies and languages
    weapons_and_armour = models.TextField(blank=True, null=True, default="")
    tools = models.TextField(blank=True, null=True, default="")
    languages = models.TextField(blank=True, null=True, default="")

    # Equipment and currency
    equipment = models.TextField(blank=True, null=True, default="")
    cp = models.SmallIntegerField(default=0)
    sp = models.SmallIntegerField(default=0)
    gp = models.SmallIntegerField(default=0)
    ep = models.SmallIntegerField(default=0)
    pp = models.SmallIntegerField(default=0)

    # Features and traits
    features_and_traits = models.TextField(blank=True, null=True, default="")

    # Descriptors
    personality_traits = models.TextField(blank=True, null=True, default="")
    ideals = models.TextField(blank=True, null=True, default="")
    bonds = models.TextField(blank=True, null=True, default="")
    flaws = models.TextField(blank=True, null=True, default="")
    alignment = models.CharField(blank=True, null=True, default="")
    age = models.CharField(blank=True, null=True, default="")
    height = models.CharField(blank=True, null=True, default="")
    weight = models.CharField(blank=True, null=True, default="")
    eyes = models.CharField(blank=True, null=True, default="")
    skin = models.CharField(blank=True, null=True, default="")
    hair = models.CharField(blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    allies_and_organisations = models.TextField(blank=True, null=True, default="")
    backstory = models.TextField(blank=True, null=True, default="")

    # Spellcasting
    spellcaster = models.BooleanField(default=False)  # Flag to represent whether spellcasting elements should be rendered
    spellcasting_ability = models.CharField(blank=True, null=True, default="")
    spell_save_dc = models.PositiveSmallIntegerField(default=0)
    spell_attack_bonus = models.SmallIntegerField(default=0)

    lvl_1_slots_total = models.SmallIntegerField(default=0)
    lvl_1_slots_expended = models.SmallIntegerField(default=0)

    lvl_2_slots_total = models.SmallIntegerField(default=0)
    lvl_2_slots_expended = models.SmallIntegerField(default=0)

    lvl_3_slots_total = models.SmallIntegerField(default=0)
    lvl_3_slots_expended = models.SmallIntegerField(default=0)

    lvl_4_slots_total = models.SmallIntegerField(default=0)
    lvl_4_slots_expended = models.SmallIntegerField(default=0)

    lvl_5_slots_total = models.SmallIntegerField(default=0)
    lvl_5_slots_expended = models.SmallIntegerField(default=0)

    lvl_6_slots_total = models.SmallIntegerField(default=0)
    lvl_6_slots_expended = models.SmallIntegerField(default=0)

    lvl_7_slots_total = models.SmallIntegerField(default=0)
    lvl_7_slots_expended = models.SmallIntegerField(default=0)

    lvl_8_slots_total = models.SmallIntegerField(default=0)
    lvl_8_slots_expended = models.SmallIntegerField(default=0)

    lvl_9_slots_total = models.SmallIntegerField(default=0)
    lvl_9_slots_expended = models.SmallIntegerField(default=0)

    # Contextual information
    conditions = models.TextField(blank=True, null=True, default="")
    boons = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return self.name


class Spell(models.Model):
    name = models.CharField(blank=True, default="", unique=True)
    desc = models.TextField(blank=True, default="")
    concentration = models.BooleanField()
    ritual = models.BooleanField()
    level = models.SmallIntegerField(default=0)
    range = models.CharField(blank=True, default="")
    casting_time = models.CharField()
    duration = models.CharField()
    components = models.CharField()

    def __str__(self):
        return self.name

class CharacterSpell(models.Model):
    # spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    spell = models.CharField(blank=False, null=False, default="")
    level = models.SmallIntegerField(default=0)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    prepared = models.BooleanField(default=False)

    def __str__(self):
        return self.character.name + ": " + self.spell


class CharacterClass(models.Model):
    """Model for representing the different class options available for player characters."""
    name = models.CharField(unique=True)

    # TODO: the rest of the class lmao


class CharacterSubclass(models.Model):
    """Model for representing subclass options."""
    name = models.CharField(unique=True)
    superclass = models.ForeignKey(CharacterClass, on_delete=models.RESTRICT)
    # TODO: the rest of the subclass teehee


class ClassInstance(models.Model):
    """Model for representing a particular instance of a class. For instance, this model may be used to store
    information about a level 14 barbarian with a subclass in path of the bezerker."""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=False, blank=False)
    class_type = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, null=False, blank=False)
    subclass_type = models.ForeignKey(CharacterSubclass, on_delete=models.CASCADE)
    class_level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])


class Feature():
    """
    Features pertain exclusively to classes and subclasses; they do not apply to races or backgrounds.
    """
    name = models.CharField(unique=True)
    desc = models.TextField()
    level = models.PositiveSmallIntegerField()
    feature_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)
    feature_subclass = models.ForeignKey(CharacterSubclass, on_delete=models.SET_NULL, null=True)


class EquipmentCategory(models.Model):
    category_name = models.CharField(unique=True)

    def __str__(self):
        return self.category_name


class Item(PolymorphicModel):
    """Abstract database model for items. There are multiple different types of items that inherit from this class, such
    as:
     - magic items;
     - tools;
     - and armour.
    Weapons are implemented in their own base class separate from Items due to the multiple inheritance required for the
    various weapon classes
    """

    COPPER = "CP"
    SILVER = "SP"
    GOLD = "GP"
    COST_UNIT_CHOICES = {
        COPPER: "Copper",
        SILVER: "Silver",
        GOLD: "Gold"
    }
    name = models.CharField(unique=True)
    cost_value = models.PositiveSmallIntegerField(default=1)
    cost_unit = models.CharField(default="CP", choices=COST_UNIT_CHOICES)
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.name


class Armour(Item):
    LIGHT = "L"
    MEDIUM = "M"
    HEAVY = "H"
    SHIELD = "S"
    ARMOUR_TYPE_CHOICES = {
        LIGHT: "Light",
        MEDIUM: "Medium",
        HEAVY: "Heavy",
        SHIELD: "Shield"
    }

    armour_type = models.CharField(max_length=1, choices=ARMOUR_TYPE_CHOICES)
    strength_requirement = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(30)]
    )
    ac = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    ac_dex_bonus = models.BooleanField(default=False)
    ac_dex_bonus_max = models.SmallIntegerField(default=0)
    stealth_disadvantage = models.BooleanField(default=False)
    weight = models.CharField(max_length=5, default="", help_text="weight of the armour, measured in pounds (lbs).")


class ArmourProficiency(Proficiency):
    armour = models.ForeignKey(Armour, on_delete=models.CASCADE)


class Weapon(Item):
    dice_choices = Dice.get_dice()
    damage_type_choices = DamageTypes.get_types()

    damage_dice = models.CharField(max_length=4, choices=dice_choices, blank=True, null=True, default="")
    num_dice = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    damage_type = models.CharField(choices=damage_type_choices, blank=True, null=True, default="")
    martial = models.BooleanField(default=False)
    two_handed = models.BooleanField(default=False)
    is_heavy = models.BooleanField(default=False)
    is_light = models.BooleanField(default=False)
    has_reach = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False)
    special_desc = models.TextField(default="")
    versatile = models.BooleanField(default=False)
    versatile_damage_dice = models.CharField(max_length=4, choices=dice_choices, blank=True, null=True, default="")
    is_finesse = models.BooleanField(default=False)
    thrown = models.BooleanField(default=False)
    effective_range = models.SmallIntegerField(blank=True, null=True)
    max_range = models.SmallIntegerField(blank=True, null=True)
    requires_ammunition = models.BooleanField(default=False)
    requires_loading = models.BooleanField(default=False)


class WeaponProficiency(Proficiency):
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)


class AdventuringGear(Item):
    description = models.TextField(default="")


class Tool(Item):
    description = models.TextField(default="")
    is_artisan_tool = models.BooleanField()
    is_gaming_set = models.BooleanField()
    is_instrument = models.BooleanField()


class ToolProficiency(Proficiency):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)


class EquipmentPack(models.Model):
    name = models.CharField(max_length=32)
    cost = models.PositiveSmallIntegerField(help_text="cost in gold (gp)")
    description = models.TextField()
    items = models.ManyToManyField(
        Item,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

class Conversation(models.Model):
    user = models.OneToOneField(HA_User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, default="New Conversation")

    # Thread ID for OpenAI API
    thread_id = models.CharField(blank=True, null=False)

class Message(models.Model):
    user = models.ForeignKey(HA_User, on_delete=models.CASCADE, null=True)
    content = models.TextField(default="")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)



