
from django.shortcuts import render, redirect
from django.db import transaction, DatabaseError, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging, time
from character_creation.openai_api_handler import openAI_api_handler as heroArchitect
from character_creation.models import *
from accounts.models import HA_User

logging.basicConfig(level=logging.INFO)
if __name__ == "__main__":
    LOGGER = logging.getLogger("general")
else:
    LOGGER = logging.getLogger(__name__)


def reverse_list(lst):

    # Uses list comprehension to efficiently return the reversed list (completes in under 1ms for
    # 100,000,000 long lists)

    start = len(lst) - 1
    return [lst[i] for i in range(start, -1, -1)]


def create_message_dict(author, content):
    message = {
        'author': author,
        'content': content
    }
    return message


def parse_dice_notation(dice_notation):
    d_list = dice_notation.split('d')

    # Handles constant values
    if len(d_list) == 1:
        return [d_list[0]]
    return [d_list[0], f'D{int(d_list[1]):03d}']  # formats sides as an int, and then forces a width of three by padding with 0s

def initialise_conversation(initialiser):
    """
    This function initialises a new conversation thread with the OpenAI API.

    :param initialiser: A string detailing whether the user or the AI is to start the conversation.
    :return t: The newly-created thread.
    """

    LOGGER.debug("Initialising thread...")
    t = heroArchitect.initialise_thread()
    LOGGER.debug(f"Thread ID: {t.id}")

    if initialiser == "ai":
        content = "Hi!"
        _ = heroArchitect.add_message_to_thread(content, t.id, role="user")
        LOGGER.debug("Getting assistant ID...")
        a = heroArchitect.ChatAssistant.get_id()
        LOGGER.debug("Running assistant...")
        r = heroArchitect.run_assistant(t.id, a)
        c = 0

        # Polls the API. Breaks the while loop when the AI has generated a response.
        while r.status != "completed":
            LOGGER.debug(f"Polling. {c * 0.5} seconds elapsed...")
            c += 1
            time.sleep(0.5)
            r = heroArchitect.retrieve_run(t, r)
            LOGGER.debug(f"r_status: {r.status}")

    return t


def add_message_to_database(user, conversation, content):
    try:
        with transaction.atomic():
            message = Message(
                content=content,
                conversation=conversation,
                user=user
            )
            message.save()

    except Exception as e:
        LOGGER.error(f"ERROR: TRANSACTION COULD NOT BE COMPLETED: {e.__str__()}")

def apply_asis(character, asis):
    for asi in asis:
        asi_ability = asi.ability.abbreviation
        LOGGER.info(f"Applying ASI: {asi_ability} +{asi.bonus}")
        if asi_ability == "STR":
            character.str_score += asi.bonus
        elif asi_ability == "DEX":
            character.dex_score += asi.bonus
        elif asi_ability == "CON":
            character.con_score += asi.bonus
        elif asi_ability == "INT":
            character.int_score += asi.bonus
        elif asi_ability == "WIS":
            character.wis_score += asi.bonus
        elif asi_ability == "CHA":
            character.cha_score += asi.bonus

def add_spells_to_char(character, spells, level):
    for spell in spells:
        char_spell = CharacterSpell(
            spell=spell,
            level=level,
            character=character
        ).save()

def retrieve_spells(c_data, spell_type):
    try:
        spells = c_data[spell_type]
    except KeyError:
        spells = []
    return spells

# view for create.html, at index /characters/create/
def create_character(request):
    context = {
        "username": "",
        "messages": [],
        "show_prompt": True,
        "show_messages": False
    }

    if request.user.is_authenticated:
        context["username"] = request.user.username

    else:
        return redirect('/auth/login/')

    if request.method == 'POST':
        data = request.POST

        context["show_prompt"] = False
        context["show_messages"] = True

        start = data.get("start")
        message = data.get("user_input")
        generate = data.get("generate")

        # Retrieve user
        try:
            user = HA_User.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            LOGGER.error(f" COULD NOT FIND USER WITH USERNAME '{request.user.username}'")
            raise ObjectDoesNotExist

        # Handles initial prompt

        if start is not None:

            t = initialise_conversation(start)

            # Check for existing conversation, delete if exists
            try:
                conversation = Conversation.objects.get(user=user)
                conversation.delete()
                # TODO: Should probably also close OpenAI thread, but idk how to do that
            except ObjectDoesNotExist:
                pass

            # Create new conversation
            conversation = Conversation(thread_id=t.id)
            conversation.user = user
            conversation.save()

            # Prompts the AI to generate a response
            if start == "ai":
                response = heroArchitect.retrieve_messages(t)
                messages = response.data
                first_msg = True
                for m in messages:
                    content = m.content[0].text.value
                    author = m.role

                    # Exclude thread initialiser message
                    if content == "Hi!" and author == "user" and first_msg == True:
                        first_msg = False
                        continue

                    first_msg = False
                    # Below should be unreachable by user messages

                    # Author can either be "user" or "assistant"

                    if author == "user":
                        LOGGER.error(" USER MESSAGE HAS REACHED QUARANTINED BLOCK")
                        print("ERROR: USER MESSAGE HAS REACHED QUARANTINED BLOCK")
                        quit()

                    # Add message to the context
                    context["messages"].append(create_message_dict(author, content))

                    # Add message to the database
                    ha = HA_User.objects.get(username="HeroArchitect")
                    add_message_to_database(ha, conversation, content)

        # Handles user message inputs
        elif message is not None or "":
            conversation = Conversation.objects.filter(user=user).get()

            # Add message to database
            add_message_to_database(user, conversation, message)

            # Add message to conversation thread
            t_id = conversation.thread_id
            thread = heroArchitect.get_thread(t_id)
            heroArchitect.add_message_to_thread(message, t_id)

            # Generate response
            a_id = heroArchitect.ChatAssistant.get_id()  # Assistant ID
            LOGGER.info("Running assistant.")
            run = heroArchitect.run_assistant(t_id, a_id)

            # Retrieve response
            heroArchitect.wait_on_run(run, thread, target_statuses=["completed", "requires_action"])
            LOGGER.info("Run complete.")
            ms = heroArchitect.retrieve_messages(thread)

            # Add messages to context
            for m in ms.data:
                # Author can either be "user" or "assistant"
                author = m.role
                content = m.content[0].text.value

                # Truncates message for logging purposes
                truncated_content = (content[:27] + '...') if len(data) > 27 else content
                LOGGER.info(f"Added message from {author}: {truncated_content}")

                context["messages"].append(create_message_dict(author, content))

            LOGGER.info("All messages successfully added to context.")

            new_message = heroArchitect.retrieve_messages(thread).data[-1].content[0].text.value
            # Add new message to database
            ha = HA_User.objects.get(username="HeroArchitect")
            add_message_to_database(ha, conversation, new_message)

        # Handles character generation
        elif generate is not None and generate == "true":
            LOGGER.info("Beginning character generation...")
            conversation = Conversation.objects.filter(user=user).get()
            t_id = conversation.thread_id

            # base_thread = "thread_5fyGd3whnK7LFcvZUknbyFtU"
            # t_id = heroArchitect.duplicate_thread(base_thread)

            LOGGER.info("Generating character data...")
            c_data = heroArchitect.generate_character_data(t_id)

            LOGGER.info("Data generated. Creating character...")

            c = Character()
            c.user = user
            LOGGER.info(f"Setting name: {c_data['name']}")
            c.name = c_data["name"]
            c.character_class = c_data["class"]
            c.character_class_and_level = "Level "+str(c_data['level']) + " " + c_data["class"]
            race = Race.objects.get(name=c_data["race"])
            c.race = race
            if c_data["subrace"] != "None":
                subrace = Subrace.objects.get(name=c_data["subrace"])
                c.subrace = subrace
            c.str_score = c_data["str-score"]
            c.dex_score = c_data["dex-score"]
            c.con_score = c_data["con-score"]
            c.int_score = c_data["int-score"]
            c.wis_score = c_data["wis-score"]
            c.cha_score = c_data["cha-score"]

            LOGGER.info("Getting Racial ASIs...")
            racial_asis = race.ability_score_bonuses.all()
            apply_asis(c, racial_asis)
            if c_data["subrace"] != "None":
                subracial_asis = c.subrace.ability_score_bonuses.all()
                apply_asis(c, subracial_asis)

            for saving_throw in c_data["saving-throw-proficiencies"]:
                if saving_throw == "strength":
                    c.str_save = True
                elif saving_throw == "dexterity":
                    c.dex_save = True
                elif saving_throw == "constitution":
                    c.con_save = True
                elif saving_throw == "intelligence":
                    c.int_save = True
                elif saving_throw == "wisdom":
                    c.wis_save = True
                elif saving_throw == "charisma":
                    c.cha_save = True

            for skill_prof in c_data["skill-proficiencies"]:
                if skill_prof == "acrobatics":
                    c.acrobatics_prof = True
                elif skill_prof == "animal_handling":
                    c.animal_handling_prof = True
                elif skill_prof == "arcana":
                    c.arcana_prof = True
                elif skill_prof == "athletics":
                    c.athletics_prof = True
                elif skill_prof == "deception":
                    c.deception_prof = True
                elif skill_prof == "history":
                    c.history_prof = True
                elif skill_prof == "insight":
                    c.insight_prof = True
                elif skill_prof == "intimidation":
                    c.intimidation_prof = True
                elif skill_prof == "investigation":
                    c.investigation_prof = True
                elif skill_prof == "medicine":
                    c.medicine_prof = True
                elif skill_prof == "nature":
                    c.nature_prof = True
                elif skill_prof == "perception":
                    c.perception_prof = True
                elif skill_prof == "persuasion":
                    c.persuasion_prof = True
                elif skill_prof == "performance":
                    c.performance_prof = True
                elif skill_prof == "religion":
                    c.religion_prof = True
                elif skill_prof == "sleight_of_hand":
                    c.sleight_of_hand_prof = True
                elif skill_prof == "stealth":
                    c.stealth_prof = True
                elif skill_prof == "survival":
                    c.survival_prof = True

            for skill_exp in c_data["skill-expertises"]:
                if skill_exp == "acrobatics":
                    c.acrobatics_prof = True
                elif skill_exp == "animal_handling":
                    c.animal_handling_prof = True
                elif skill_exp == "arcana":
                    c.arcana_prof = True
                elif skill_exp == "athletics":
                    c.athletics_prof = True
                elif skill_exp == "deception":
                    c.deception_prof = True
                elif skill_exp == "history":
                    c.history_prof = True
                elif skill_exp == "insight":
                    c.insight_prof = True
                elif skill_exp == "intimidation":
                    c.intimidation_prof = True
                elif skill_exp == "investigation":
                    c.investigation_prof = True
                elif skill_exp == "medicine":
                    c.medicine_prof = True
                elif skill_exp == "nature":
                    c.nature_prof = True
                elif skill_exp == "perception":
                    c.perception_prof = True
                elif skill_exp == "persuasion":
                    c.persuasion_prof = True
                elif skill_exp == "performance":
                    c.performance_prof = True
                elif skill_exp == "religion":
                    c.religion_prof = True
                elif skill_exp == "sleight_of_hand":
                    c.sleight_of_hand_prof = True
                elif skill_exp == "stealth":
                    c.stealth_prof = True
                elif skill_exp == "survival":
                    c.survival_prof = True

            c.weapons_and_armour = c_data["weapon-and-armour-proficiencies"]
            c.tools = c_data["tool-proficiencies"]
            c.languages = c_data["languages"]

            LOGGER.info(f"size: {c_data['size']}")
            LOGGER.info(f"speed: {c_data['speed']}")

            if c_data['size'] == "medium":
                size = 'M'
            elif c_data['size'] == "small":
                size = 'S'

            c.size = size
            c.speed = int(c_data["speed"])

            # Parses hit dice into valid database-compatible notation
            c.hit_dice = parse_dice_notation("1"+c_data["hit-dice"])[1]

            equipments = c_data["equipment"]
            for equipment in equipments:
                c.equipment += "-"+equipment+"\n"
            attacks = c_data["attacks"]
            for attack in attacks:
                c.attacks += "-"+attack+("\n")

            c.personality_traits = c_data["personality-traits"]
            c.ideals = c_data["ideals"]
            c.bonds = c_data["bonds"]
            c.flaws = c_data["flaws"]
            c.alignment = c_data["alignment"]
            c.age = c_data["age"]
            c.height = c_data["height"]
            c.eyes = c_data["eyes"]
            c.skin = c_data["skin"]
            c.hair = c_data["hair"]
            c.description = c_data["desc"]
            c.backstory = c_data["backstory"]
            c.spell_save_dc = c_data["spell-save-dc"]
            c.spell_attack_bonus = c_data["spell-attack-bonus"]

            c.features_and_traits = ""
            traits = race.traits.all()
            for t in traits:
                c.features_and_traits += t.name + ": " + t.desc + "\n\n"

            c.save()

            c.lvl_1_slots_total = c_data["1st-level-spell-slots"]
            c.lvl_1_slots_expended = c_data["1st-level-spell-slots"]

            c.lvl_2_slots_total = c_data["2nd-level-spell-slots"]
            c.lvl_2_slots_expended = c_data["2nd-level-spell-slots"]

            c.lvl_3_slots_total = c_data["3rd-level-spell-slots"]
            c.lvl_3_slots_expended = c_data["3rd-level-spell-slots"]

            c.lvl_4_slots_total = c_data["4th-level-spell-slots"]
            c.lvl_4_slots_expended = c_data["4th-level-spell-slots"]

            c.lvl_5_slots_total = c_data["5th-level-spell-slots"]
            c.lvl_5_slots_expended = c_data["5th-level-spell-slots"]

            c.lvl_6_slots_total = c_data["6th-level-spell-slots"]
            c.lvl_6_slots_expended = c_data["6th-level-spell-slots"]

            c.lvl_7_slots_total = c_data["7th-level-spell-slots"]
            c.lvl_7_slots_expended = c_data["7th-level-spell-slots"]

            c.lvl_8_slots_total = c_data["8th-level-spell-slots"]
            c.lvl_8_slots_expended = c_data["8th-level-spell-slots"]

            c.lvl_9_slots_total = c_data["9th-level-spell-slots"]
            c.lvl_9_slots_expended = c_data["9th-level-spell-slots"]

            c.save()

            cantrips = retrieve_spells(c_data, "cantrips")
            l1_spells = retrieve_spells(c_data, "1st-level-spells")
            l2_spells = retrieve_spells(c_data, "2nd-level-spells")
            l3_spells = retrieve_spells(c_data, "3rd-level-spells")
            l4_spells = retrieve_spells(c_data, "4th-level-spells")
            l5_spells = retrieve_spells(c_data, "5th-level-spells")
            l6_spells = retrieve_spells(c_data, "6th-level-spells")
            l7_spells = retrieve_spells(c_data, "7th-level-spells")
            l8_spells = retrieve_spells(c_data, "8th-level-spells")
            l9_spells = retrieve_spells(c_data, "9th-level-spells")

            add_spells_to_char(c, cantrips, 0)
            add_spells_to_char(c, l1_spells, 1)
            add_spells_to_char(c, l2_spells, 2)
            add_spells_to_char(c, l3_spells, 3)
            add_spells_to_char(c, l4_spells, 4)
            add_spells_to_char(c, l5_spells, 5)
            add_spells_to_char(c, l6_spells, 6)
            add_spells_to_char(c, l7_spells, 7)
            add_spells_to_char(c, l8_spells, 8)
            add_spells_to_char(c, l9_spells, 9)

            c.save()

            return redirect('/characters/mycharacters')

    context["messages"] = reverse_list(context["messages"])
    return render(request, 'create.html', context=context)


def my_characters(request):
    context = {
        "username": "",
        "characters": []
    }

    if request.user.is_authenticated:
        context["username"] = request.user.username
    else:
        return redirect('/auth/login/')

    user = HA_User.objects.get(username=request.user.username)
    characters = list(Character.objects.filter(user=user))
    for character in characters:
        character_dict = {
            "id": character.pk,
            "name": character.name,
            "class_and_level": character.character_class_and_level
        }
        context["characters"].append(character_dict)

    return render(request, 'mycharacters.html', context=context)


def character_detail(request, character_id):
    print(character_id)

    context = {
        "username": "",
        "character_id": character_id,
        "character": None
    }

    # Check if the user is logged in
    if not request.user.is_authenticated:
        # If not, redirect to login page
        return redirect('/auth/login/')

    c = Character.objects.get(pk=character_id)
    username = request.user.username
    user = HA_User.objects.get(username=username)

    # Check if the character belongs to the user
    if c.user != user:
        # If not, redirect to home
        return redirect('/')

    context["username"] = username

    if request.method == "POST":
        print("hello")
        print(request.POST)

    c_race = c.subrace.name if c.subrace else c.race

    spells = CharacterSpell.objects.filter(character=c)

    cantrips = []
    level_1_spells = []
    level_2_spells = []
    level_3_spells = []
    level_4_spells = []
    level_5_spells = []
    level_6_spells = []
    level_7_spells = []
    level_8_spells = []
    level_9_spells = []

    for char_spell in spells:
        spell = (char_spell.spell, char_spell.prepared)
        if char_spell.level == 0:
            cantrips.append(spell)
        elif char_spell.level == 1:
            level_1_spells.append(spell)
        elif char_spell.level == 2:
            level_2_spells.append(spell)
        elif char_spell.level == 3:
            level_3_spells.append(spell)
        elif char_spell.level == 4:
            level_4_spells.append(spell)
        elif char_spell.level == 5:
            level_5_spells.append(spell)
        elif char_spell.level == 6:
            level_6_spells.append(spell)
        elif char_spell.level == 7:
            level_7_spells.append(spell)
        elif char_spell.level == 8:
            level_8_spells.append(spell)
        elif char_spell.level == 9:
            level_9_spells.append(spell)

    print(sorted(level_1_spells, key=lambda i:i[0]))

    # Parses database-formatted hit dice into standard dice notation
    hit_dice = "d" + str(int(c.hit_dice.split("D")[1]))

    character_dict = {
        "name": c.name,
        "size": c.size,
        "class_and_level": c.character_class_and_level,
        "inventory": c.inventory,
        "race": c_race,
        "prof_bonus": c.proficiency_bonus,

        "str_score": c.str_score,
        "str_mod": c.str_mod,
        "str_save": c.str_save,

        "dex_score": c.dex_score,
        "dex_mod": c.dex_mod,
        "dex_save": c.dex_save,

        "con_score": c.con_score,
        "con_mod": c.con_mod,
        "con_save": c.con_save,

        "int_score": c.int_score,
        "int_mod": c.int_mod,
        "int_save": c.int_save,

        "wis_score": c.wis_score,
        "wis_mod": c.wis_mod,
        "wis_save": c.wis_save,

        "cha_score": c.cha_score,
        "cha_mod": c.cha_mod,
        "cha_save": c.cha_save,

        "acrobatics_prof": c.acrobatics_prof,
        "acrobatics_exp": c.acrobatics_exp,
        "animal_handling_prof": c.animal_handling_prof,
        "animal_handling_exp": c.animal_handling_exp,
        "arcana_prof": c.arcana_prof,
        "arcana_exp": c.arcana_exp,
        "athletics_prof": c.athletics_prof,
        "athletics_exp": c.athletics_exp,
        "deception_prof": c.deception_prof,
        "deception_exp": c.deception_exp,
        "history_prof": c.history_prof,
        "history_exp": c.history_exp,
        "insight_prof": c.insight_prof,
        "insight_exp": c.insight_exp,
        "intimidation_prof": c.intimidation_prof,
        "intimidation_exp": c.intimidation_exp,
        "investigation_prof": c.investigation_prof,
        "investigation_exp": c.investigation_exp,
        "medicine_prof": c.medicine_prof,
        "medicine_exp": c.medicine_exp,
        "nature_prof": c.nature_prof,
        "nature_exp": c.nature_exp,
        "perception_prof": c.perception_prof,
        "perception_exp": c.perception_exp,
        "performance_prof": c.performance_prof,
        "persuasion_prof": c.persuasion_prof,
        "persuasion_exp": c.persuasion_exp,
        "religion_prof": c.religion_prof,
        "religion_exp": c.religion_exp,
        "sleight_of_hand_prof": c.sleight_of_hand_prof,
        "sleight_of_hand_exp": c.sleight_of_hand_exp,
        "stealth_prof": c.stealth_prof,
        "stealth_exp": c.stealth_exp,
        "survival_prof": c.survival_prof,
        "survival_exp": c.survival_exp,
        "passive_wis": c.passive_wis,

        # Other proficiencies
        "weapons_and_armour": c.weapons_and_armour,
        "tools": c.tools,
        "languages": c.languages,

        "armour_class": c.armour_class,
        "initiative_mod": c.initiative_mod,
        "speed": c.speed,
        "max_hp": c.max_hp,
        "current_hp": c.current_hp,
        "temp_hp": c.temp_hp,
        "hit_dice": hit_dice,
        "hit_dice_remaining": c.hit_dice_remaining_and_total,
        "death_save_fails": c.death_save_fails,
        "death_save_passes": c.death_save_passes,

        "boons": c.boons,
        "conditions": c.conditions,

        "attacks": c.attacks,

        "equipment": c.equipment,
        "cp": c.cp,
        "sp": c.sp,
        "gp": c.gp,
        "ep": c.ep,
        "pp": c.pp,

        "features_and_traits": c.features_and_traits,

        "personality_traits": c.personality_traits,
        "ideals": c.ideals,
        "bonds": c.bonds,
        "flaws": c.flaws,
        "alignment": c.alignment,
        "age": c.age,
        "height": c.height,
        "weight": c.weight,
        "eyes": c.eyes,
        "skin": c.skin,
        "hair": c.hair,
        "description": c.description,
        "allies_and_orgs": c.allies_and_organisations,
        "backstory": c.backstory,

        "is_spellcaster": c.spellcaster,
        "spellcasting_class": c.character_class,
        "spellcasting_ability": c.spellcasting_ability,
        "spell_save_dc": c.spell_save_dc,
        "spell_attack_bonus": c.spell_attack_bonus,

        "cantrips": sorted(cantrips, key=lambda i:i[0]),
        "lvl_1_slots_total": c.lvl_1_slots_total,
        "lvl_1_slots_expended": c.lvl_1_slots_expended,
        "lvl_1_spells": sorted(level_1_spells, key=lambda i:i[0]),
        "lvl_2_slots_total": c.lvl_2_slots_total,
        "lvl_2_slots_expended": c.lvl_2_slots_expended,
        "lvl_2_spells": sorted(level_2_spells, key=lambda i:i[0]),
        "lvl_3_slots_total": c.lvl_3_slots_total,
        "lvl_3_slots_expended": c.lvl_3_slots_expended,
        "lvl_3_spells": sorted(level_3_spells, key=lambda i:i[0]),
        "lvl_4_slots_total": c.lvl_4_slots_total,
        "lvl_4_slots_expended": c.lvl_4_slots_expended,
        "lvl_4_spells": sorted(level_4_spells, key=lambda i:i[0]),
        "lvl_5_slots_total": c.lvl_5_slots_total,
        "lvl_5_slots_expended": c.lvl_5_slots_expended,
        "lvl_5_spells": sorted(level_5_spells, key=lambda i:i[0]),
        "lvl_6_slots_total": c.lvl_6_slots_total,
        "lvl_6_slots_expended": c.lvl_6_slots_expended,
        "lvl_6_spells": sorted(level_6_spells, key=lambda i:i[0]),
        "lvl_7_slots_total": c.lvl_7_slots_total,
        "lvl_7_slots_expended": c.lvl_7_slots_expended,
        "lvl_7_spells": sorted(level_7_spells, key=lambda i:i[0]),
        "lvl_8_slots_total": c.lvl_8_slots_total,
        "lvl_8_slots_expended": c.lvl_8_slots_expended,
        "lvl_8_spells": sorted(level_8_spells, key=lambda i:i[0]),
        "lvl_9_slots_total": c.lvl_9_slots_total,
        "lvl_9_slots_expended": c.lvl_9_slots_expended,
        "lvl_9_spells": sorted(level_9_spells, key=lambda i:i[0])

    }

    context["character"] = character_dict

    return render(request, 'character.html', context)


def main():
    pass


if __name__ == "__main__":
    main()
