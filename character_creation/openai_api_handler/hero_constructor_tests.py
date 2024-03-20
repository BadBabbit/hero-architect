from openAI_api_handler import *
import logging

logging.basicConfig(level=logging.INFO)
if __name__ == "__main__":
    LOGGER = logging.getLogger("general")
else:
    LOGGER = logging.getLogger(__name__)

def main():
    LOGGER.debug("Getting assistant ID...")
    # a_id = GenerationAssistant.get_id()
    client = OpenAIClient.get_client()
    a = client.beta.assistants.create(
        instructions="You are a helpful dietitian who uses the provided functions in order to tell users the calorie content of foods they are interested in. ",
        model="gpt-4-1106-preview",
        tools=[{
            "type": "function",
            "function": {
                "name": "get_calories",
                "description": "A function that takes a food item as an input and returns the calorie content of that food as an output.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "food": {
                            "type": "string",
                            "description": "The food of interest."
                        }
                    },
                    "required": [
                        "food"
                    ]
                }
            }
        }]
    )
    a_id = a.id

    LOGGER.info("Getting thread...")
    # t = get_thread("thread_hzIDtsSfNZPIljheUhfxvCxe")
    t = initialise_thread()

    content = "Hi! How many calories are there in an apple?"
    _ = add_message_to_thread(content, t.id, role="user")

    LOGGER.info("Running assistant...")
    r = run_assistant(t.id, a_id)

    c = 0
    while (r.status != "requires_action") and (r.status != "completed"):
        LOGGER.info(f"Polling. {c * 0.5} seconds elapsed...")
        c+=1
        time.sleep(0.5)
        r = retrieve_run(t, r)
        LOGGER.info(f"r_status: {r.status}")

    if r.status == "completed":
        ms = retrieve_messages(t)
        print(ms.data)

    apple = r.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    print(apple)
    call_id = r.required_action.submit_tool_outputs.tool_calls[0].id
    put_run_out_of_misery(thread=t, run=r, call_id=call_id, output="127")

    c=0
    while r.status != "completed":
        LOGGER.info(f"Polling. {c * 0.5} seconds elapsed...")
        c+=1
        time.sleep(0.5)
        r = retrieve_run(t, r)
        LOGGER.debug(f"r_status: {r.status}")
    LOGGER.info("Run complete!")
    LOGGER.info("Retrieving messages...")

    # Response object layout can be found at https://platform.openai.com/docs/api-reference/messages/listMessages
    ms = retrieve_messages(t)
    print(ms.data)


if __name__ == "__main__":
    main()
