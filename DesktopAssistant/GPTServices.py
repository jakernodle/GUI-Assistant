import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

def get_commands(task_string, availible_functions):
    prompt = f"Given the following task(s):\n{task_string}\nand commands: {availible_functions}\ndetermine which of the provided function(s) should be run to achieve the task. Only respond with the name of the function(s) in a comma seperated list."

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

def respond_to_message_thread(ocr_text):
    prompt = f"Write a response to the following text message thread:\n{ocr_text}\nYour response:"

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