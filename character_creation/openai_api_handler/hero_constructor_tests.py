from openAI_api_handler import *
import logging

logging.basicConfig(level=logging.NOTSET)
if __name__ == "__main__":
    LOGGER = logging.getLogger("general")
else:
    LOGGER = logging.getLogger(__name__)

def main():
    LOGGER.debug("Getting assistant ID...")
    a_id = GenerationAssistant.get_id()
    LOGGER.debug("Getting thread...")
    t = get_thread("thread_hzIDtsSfNZPIljheUhfxvCxe")

    content = "Could you generate it again for me? Something went wrong on my end."
    _ = add_message_to_thread(content, t.id, role="user")

    LOGGER.debug("Running assistant...")
    r = run_assistant(t.id, a_id)


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
    print(ms.data)

if __name__ == "__main__":
    main()
