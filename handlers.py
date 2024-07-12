import openai
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()
client = openai.OpenAI()

# Constants
PERSONA = "You are a skilled statician with knowledge of population numbers per country"
MODEL_ENGINE = "gpt-3.5-turbo"
MESSAGE_SYSTEM = " You are a skilled statician with knowledge of population numbers per country."
messages = [{"role": "system", "content": MESSAGE_SYSTEM}]


def to_dict(obj):
    return {
        "content": obj.content,
        "role": obj.role,
    }


def print_messages(messages):
    messages = [message for message in messages if message["role"] != "system"]
    for message in messages:
        role = "Bot" if message["role"] == "assistant" else "You"
        print(Fore.BLUE + role + ": " + message["content"])
    return messages

def moderate(user_input):
    response = client.moderations.create(input=user_input)
    return response.results[0].flagged


def generate_chat_completion(user_input=""):
    flagged = moderate(user_input)
    print(f"Flagged: {flagged}")
    if flagged:
        return ":red Your comment has been flagged for review"
    messages.append({"role": "user", "content": user_input})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    message = completion.choices[0].message
    messages.append(to_dict(message))
    print_messages(messages)
    return message.content