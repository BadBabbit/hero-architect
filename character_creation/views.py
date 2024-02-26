from django.shortcuts import render
from django.http import HttpResponse
from openai_api_handler import openAI_api_handler as heroArchitect

logging.basicConfig(level=logging.NOTSET)
if __name__ == "__main__":
    LOGGER = logging.getLogger("general")
else:
    LOGGER = logging.getLogger(__name__)

def create_message(author, content):
    message = {}
    message['author'] = author
    message['content'] = content
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
            r = retrieve_run(t, r)
            LOGGER.debug(f"r_status: {r.status}")

    return t



# view for create.html, at index /create/
def create_character(request):
    context = {}
    context["messages"] = []
    context["messages"]
    if request.method == 'POST':
        data = request.POST

        # Handles initial prompt
        action = data.get("start")
        if action != None:
            t = initialise_conversation(action)
            response = heroArchitect.retrieve_messages(t)
            messages = response[data]
            for m in messages:
                content = m.content[0].text.value

                # Exclude thread initialiser message
                if content == "BEGIN_THREAD":
                    continue

                # Author can either be "user" or "assistant"
                author = m.role

                # Add message to the context
                context["messages"].append(create_message(author, content))

        # Handles user message inputs
        if

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

