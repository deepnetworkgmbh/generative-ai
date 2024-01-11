import json
import os
from openai import AzureOpenAI

IMPORTANT_INFORMATION = """
- Dietary restrictions or preferences, eg. being vegeterian, having alergies
- Style of cooking, eg. baked, fried
- Preferred cuisines, eg. Italian, French
"""

SYSTEM_MESSAGE = """
You are a cooking assistant that will help with finding dishes the user can cook.
Never answer questions unrelated to this task. Instead tell the user "I am a cooking assistant, I cannot help with that"
You have the list of ingredients user has at home below.
Ingredients:
{ingredients}

Assume user has nothing else at home, so try to come up with dishes from the list above.
You can use other ingredients as well but try to keep those to a minimum.
When you come up with a dish, list what ingredients the user will need to buy for that dish.
You will ask questions one by one to come up with a dish that the user will like.
Below are some of the important information you should ask about to the user but if you need other information ask about them as well.
IMPORTANT_INFORMATION:
{important_information}
"""

DISH_SYSTEM_MESSAGE = """
You are a chat analyzer tool, your job is to find the dish user agreed upon in the below chat history.
You must only answer with the dish name and nothing else.
If the user has not picked any dish respond with 'no_dish_chosen'
Chat History:
{chat_history}
"""

def get_ingredients(file):
    with open(file, 'r') as f:
        return json.load(f)

def add_to_messages(history, completion, prompt):
    history.append({"role": "assistant", "content": completion})
    history.append({"role": "user", "content": prompt})
    return history

def chat_with_gpt(client, messages):
    return client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
        messages=messages,
        temperature=0.7,
        frequency_penalty=0.3
    ).choices[0].message.content

def get_dish_name_from_chat(client, history):
    return client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
        messages=[{"role": "system", "content": DISH_SYSTEM_MESSAGE.format(chat_history=history)}],
        temperature=0,
    ).choices[0].message.content

def main():
    client = AzureOpenAI(
        api_version="2023-09-01-preview"
    )

    ingredients = get_ingredients("./recipe-generator/reverse_recipe/ingredients_at_home.json")
    system_message = SYSTEM_MESSAGE.format(ingredients=ingredients, important_information=IMPORTANT_INFORMATION)
    messages = [{"role": "system", "content": system_message}]
    print('You can type "yes" to choose a dish or "exit" to stop the program.')
    while True:
        completion = chat_with_gpt(client, messages)
        prompt = input(f"{completion}\n")
        if prompt == "yes":
            messages = add_to_messages(messages, completion, prompt)
            dish_name = get_dish_name_from_chat(client, messages[1:])
            if dish_name == "no_dish_chosen":
                print("No dish was chosen")
            else:
                print(f"Chosen dish: {dish_name}")
            break
        elif prompt == "exit":
            break
        else:
            messages = add_to_messages(messages, completion, prompt)

if __name__ == "__main__":
    main()