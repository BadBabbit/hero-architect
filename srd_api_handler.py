import requests
import logging
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import django


logger = logging.getLogger(__name__)

def extract_indexes(response):
    indexes = []
    for r in response["results"]:
        indexes.append(r["index"])
    return indexes

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

def main():
    create_skills()

if __name__ == "__main__":

    django.setup()
    from character_creation.models import *

    main()