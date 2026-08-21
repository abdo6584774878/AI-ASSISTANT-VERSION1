import logging
from dotenv import load_dotenv 
from assistant.commands import handle_command
from assistant.config import get_assistant_backend
from assistant.factory import create_assistant

def main():
   load_dotenv()
   logging.basicConfig(level=logging.ERROR)
   assitant_backend = get_assistant_backend()
   assistant = create_assistant(assitant_backend)

   while True:
    user_input = input("You: ")
    if user_input.startswith("/"):
        command_result = handle_command(user_input, assistant)
        if command_result == "exit":
            print("Exiting the chat. Goodbye!")
            break
        elif command_result == "handled":
            continue
        else:
            print("Unknown command. Type /help for a list of commands.")
            continue

    #response = assistant.send_message(user_input)

    for chunk in assistant.stream_message(user_input):
        print(chunk, end="", flush=True)
    
    print()


if __name__ == "__main__":
    main()

