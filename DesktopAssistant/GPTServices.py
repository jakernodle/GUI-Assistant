import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

def get_tasks_response(tasks_string, availible_functions):
    prompt = f"""You are an assistant that can complete tasks on behalf of users. A user has requested the following:\n{tasks_string}\n and to help you complete your task you have the following commands: {availible_functions}\nyou must seperate the users request into the individual commands that need to be executed.  
    Your response should be in the form of an array of json objects that each include the command, and the context associated with that command. 
    
    Example: Tell davis I'll be home at 8 and respond to my messages and tell everyone I'm in a meeting but will respond shortly.
    Your response:[{{"command":"send_message_to", "context":"Tell davis I'll be home at 8"}},{{"command":"respond_to_unread_messages", "context":"Respond to my messages and tell everyone I'm in a meeting but will respond shortly.""}}]

    Example: Respond to my messages and send a message to hunter about the football game were going to.
    Your response: [{{"command":"respond_to_unread_messages", "context":""}}, {{"command":"send_message_to", "context":"Send a message to hunter about the football game were going to."}}]

    Example: Send a message about my favorite color blue.
    Your response: [{{"command":"send_message_to", "context":"Send a message about my favorite color blue."}}]
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "text-davinci-003",  # Choose an appropriate model like text-davinci-003
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.4  # Adjust as needed for creativity
    }

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        print("200", response_data)
        return response_data["choices"][0]["text"].strip()
    else:
        print("Error in API request:", response.status_code, response.text)
        return None

def get_context_for_command_response(task_string, prompt, response_criteria, example_responses):

    prompt = f"""Given the following string:"{task_string}". Answer this question: 
    {prompt}.\n
    {response_criteria}

    {example_responses}
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "text-davinci-003",  # Choose an appropriate model like text-davinci-003
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7  # Adjust as needed for creativity
    }

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["text"].strip()
    else:
        print("Error in API request:", response.status_code, response.text)
        return None

def respond_to_message_thread(ocr_text,message_topics):
    prompt = f"Write a response to the following text message thread:\n{ocr_text}\n{message_topics}\nYour response:"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "text-davinci-003",  # Choose an appropriate model like text-davinci-003
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7  # Adjust as needed for creativity
    }

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["text"].strip()
    else:
        print("Error in API request:", response.status_code, response.text)
        return None