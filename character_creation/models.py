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
    def get_size_choices():
        return SIZE_CHOICES

class Character(models.Model):
    """Model that describes how player character information is stored. Many-to-one relationship with User. A character
    can belong to many classes (through multi-classing)."""
    name = models.CharField(max_length=32)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    raw_stats = models.ForeignKey(RawStats, on_delete=models.CASCADE)
    character_level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])


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
    acrobatics_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    animal_handling_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    arcana_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    athletics_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    deception_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    history_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    insight_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    intimidation_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    investigation_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    medicine_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    nature_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    perception_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    performance_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    persuasion_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    religion_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    sleight_of_hand_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    stealth_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    survival_val = models.SmallIntegerField(null=true, default=null, validators=[MinValueValidator(-100), MaxValueValidator(100)])

class ClassInstance(models.Model):
    """Model for representing a particular instance of a class. For instance, this model may be used to store
    information about a level 14 barbarian with a subclass in path of the bezerker."""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=false, blank=false)
    class_type = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, null=false, blank=false)
    subclass_type = models.ForeignKey(CharacterSubclass, on_delete=models.CASCADE)
    class_level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])


class CharacterClass(models.Model):
    """Model for representing the different class options available for player characters."""
    name = models.CharField(unique=True)
    # TODO: the rest of the class lmao

class RawStats(models.Model):
    """Model for holding the raw statistical modifiers for a character's abilities."""
    strength     = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    constitution = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    dexterity    = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    wisdom       = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    intelligence = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    charisma     = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])

class Race(models.Model):
    """Model that describes how races are stored in the database."""
    name = models.CharField(unique=true)
    size = models.CharField(max_length=1, choices=sizes.get_size_choices())
    speed_walking = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    speed_flying = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    speed_burrowing = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    speed_swimming = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    speed_climbing = models.PositiveSmallIntegerField(validators=[validate_mod_five])
    desc_short = models.CharField(max_length=500) # Arbitrary limit, may need revising later
    desc_long = models.CharField()
    age_desc = models.CharField()

class ItemProficiencyChoice(models.Model):
    """Model that descibes a choice which a player may have to make between item proficiencies. For example, players
    choosing to make a Dwarf character must choose between proficiency in smith's tools, brewer's supplies, or masons's
    tools."""
    items = models.ManyToManyField(ItemProficiency)

class ItemProficiency(models.Model):
    proficiency_name = models.CharField()
    item = models.ForeignKey(Item, on_delete=CASCADE)

class Item(models.Model):
    """Abstract database model for items. There are multiple different types of items that inherit from this class, such
    as:
     - weapons
     - magic items
     - tools
    """
    name = models.CharField()
    description = models.CharField()

    class Meta:
        abstract=True
