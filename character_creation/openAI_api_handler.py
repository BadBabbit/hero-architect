from openai import OpenAI
from dotenv import load_dotenv
import time
import os

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

def main():

    print("Initialising thread...")
    t = initialise_thread()
    print(f"Thread ID: {t.id}")

    print("Adding message to thread...")
    content = "I want to create an intellectual academic. How can I do that?"
    _ = add_message_to_thread(content, t)

    print("Getting assistant ID...")
    a = Assistant.get_id()
    print("Running assistant...")
    r = run_assistant(t, a)

    while r.status != "completed":
        print("Polling...")
        time.sleep(0.5)
        r = retrieve_run(t, r)
        print(f"r_status: {r.status}")
    print("Run complete!")
    print("Retrieving messages...")
    ms = retrieve_messages(t)
    print(ms.data[0].content)


if __name__ == "__main__":
    main()