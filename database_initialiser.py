import requests
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
import django


logger = logging.getLogger(__name__)

def extract_equipment_indexes(response):
    print(response)
    indexes = []
    for r in response:
        indexes.append(r["index"])
    return indexes

def extract_indexes(response):
    indexes = []
    for r in response["results"]:
        indexes.append(r["index"])
    return indexes

def is_magic_item(item):
    return True if "magic-item" in item["url"] else False

def remove_magic_items(response):
    non_magic_items = []
    for r in response["equipment"]:
        if not is_magic_item(r):
            non_magic_items.append(r)
    return non_magic_items

def extract_names(response):
    names = []
    for r in response:
        names.append(r["name"])
    return names

def get_unique_instances_of_field(base_url, indexes, field):
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    field_instances = []
    count = 0
    num_indexes = len(indexes)

    for index in indexes:
        url = base_url + "/" + index
        response = requests.request("GET", url, headers=headers, data=payload).json()

        count += 1

        print(f"{count} / {num_indexes} retrieved")

        if response[field] not in field_instances:
            field_instances.append(response[field])

    return field_instances

def create_races():
    """
    NOTE TO SELF: this does not embue races with starting proficiencies or traits.
    """

    base_url = "https://www.dnd5eapi.co/api/races"

    payload = {}
    headers = {
      'Accept': 'application/json'
    }

    races = extract_indexes(requests.request("GET", base_url, headers=headers, data=payload).json())

    for race in races:
        url = base_url + "/" + race
        response = requests.request("GET", url, headers=headers, data=payload).json()

        r = Race()
        try:
            r.save()

            name = response["name"]
            walk_speed = response["speed"]
            alignment = response["alignment"]
            age_desc = response["age"]

            if response["size"] == "Small":
                size = 'S'
            elif response["size"] == "Medium":
                size = 'M'
            size_desc = response["size_description"]
            language_desc = response["language_desc"]

            r.name = name
            r.speed_walking = walk_speed
            r.size = size
            r.size_desc = size_desc
            r.alignment_desc = alignment
            r.age_desc = age_desc
            r.language_desc = language_desc

            for bonus in response["ability_bonuses"]:
                ability_str = bonus["ability_score"]["name"]
                print(f"ability str = {ability_str}")
                score_increase = bonus["bonus"]
                print(f"bonus = {score_increase}")
                try:
                    abs = AbilityScoreBonus.objects.filter(ability__abbreviation=ability_str).filter(bonus=score_increase).get()
                except ObjectDoesNotExist:
                    ability = Ability.objects.get(abbreviation=ability_str)
                    asb = AbilityScoreBonus(bonus=score_increase)
                    asb.ability = ability
                    print("creating ability score")
                    asb.save()
                print(f"adding ability score for {name}")
                r.ability_score_bonuses.add(abs)

            languages = response["languages"]
            for language in languages:
                l = Language.objects.filter(name=language["name"]).get()
                r.languages.add(l)

            r.save()

        except IntegrityError:
            try:
                r.delete()
            except ValueError:
                pass
            continue

def create_subraces():
    """
    NOTE TO SELF: this does not embue subraces with starting proficiencies or traits.
    """

    base_url = "https://www.dnd5eapi.co/api/subraces"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    subraces = extract_indexes(requests.request("GET", base_url, headers=headers, data=payload).json())
    print(subraces)

    for subrace in subraces:

        url = base_url + "/" + subrace
        response = requests.request("GET", url, headers=headers, data=payload).json()

        s = Subrace()
        try:

            name = response["name"]
            print(name)
            desc = response["desc"]
            race = response["race"]["name"]
            r = Race.objects.get(name=race)

            s.name = name
            s.desc = desc
            s.race = r

            s.save()

            for bonus in response["ability_bonuses"]:
                ability_str = bonus["ability_score"]["name"]
                print(f"ability str = {ability_str}")
                score_increase = bonus["bonus"]
                print(f"bonus = {score_increase}")
                try:
                    abs = AbilityScoreBonus.objects.filter(ability__abbreviation=ability_str).filter(bonus=score_increase).get()
                except ObjectDoesNotExist:
                    ability = Ability.objects.get(abbreviation=ability_str)
                    asb = AbilityScoreBonus(bonus=score_increase)
                    asb.ability = ability
                    print("creating ability score")
                    asb.save()
                print(f"adding ability score for {name}")
                s.ability_score_bonuses.add(abs)

            languages = response["languages"]
            for language in languages:
                l = Language.objects.filter(name=language["name"]).get()
                s.languages.add(l)

            s.save()

        except IntegrityError:
            print("INTEGRITY ERROR")
            try:
                s.delete()
            except ValueError:
                pass
            continue

def create_languages():
    base_url = "https://www.dnd5eapi.co/api/languages"

    payload = {}
    headers = {
      'Accept': 'application/json'
    }

    url = base_url

    languages = extract_indexes(requests.request("GET", url, headers=headers, data=payload).json())

    for language in languages:
        url = base_url + "/" + language
        language_response = requests.request("GET", url, headers=headers, data=payload).json()

        name = language_response["name"]
        type_string = language_response["type"]
        if type_string == "Standard":
            type = 'S'
        else:
            type = 'E'

        typical_speakers = ", ".join(language_response["typical_speakers"])
        print(language)
        try:
            script = language_response["script"]
        except KeyError:
            script = "No script"

        l = Language(name=name, type=type, typical_speakers=typical_speakers, script=script)
        l.save()

def create_traits():

    base_url = "https://www.dnd5eapi.co/api/traits"

    payload = {}
    headers = {
      'Accept': 'application/json'
    }

    url = base_url

    traits = extract_indexes(requests.request("GET", url, headers=headers, data=payload).json())

    for trait in traits:
        url = base_url + "/" + trait

        trait_response = requests.request("GET", url, headers=headers, data=payload).json()

        name = trait_response["name"]
        desc_list = trait_response["desc"]
        desc = "\n\n".join(desc_list)

        t = Trait(name=name, desc=desc)
        t.save()

def add_traits_to_races_and_subraces():

    base_url = "https://www.dnd5eapi.co/api/traits"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    url = base_url

    traits = extract_indexes(requests.request("GET", url, headers=headers, data=payload).json())

    for trait in traits:

        url = base_url + "/" + trait
        response = requests.request("GET", url, headers=headers, data=payload).json()

        t = Trait.objects.get(name=response["name"])

        races = extract_names(response["races"])
        for race in races:
            r = Race.objects.get(name=race)
            r.traits.add(t)
            r.save()

        subraces = extract_names(response["subraces"])
        for subrace in subraces:
            s = Subrace.objects.get(name=subrace)
            s.traits.add(t)
            s.save()


def create_skills():

    base_url = "https://www.dnd5eapi.co/api/skills"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    url = base_url

    skills = extract_indexes(requests.request("GET", url, headers=headers, data=payload).json())

    for skill in skills:

        url = base_url + "/" + skill
        response = requests.request("GET", url, headers=headers, data=payload).json()

        s = Skill()

        name = response["name"]
        desc = response["desc"][0]
        if len(response["desc"]) > 1:
            raise Exception
        ability = response["ability_score"]["name"]
        a = Ability.objects.get(abbreviation=ability)

        s.name=name
        s.desc=desc
        s.ability=a
        s.save()


def create_armour():
    # TODO: Make armour entries in the db conform with CP/SP/GP cost unit constraints and L/M/H/S type constraints

    base_url = "https://www.dnd5eapi.co/api/equipment-categories/armor"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    url = base_url

    armours = extract_equipment_indexes(requests.request("GET", url, headers=headers, data=payload).json()["equipment"])

    for armour in armours:
        print(f"adding {armour}...")
        url = "https://www.dnd5eapi.co/api/equipment/" + armour
        response = requests.request("GET", url, headers=headers, data=payload).json()

        if is_magic_item(response):
            continue

        a = Armour()

        name = response["name"]
        armour_type = response["armor_category"]
        ac = response["armor_class"]["base"]
        dex_bonus = response["armor_class"]["dex_bonus"]
        try:
            max_bonus = response["armor_class"]["max_bonus"]
        except KeyError:
            pass
        stren_min = response["str_minimum"]
        stealth_dis = response["stealth_disadvantage"]
        weight = response["weight"]
        cost_quantity = response["cost"]["quantity"]
        cost_unit = response["cost"]["unit"]

        a.name = name
        a.armor_type = armour_type
        a.ac = ac
        a.ac_dex_bonus = dex_bonus
        try:
            a.ac_dex_bonus_max = max_bonus
        except UnboundLocalError:
            if dex_bonus:
                a.ac_dex_bonus_max = 99
            else:
                a.ac_dex_bonus_max = 0
        a.strength_requirement = stren_min
        a.stealth_disadvantage = stealth_dis
        a.weight = weight
        a.cost_value = cost_quantity
        a.cost_unit = cost_unit
        a.equipment_category = EquipmentCategory.objects.get(category_name="Armour")

        a.save()

def parse_dice_notation(dice_notation):
    d_list = dice_notation.split('d')

    # Handles constant values
    if len(d_list) == 1:
        return [d_list[0]]
    return [d_list[0], f'D{int(d_list[1]):03d}']  # formats sides as an int, and then forces a width of three by padding with 0s

def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def create_weapons():

    url = "https://www.dnd5eapi.co/api/equipment-categories/weapon"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    weapons = extract_equipment_indexes(
        remove_magic_items(
            requests.request(
                "GET", url, headers=headers, data=payload
            ).json()
        )
    )

    # weapons = ["quarterstaff"]

    weapon_category = EquipmentCategory.objects.get(category_name="Weapon")

    for weapon in weapons:
        print(f"adding {weapon}...")
        url = "https://www.dnd5eapi.co/api/equipment/" + weapon
        response = requests.request("GET", url, headers=headers, data=payload).json()
        print(response)

        w = Weapon()

        w.name = response["name"]
        w.desc = response["desc"]
        w.special_desc = response["special"]

        if response["weapon_category"] == "Martial":
            w.martial = True

        w.cost_value = response["cost"]["quantity"]
        w.cost_unit = response["cost"]["unit"].upper()
        w.equipment_category = weapon_category

        dice = parse_dice_notation(response["damage"]["damage_dice"])
        w.num_dice = dice[0]
        if len(dice) == 2:
            w.damage_dice = dice[1]
        else:
            w.damage_dice = None

        damage_types = DamageTypes.get_types()
        damage_type = get_key_by_value(damage_types, response["damage"]["damage_type"]["index"])
        w.damage_type = damage_type

        if "long" in response["range"]:
            w.effective_range = response["range"]["normal"]
            w.max_range = response["range"]["long"]
        elif "thrown_range" in response:
            print("thrown_range is in response")
            w.effective_range = response["thrown_range"]["normal"]
            w.max_range = response["thrown_range"]["long"]
        else:
            w.effective_range = 5
            w.max_range = 5

        for p in response["properties"]:
            p_name = p["index"]
            if p_name == "ammunition":
                w.requires_ammunition = True
            elif p_name == "finesse":
                w.is_finesse = True
            elif p_name == "heavy":
                w.is_heavy = True
            elif p_name == "light":
                w.is_light = True
            elif p_name == "loading":
                w.requires_loading = True
            elif p_name == "reach":
                w.has_reach = True
            elif p_name == "special":
                w.is_special = True
            elif p_name == "thrown":
                w.thrown = True
            elif p_name == "two-handed":
                w.two_handed = True
            elif p_name == "versatile":
                w.versatile = True
                v_dice = parse_dice_notation(response["two_handed_damage"]["damage_dice"])
                w.versatile_damage_dice = v_dice[1]

        # TODO: resolve issues with:
        # - thrown ranges
        # - damage types - probably resolved? i think it was because of the two-character limitation
        # - versatile damage dice defaulting to d4 instead of none

        w.save()

def create_spells():

    url = "https://www.dnd5eapi.co/api/spells"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    spells = extract_indexes(
        requests.request(
            "GET", url, headers=headers, data=payload
        ).json()
    )

    for spell in spells:
        print(f"adding {spell}...")
        spell_url = url + '/' + spell
        response = requests.request("GET", spell_url, headers=headers, data=payload).json()

        print(response)

        s = Spell()
        s.name = response["name"]

        desc = "\n\n".join(response["desc"])
        s.desc = desc

        s.concentration = response["concentration"]
        s.ritual = response["ritual"]
        s.level = response["level"]
        s.range = response["range"]
        s.casting_time = response["casting_time"]
        s.duration = response["duration"]
        s.components = ", ".join(response["components"])

        try:
            s.save()

        except IntegrityError:
            try:
                s.delete()
            except ValueError:
                pass
            continue

def add_ability_score_mods():

    base_url = "https://www.dnd5eapi.co/api"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    races = extract_indexes(requests.request("GET", base_url + "/races", headers=headers, data=payload).json())
    subraces = extract_indexes(requests.request("GET", base_url + "/subraces", headers=headers, data=payload).json())

    for race in races:
        url = base_url + "/races/" + race
        response = requests.request("GET", url, headers=headers, data=payload).json()
        r = Race.objects.get(name=response["name"])
        r.ability_score_bonuses.clear()
        for asb in response["ability_bonuses"]:
            asb_obj = AbilityScoreBonus.objects.filter(ability__abbreviation=asb["ability_score"]["name"]).filter(bonus=asb["bonus"]).get()
            r.ability_score_bonuses.add(asb_obj)
        r.save()

    for subrace in subraces:
        url = base_url + "/subraces/" + subrace
        response = requests.request("GET", url, headers=headers, data=payload).json()
        s = Subrace.objects.get(name=response["name"])
        s.ability_score_bonuses.clear()
        for asb in response["ability_bonuses"]:
            asb_obj = AbilityScoreBonus.objects.filter(ability__abbreviation=asb["ability_score"]["name"]).filter(bonus=asb["bonus"]).get()
            s.ability_score_bonuses.add(asb_obj)
        s.save()

def main():

    create_skills()
    create_races()
    create_subraces()
    create_traits()
    add_traits_to_races_and_subraces()
    add_ability_score_mods()
    create_spells()



if __name__ == "__main__":

    django.setup()
    from character_creation.models import *

    main()
