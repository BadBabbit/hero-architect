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

class Assistant:
    load_dotenv()
    id = os.getenv("ASSISTANT_ID")

    @staticmethod
    def get_id():
        return Assistant.id

def initialise_thread():
    client = OpenAIClient.get_client()
    return client.beta.threads.create()

def add_message_to_thread(content, thread):
    client = OpenAIClient.get_client()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )
    return message

def run_assistant(thread, assistant, instructions=""):
    client = OpenAIClient.get_client()
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant,
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

def openAI_API_call(client, messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message

def main(LOGGER):

    LOGGER.debug("Initialising thread...")
    t = initialise_thread()
    LOGGER.debug(f"Thread ID: {t.id}")

    LOGGER.debug("Adding message to thread...")
    content = "I want to create a level 2 barbarian. How do I start?"
    _ = add_message_to_thread(content, t)

    LOGGER.debug("Getting assistant ID...")
    a = Assistant.get_id()
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
    ms = retrieve_messages(t)
    print(ms.data[0].content)


if __name__ == "__main__":
    main()
