from openAI_api_handler import *
import json
import logging

logging.basicConfig(level=logging.INFO)
if __name__ == "__main__":
    LOGGER = logging.getLogger("general")
else:
    LOGGER = logging.getLogger(__name__)

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

def test_hero_constructor():
    LOGGER.debug("Getting assistant ID...")
    # a_id = GenerationAssistant.get_id()
    client = OpenAIClient.get_client()

    instructions = get_txt_file("hero_constructor_instructions.txt")
    function = get_json_file("create_character.json")
    # a = client.beta.assistants.create(
    #     name="HeroConstructor",
    #     instructions=instructions,
    #     model="gpt-4-1106-preview",
    #     tools=[{
    #         "type": "function",
    #         "function": function
    #     }]
    # )
    # a_id = a.id
    a_id = create_assistant(
        name="HeroConstructor",
        instructions=instructions,
        functions=function
    ).id

    LOGGER.info("Getting thread...")
    # t = get_thread("thread_hzIDtsSfNZPIljheUhfxvCxe")
    t = initialise_thread()

    content = "Hi! Can you create a level 1 High Elf Bard for me?"
    _ = add_message_to_thread(content, t.id, role="user")

    LOGGER.info("Running assistant...")
    r = run_assistant(t.id, a_id)

    c = 0
    while (r.status != "requires_action") and (r.status != "completed"):
        LOGGER.info(f"Polling. {c * 0.5} seconds elapsed...")
        c += 1
        time.sleep(0.5)
        r = retrieve_run(t, r)
        LOGGER.info(f"r_status: {r.status}")

    if r.status == "completed":
        LOGGER.error(f"ERROR: AI did not function call.")
        ms = retrieve_messages(t)
        print(ms.data)
        return

    args_str = r.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    args = json.loads(args_str)
    print(args)
    call_id = r.required_action.submit_tool_outputs.tool_calls[0].id
    put_run_out_of_misery(thread=t, run=r, call_id=call_id, output="127")

    c=0
    while r.status != "completed":
        LOGGER.info(f"Polling. {c * 0.5} seconds elapsed...")
        c += 1
        time.sleep(0.5)
        r = retrieve_run(t, r)
        LOGGER.debug(f"r_status: {r.status}")
    LOGGER.info("Run complete!")
    LOGGER.info("Retrieving messages...")

    # Response object layout can be found at https://platform.openai.com/docs/api-reference/messages/listMessages
    ms = retrieve_messages(t)
    print(ms.data)

def main():
    # test_hero_constructor()




if __name__ == "__main__":
    main()
