from django.shortcuts import render, redirect
from django.db import transaction, DatabaseError, IntegrityError
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
        _ = heroArchitect.add_message_to_thread(content, t)
        LOGGER.debug("Getting assistant ID...")
        a = heroArchitect.Assistant.get_id()
        LOGGER.debug("Running assistant...")
        r = heroArchitect.run_assistant(t, a)
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
            message_object = Message(content=content)
            conversation.messages.add(message_object)
            message_object.user = user

            conversation.save()
            message_object.save()

    # Marks conversation as inactive if an error occurs.
    except Exception as e:
        conversation.active = False


# view for create.html, at index /create/
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

        user_obj = HA_User.objects.get(username=request.user.username)
        if user_obj is None:
            LOGGER.error(f" COULD NOT FIND USER WITH USERNAME '{request.user.username}'")
            raise DatabaseError

        # Handles initial prompt
        if start is not None:

            t = initialise_conversation(start)
            conversation = Conversation(thread_id=t.id, active=True)
            conversation.user = user_obj
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
        elif message is not None:
            conversation = Conversation.objects.filter(active=True).get()
            # Do stuff with the user's message

            # Add message to database
            add_message_to_database(user_obj, conversation, message)

            t_id = conversation.thread_id
            thread = heroArchitect.get_thread(t_id)
            heroArchitect.add_message_to_thread(message, thread)

            a_id = heroArchitect.Assistant.get_id()  # Assistant ID
            LOGGER.info("Running assistant.")
            run = heroArchitect.run_assistant(t_id, a_id)
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

    return render(request, 'create.html', context)


def my_characters(request):
    context = {}
    return render(request, 'TODO.html', context)


def character_detail(request):
    context = {}
    return render(request, 'TODO.html', context)


def main():
    pass


if __name__ == "__main__":
    main()
