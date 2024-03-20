from openai import OpenAI
from dotenv import load_dotenv
import logging
import time
import os

logging.basicConfig(level=logging.NOTSET)
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
        return ChatAssistant.id


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
    c = 0
    while run.status != "completed":
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


def openAI_API_call(client, messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message

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
