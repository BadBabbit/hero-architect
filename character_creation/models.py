from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

def validate_mod_five(value):
    if value % 5 != 0:
        raise ValidationError(str(value)+" is not valid; input must be a multiple of 5.")

class sizes():
    SIZE_CHOICES = {
        "T": "Tiny",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
        "H": "Huge",
        "G": "Gargantuan"
    }
    def get_size_choices(self):
        return self.SIZE_CHOICES

class dice():
    DICE = {
        "D004": "d4",
        "D006": "d6",
        "D008": "d8",
        "D010": "d10",
        "D012": "d12",
        "D020": "d20",
        "D100": "d100"
    }

    def get_dice(self):
        return self.DICE

class damage_types():
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

    def get_types(self):
        return self.DAMAGE_TYPES

class Race(models.Model):
    """Model that describes how races are stored in the database."""
    name = models.CharField(unique=True)
    size = models.CharField(max_length=1, choices=sizes.SIZE_CHOICES)
    size_desc = models.TextField()
    speed_walking = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    speed_flying = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    speed_burrowing = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    speed_swimming = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    speed_climbing = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    desc_short = models.CharField(max_length=500) # Arbitrary limit, may need revising later
    desc_long = models.CharField()
    age_desc = models.CharField()

class Subrace(models.Model):
    name = models.CharField(unique=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)


class Trait(models.Model):
    name = models.CharField(unique=True)
    races = models.ManyToManyField(Race)
    desc = models.TextField()

class Feature():
    name = models.CharField(unique=True)

class RawStats(models.Model):
    """Model for holding the raw statistical modifiers for a character's abilities."""
    strength     = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    constitution = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    dexterity    = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    wisdom       = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    intelligence = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    charisma     = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])


class Character(models.Model):
    """Model that describes how player character information is stored. Many-to-one relationship with User. A character
    can belong to many classes (through multi-classing)."""
    name = models.CharField(max_length=32)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    raw_stats = models.ForeignKey(RawStats, on_delete=models.CASCADE)
    character_level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    inventory = models.TextField()
    race = models.ForeignKey(Race, on_delete=models.RESTRICT)
    subrace = models.ForeignKey(Subrace, on_delete=models.RESTRICT)


class CharacterProficiencies(models.Model):
    """Extends the Character model, for the purpose of not overpopulating the table with too many columns."""
    acrobatics_prof = models.BooleanField(default=False)
    animal_handling_prof = models.BooleanField(default=False)
    arcana_prof = models.BooleanField(default=False)
    athletics_prof = models.BooleanField(default=False)
    deception_prof = models.BooleanField(default=False)
    history_prof = models.BooleanField(default=False)
    insight_prof = models.BooleanField(default=False)
    intimidation_prof = models.BooleanField(default=False)
    investigation_prof = models.BooleanField(default=False)
    medicine_prof = models.BooleanField(default=False)
    nature_prof = models.BooleanField(default=False)
    perception_prof = models.BooleanField(default=False)
    performance_prof = models.BooleanField(default=False)
    persuasion_prof = models.BooleanField(default=False)
    religion_prof = models.BooleanField(default=False)
    sleight_of_hand_prof = models.BooleanField(default=False)
    stealth_prof = models.BooleanField(default=False)
    survival_prof = models.BooleanField(default=False)

class CharacterProficiencyCustomValues(models.Model):
    """Model for representing custom values for proficiencies, should the player wish to override the values for reasons
     such as magical items, features, or for fun."""
    acrobatics_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    animal_handling_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    arcana_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    athletics_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    deception_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    history_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    insight_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    intimidation_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    investigation_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    medicine_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    nature_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    perception_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    performance_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    persuasion_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    religion_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    sleight_of_hand_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    stealth_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    survival_val = models.SmallIntegerField(null=True, default=None, validators=[MinValueValidator(-100), MaxValueValidator(100)])

class CharacterClass(models.Model):
    """Model for representing the different class options available for player characters."""
    name = models.CharField(unique=True)
    # TODO: the rest of the class lmao

class CharacterSubclass(models.Model):
    """Model for representing subclass options."""
    name = models.CharField(unique=True)
    superclass = models.ForeignKey(CharacterClass)
    # TODO: the rest of the subclass teehee

class ClassInstance(models.Model):
    """Model for representing a particular instance of a class. For instance, this model may be used to store
    information about a level 14 barbarian with a subclass in path of the bezerker."""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=False, blank=False)
    class_type = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, null=False, blank=False)
    subclass_type = models.ForeignKey(CharacterSubclass, on_delete=models.CASCADE)
    class_level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])




class Choice(models.Model):
    """Model that descibes a choice which a player may have to make. For example, players choosing to make a Dwarf char-
    acter must choose between proficiency in smith's tools, brewer's supplies, or masons's tools."""
    desc    = models.TextField(help_text="description of the choice to be made")
    options = models.ManyToManyField(Option)

class Option(models.Model):
    """Model that describes one option from a choice that a player may make. Can contain references to items, profic-
    iencies, languages, ability score increases, and more."""
    items = models.ManyToManyField(models.Model, help_text="description of the contents of this option")

class Proficiency(models.Model):
    proficiency_name = models.CharField()

class ItemProficiency(Proficiency):
    item = models.ForeignKey(Item, on_delete=CASCADE)

class Item(models.Model):
    """Abstract database model for items. There are multiple different types of items that inherit from this class, such
    as:
     - weapons
     - magic items
     - tools
    """
    name = models.CharField()
    value_gold = models.PositiveIntegerField()
    value_silver = models.PositiveIntegerField()
    value_bronze = models.PositiveIntegerField()
    weight = models.CharField(max_length=5, default="", help_text="weight of the item, measured in pounds (lbs).")

    class Meta:
        abstract=True

class Armour(Item):
    LIGHT = "L"
    MEDIUM = "M"
    HEAVY = "H"
    SHIELD = "S"
    ARMOR_TYPE_CHOICES = {
        LIGHT: "Light",
        MEDIUM: "Medium",
        HEAVY: "Heavy",
        SHIELD: "Shield"
    }

    armor_type = models.CharField(max_length=1, choices=ARMOR_TYPE_CHOICES)
    description = models.TextField(default="")
    strength_requirement = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    ac = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    ac_dex_bonus = models.BooleanField()
    ac_dex_bonus_max = models.SmallIntegerField(default=0)
    stealth_disadvantage = models.BooleanField()

class Weapon(Item):
    dice_choices = dice.get_dice()
    damage_type_choices = damage_types.get_types()

    damage_dice = models.CharField(max_length=4, choices=dice_choices, blank=True, null=True, default="")
    num_dice    = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    damage_type = models.CharField(max_length=2, choices=damage_type_choices, blank=True, null=True, default="")
    martial     = models.BooleanField(default=False)
    two_handed  = models.BooleanField(default=False)
    is_heavy    = models.BooleanField(default=False)
    is_light    = models.BooleanField(default=False)
    has_reach   = models.BooleanField(default=False)
    thrown      = models.BooleanField(default=False)
    effective_range = models.PositiveSmallIntegerField(blank=True, null=True)
    max_range       = models.PositiveSmallIntegerField(blank=True, null=True)
    is_special   = models.BooleanField(default=False)
    special_desc = models.TextField()

class MeleeWeapon(Weapon):
    versatile               = models.BooleanField(default=False)
    versatile_damage_dice   = models.CharField(max_length=4, choices=dice_choices)
    is_finesse = models.BooleanField(default=False)


class RangedWeapon(Weapon):
    requires_ammunition = models.BooleanField(default=False)
    requires_loading    = models.BooleanField(default=False)

class AdventuringGear(Item):
    description = models.TextField(default="")

class Tool(Item):
    description = models.TextField(default="")
    is_artisan_tool = models.BooleanField()
    is_gaming_set = models.BooleanField()
    is_instrument = models.BooleanField()

class Container(Item):
    capacity = models.CharField(max_length=200) # arbitrary limit

class EquipmentPack(models.Model):
    name = models.CharField(max_length=32)
    cost = models.PositiveSmallIntegerField(help_text="cost in gold (gp)")
    description = models.TextField()
    items = models.ManyToManyField(Item)

class MagicItem(Item):
    COMMON = "C"
    UNCOMMON = "U"
    RARE = "R"
    VERY_RARE = "V"
    LEGENDARY = "L"
    RARITY_CHOICES = {
        COMMON: "Common",
        UNCOMMON: "Uncommon",
        RARE: "Rare",
        VERY_RARE: "Very rare",
        LEGENDARY: "Legendary"
    }
    description = models.TextField(default="")
    requires_attunement = models.BooleanField(default=True)
    rarity = models.CharField(max_length=1, choices=RARITY_CHOICES)

class MagicWeapon(MagicItem, Weapon):
    pass
class WondrousItem(MagicItem):
    pass

class Wand(MagicItem):
    pass

class MagicArmour(MagicItem, Armour):
    pass

class Language(model.Models):
    STANDARD = "S"
    EXOTIC = "E"
    type_choices = {
        STANDARD : "Standard",
        EXOTIC : "Exotic"
    }

    name = models.CharField()
    desc = models.TextField()
    type = models.CharField(choices=type_choices)
    typical_speakers = models.CharField()