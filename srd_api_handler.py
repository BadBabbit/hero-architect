import requests
import logging
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
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

        r=Race()

        name=response["name"]
        walk_speed=response["speed"]
        alignment=response["alignment"]
        age_desc=response["age"]

        if response["size"] == "Small":
            size = 'S'
        elif response["size"] == "Medium":
            size = 'M'
        size_desc = response["size_description"]
        language_desc = response["language_desc"]

        r.name=name
        r.speed_walking=walk_speed
        r.size=size
        r.size_desc=size_desc
        r.alignment_desc=alignment
        r.age_desc=age_desc
        r.language_desc=language_desc

        r.save()

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

    for subrace in subraces:

        url = base_url + "/" + subrace
        response = requests.request("GET", url, headers=headers, data=payload).json()

        s = Subrace()

        name = response["name"]
        desc = response["desc"]
        race = response["race"]["name"]
        r = Race.objects.get(name=race)

        s.name=name
        s.desc=desc
        s.race=r
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

def create_weapons():

    url = "https://www.dnd5eapi.co/api/equipment-categories/weapon"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }


    # weapons = extract_equipment_indexes(
    #     remove_magic_items(
    #         requests.request(
    #             "GET", url, headers=headers, data=payload
    #         ).json()
    #     )
    # )

    weapons = ["dagger"]
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

        # TODO: handle damage + damage type

        try:
            w.effective_range = weapon["range"]["normal"]
            w.max_range = weapon["range"]["long"]
        except KeyError:
            try:
                w.effective_range = weapon["thrown_range"]["normal"]
                w.max_range = weapon["thrown_range"]["long"]
            except KeyError:
                pass
                # TODO: extract property indexes from weapon["properties"]

def main():
    create_weapons()


if __name__ == "__main__":

    django.setup()
    from character_creation.models import *

    main()