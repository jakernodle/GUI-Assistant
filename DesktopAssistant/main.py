from DesktopAssistant.GPTServices import get_tasks_response, get_context_for_command_response
from DesktopAssistant.DesktopServices import take_screenshot
from iMessageAssistant.main import iMessageAssistant
import json

class DesktopAssistant:
    #a queue for tasks that are requested by the user
    task_queue = [] 

    #internal services
    #assistant_services = AssistantInternalServices()
    #init start watching screen
    def __init__(self):
        print("What can I help with?")
        user_input = input()
        # exposed_functions_map = {
        #     "respond_to_unread_messages": {
        #         "description": "This command will responsed to all unread messages with optional message context.",
        #         "required-context": None,
        #         "optional-context": { "name": "message-context", "description": "any additional context provided by the user to be included in message responses" },
        #     },
        #     "send_message_to": {
        #         "description": "This command will send a single message to a recipient or recipients with optional message context.",
        #         "required-context": { "name": "message-recipient", "description": "the recipient of the message"},
        #         "optional-context": { "name": "message-context", "description": "any additional context provided by the user to be included the message"},
        #     },
        # }

        exposed_functions_map = {
            "respond_to_unread_messages": {
                "description": "This command will respond to all messages with optional message context.",
                #"context": {"message":"provide what should be included in message responses"},
            },
            "send_message_to": {
                "description": "This command will send a single message to a recipient or recipients with optional message context.",
               # "context": { "recipient":"provide the recipient or recipients of the message in a coma seperated list", "message":"provide what should be included in message"},
            },
        }
        context_prompts = {
            "respond_to_unread_messages": {
                "message":{
                    "prompt":"What are the message topics?",
                    "response-criteria":"Your response should be decodable json in the form of an array of strings. If there are no discernible topics return an empty array. Your response should be in quotes",
                    "example-responses": """
                        Example: Send a message about my favorite color blue and how crazy the news has been recently.
                        Your response: "["my favorite color is blue", "the news has been crazy recently"]"

                        Example: ask donald if he picked up the to-go order, 
                        Your response: "["was the to-go order picked up"]"

                        Example: Tell davis and hunter that I'll be there in 20 minutes.
                        Your response: "["I'll be there in 20 minutes"]"

                        return ONLY the response part in quotes
                    """,
                }
            },
            "send_message_to": {
                "recipient": {
                    "prompt":"who are the recipient(s) of the message?",
                    "response-criteria":"Your response should be decodable json in the form of an array of strings. If there are no recipients return an empty array. Your response should be in quotes",
                    "example-responses": """
                        Example: Send a message about my favorite color blue.
                        Response: "[]"

                        Example: Send a message to donald my favorite color blue.
                        Response: "["donald"]"

                        Example: Tell davis and hunter that I'll be there in 20 minutes.
                        Response: "["davis", "hunter"]"

                        return ONLY the response part in quotes
                    """,
                }, 
                "message": {
                    "prompt":"What are the message topics?",
                    "response-criteria":"Your response should be decodable json in the form of an array of strings. If there are no discernible topics return an empty array. Your response should be in quotes",
                    "example-responses": """
                        Example: Send a message about my favorite color blue and how crazy the news has been recently.
                        Your response: "["my favorite color is blue", "the news has been crazy recently"]"

                        Example: ask donald if he picked up the to-go order, 
                        Your response: "["was the to-go order picked up"]"

                        Example: Tell davis and hunter that I'll be there in 20 minutes and they going out last night was so fun.
                        Your response: "["I'll be there in 20 minutes", "going out last night was so fun"]"

                        return ONLY the response part in quotes
                    """,
                },
            }
        }   

        def remove_before_first_bracket(input_string, find='['):
            index = input_string.find(find)
            if index != -1:
                return input_string[index:]
            else:
                return input_string
        
        def extract_between_quotes(input_string):
            first_quote_index = input_string.find('"')
            last_quote_index = input_string.rfind('"')

            if first_quote_index != -1 and last_quote_index != -1 and last_quote_index > first_quote_index:
                return input_string[first_quote_index + 1:last_quote_index]
            else:
                return ""

        print("EXPOSED:", exposed_functions_map)
        exposed_functions_json_string = json.dumps(exposed_functions_map, indent=4)
        print("INPUT:", user_input)
        tasks_string = get_tasks_response(user_input, exposed_functions_json_string)

        # Define the prefix to remove
        prefix = "Your response: "

        # Remove the prefix once
        print("TASK STRING:", tasks_string)
        cleaned_string = remove_before_first_bracket(tasks_string)
        print("CLEANED STRING:", tasks_string)
        tasks = json.loads(cleaned_string)
        print("TASKS:",tasks)

        commands = []
        for task in tasks:
            command_name = task["command"]
            command_details = exposed_functions_map[command_name]
            command_context_to_infer = context_prompts[command_name]
            command_map = {"command":command_name}
            for key, value in command_context_to_infer.items():
                print("GETTING CONTEXT:",task["context"])
                raw_context = get_context_for_command_response(task["context"], value["prompt"], value["response-criteria"], value["example-responses"])
                print("PARSING:",raw_context)
                parsed_context = extract_between_quotes(raw_context)
                print("DECODING:",parsed_context)
                loaded_context = json.loads(parsed_context)
                command_map[key] = loaded_context
            commands.append(command_map)

        print(commands)

        #commands = "respond_to_unread_messages"
        self.handle_commands(commands)
    
    # handle the commands
    def handle_commands(self, commands):

        #TODO: move this function
        def stringify_message_context(message_topic_context):
            if message_topic_context is None:
                message_topics = ""
            else:
                formatted_topics = ', '.join(message_topic_context)  # Join the array elements into a string
                message_topics = f"These are important topics that your response should be mainly about: {formatted_topics}"

        for command in commands:
            if command["command"] == "respond_to_unread_messages":
                screenshot = take_screenshot()
                new_assistant = iMessageAssistant(screenshot)
                context_string = stringify_message_context(command["message"])
                new_assistant.respond_to_unread_messages(context_string)

            if command["command"] == "send_message_to":
                screenshot = take_screenshot()
                new_assistant = iMessageAssistant(screenshot)
                context_string = stringify_message_context(command["message"])
                new_assistant.send_message_to(command["recipient"], context_string)


    #pick up windows
    # def watch_screen():
    #      while True:
    #         # Take Screenshot
    #         #screenshot = take_screenshot()
    #         #predictions = run_inference(screenshot)
    #         time.sleep(5)

    # #desktop opject detection
    # def run_inference(screenshot):
    #     pass

    #def perform_tasks:
       # for task in task_queue:

   