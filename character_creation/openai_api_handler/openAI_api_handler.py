from openai import OpenAI
from dotenv import load_dotenv
import logging, time, json, os

logging.basicConfig(level=logging.INFO)
if __name__ == "__main__":
    LOGGER = logging.getLogger("general")
else:
    LOGGER = logging.getLogger(__name__)

class OpenAIClient:
    load_dotenv()
    client = OpenAI()

    @staticmethod
    def get_client():
        return OpenAIClient.client

class ChatAssistant:
    load_dotenv()
    id = os.getenv("CHAT_ASSISTANT_ID")

    @staticmethod
    def get_id():
        return ChatAssistant.id

class GenerationAssistant:
    load_dotenv()
    id = os.getenv("GEN_ASSISTANT_ID")

    @staticmethod
    def get_id():
        return GenerationAssistant.id

def upload_file(file):
    client = OpenAIClient.get_client()
    file_id = client.files.create(
        file=open(file, "rb"),
        purpose="assistants"
    )
    return file_id


def create_assistant(name, instructions, model="gpt-4-1106-preview", functions=None, file_ids=[]):
    client = OpenAIClient.get_client()

    tools = []
    if functions is not None:
        tools.append({
            "type": "function",
            "function": functions
        })
    if bool(file_ids):
        tools.append({
            "type": "retrieval"
        })

    logging.info("Creating assistant...")
    a = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=tools,
        file_ids=file_ids
    )
    logging.info(f"Assistant created with ID {a.id}.")

    return a


def initialise_thread():
    client = OpenAIClient.get_client()
    return client.beta.threads.create()


def get_thread(thread_id):
    client = OpenAIClient.get_client()
    return client.beta.threads.retrieve(thread_id)


def add_message_to_thread(content, thread_id, role="user"):
    client = OpenAIClient.get_client()
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content
    )
    return message


def run_assistant(thread_id, assistant_id, instructions=""):
    client = OpenAIClient.get_client()
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions
    )
    return run


def retrieve_run(thread, run):
    client = OpenAIClient.get_client()
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    return run


def retrieve_messages(thread):
    client = OpenAIClient.get_client()
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    return messages


def wait_on_run(run, thread):
    # Run life-cycle: https://platform.openai.com/docs/assistants/how-it-works/run-lifecycle
    c = 0
    while run.status == "in_progress":
        if c % 5 == 0:
            LOGGER.debug(f"Polling. {c * 0.1} seconds elapsed...")
        c += 1
        time.sleep(0.1)
        run = retrieve_run(thread, run)
        LOGGER.debug(f"r_status: {run.status}")
    return run

def cancel_run(run, thread):
    client = OpenAIClient.get_client()
    LOGGER.info("Cancelling run...")
    run = client.beta.threads.runs.cancel(
        run_id=run.id
    )
    c = 0
    while not(run.status in ["cancelled", "failed", "completed"]):
        if c % 5 == 0:
            LOGGER.debug(f"Polling. {c * 0.1} seconds elapsed...")
        c += 1
        time.sleep(0.1)
        run = retrieve_run(thread, run)
        LOGGER.debug(f"r_status: {run.status}")


def put_run_out_of_misery(thread, run, call_id, output):
    client = OpenAIClient.get_client()
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": call_id,
                "output": output,
            },
        ]
    )
    return run

def get_json_file(file):
    with open(file, "r") as rf:
        data = json.load(rf)
    return data

def get_txt_file(file):
    with open(file, "r") as rf:
        data = rf.read()
    return data

def delete_assistant(assistant_id):
    client = OpenAIClient.get_client()
    return client.beta.assistants.delete(assistant_id=assistant_id)

def create_hero_constructor():
    client = OpenAIClient.get_client()

    instructions = get_txt_file("hero_constructor_instructions.txt")
    function = get_json_file("create_character.json")
    srd_id = os.getenv("SRD_FILE_ID")
    file_ids = [srd_id]
    a_id = create_assistant(
        name="HeroConstructor",
        instructions=instructions,
        functions=function,
        file_ids=file_ids
    ).id
    print(a_id)

def generate_character_data(thread_id):
    LOGGER.info("Generating character data...")
    assistant_id = GenerationAssistant.get_id()
    LOGGER.info(f"Thread ID: {thread_id}")

    content = "Please generate the character using the information above."
    add_message_to_thread(content, thread_id, role="user")

    LOGGER.info("Running assistant...")
    run = run_assistant(thread_id, assistant_id)

    thread = get_thread(thread_id)
    run = wait_on_run(run, thread)

    if run.status == "completed":
        LOGGER.error(f"ERROR: AI did not function call.")
        ms = retrieve_messages(thread)
        LOGGER.error(f"Conversation data: {ms.data}")
        raise RuntimeError

    args_str = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    args = json.loads(args_str)
    cancel_run(run, thread)

    return args


def main():

    LOGGER.debug("Initialising thread...")
    t = initialise_thread()
    LOGGER.debug(f"Thread ID: {t.id}")

    LOGGER.debug("Adding message to thread...")
    content = "I want to create a level 2 barbarian. How do I start?"
    _ = add_message_to_thread(content, t)

    LOGGER.debug("Getting assistant ID...")
    a = ChatAssistant.get_id()
    LOGGER.debug("Running assistant...")
    r = run_assistant(t, a)

    c = 0
    while r.status != "completed":
        LOGGER.debug(f"Polling. {c * 0.5} seconds elapsed...")
        c+=1
        time.sleep(0.5)
        r = retrieve_run(t, r)
        LOGGER.debug(f"r_status: {r.status}")
    LOGGER.info("Run complete!")
    LOGGER.debug("Retrieving messages...")

    # Response object layout can be found at https://platform.openai.com/docs/api-reference/messages/listMessages
    ms = retrieve_messages(t)
    print(ms.data[0].content[0].text.value)


if __name__ == "__main__":
    main()
