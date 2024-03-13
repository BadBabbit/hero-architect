from django.shortcuts import render, redirect
from django.db import transaction, DatabaseError, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import logging, time
from django.http import HttpResponse
from character_creation.openai_api_handler import openAI_api_handler as heroArchitect
from character_creation.models import *
from accounts.models import HA_User

logging.basicConfig(level=logging.NOTSET)
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
        content = "BEGIN_THREAD"
        _ = heroArchitect.add_message_to_thread(content, t.id)
        LOGGER.debug("Getting assistant ID...")
        a = heroArchitect.Assistant.get_id()
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
                for m in messages:
                    content = m.content[0].text.value

                    # Exclude thread initialiser message
                    if content == "BEGIN_THREAD":
                        continue

                    # Below should be unreachable by user messages

                    # Author can either be "user" or "assistant"
                    author = m.role
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
            a_id = heroArchitect.Assistant.get_id()  # Assistant ID
            LOGGER.info("Running assistant.")
            run = heroArchitect.run_assistant(t_id, a_id)

            # Retrieve response
            heroArchitect.wait_on_run(run, thread)
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

    if request.method == 'POST':
        pass

    return render(request, 'mycharacters.html', context=context)


def character_detail(request, character_id):
    print(character_id)

    context = {
        "username": "",
        "character": None
    }

    if request.user.is_authenticated:
        # Check if the character belongs to the user


        context["username"] = request.user.username
    else:
        return redirect('/auth/login/')
    return render(request, 'character.html', context)


def main():
    pass


if __name__ == "__main__":
    main()
