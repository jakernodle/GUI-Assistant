from DesktopAssistant.GPTServices import get_commands
from DesktopAssistant.DesktopServices import take_screenshot
from iMessageAssistant.main import iMessageAssistant

class DesktopAssistant:
    #a queue for tasks that are requested by the user
    task_queue = [] 

    #internal services
    #assistant_services = AssistantInternalServices()
    #init start watching screen
    def __init__(self):
        print("What can I help with?")
        user_input = input()
        exposed_functions_description = """
            name:respond_to_unread_messages
            description:Send responses to all visible unread message threads.
            """
        commands = get_commands(user_input, exposed_functions_description)
        #commands = "respond_to_unread_messages"
        self.handle_commands(commands)

    # handle the commands
    def handle_commands(self, commands):
        commands_array = [commands.strip() for command in commands.split(',')]
        print(commands_array)

        if "respond_to_unread_messages" in commands_array:
            screenshot = take_screenshot()
            new_assistant = iMessageAssistant(screenshot)
            new_assistant.respond_to_unread_messages()


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