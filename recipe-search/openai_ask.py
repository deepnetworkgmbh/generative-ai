import os

from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint='https://openai-dn-fr.openai.azure.com/',
    api_key=os.environ.get('OPENAI_API_KEY'),
    api_version="2023-09-01-preview"
)


def openai_ask_dish_init(user_request, language):
    # 1. Ask ---
    # parameters_schema = {
    #     "type": "object",
    #     "properties": {
    #         "meal_name": {
    #             "type": "string",
    #             "description": 'The name of the meal. If no name is provided or the name you find is not a valid meal name, return "not_stated".',
    #         },
    #     },
    #     "required": ["meal_name"],
    # }
    #
    # function_schema = {
    #     "name": "set_meal_name",
    #     "description": "Get/Scrape meal name from the statement.",
    #     "parameters": parameters_schema,
    # }

    messages_init = [{"role": "system", "content": "You are an assistant that gets dish name from the statement."
                                                   "Return json object which consists of 2 fields."
                                                   "These fields are 'is_dish' and 'dish_name'"
                                                   "Do not give other information in json."
                                                   "Do not give instructions or ingredients in json object."
                                                   "If you can find meal name, set 'is_dish' true, and 'dish_name' name of the dish"
                                                   "If you can not find dish name, set 'is_dish' false, and 'dish_name' not_stated"
                                                   "Dish name can not be just a product such as apple, orange etc. If so, set 'is_dish' false, and 'dish_name' not_stated"
                                                   f"Language of the dish is {language}, so please consider that language during dish search."
                      }, {"role": "user", "content": user_request}]

    response_init = client.chat.completions.create(
        model='test-deployment',
        messages=messages_init,
    )
    # args_init = json.loads(response_init.choices[0].message.function_call.arguments)
    # return args_init["meal_name"]
    return response_init


def openai_ask_count_init(user_request, language):
    # 1. Ask ---
    messages_init = [{"role": "system", "content": "You are an assistant that gets number of people from the statement."
                                                   "Return json object which consists of 2 fields."
                                                   "These fields are 'is_count' and 'number_of_people'"
                                                   "Do not give other information in json."
                                                   "If you can find number of people, set 'is_count' true, and 'number_of_people' people count"
                                                   "If you can not find number of people, set 'is_count' false, and 'number_of_people' not_stated"
                                                   "People count can be given such as '5 people', '3 men' or just '2000'. Always return just integer not other words."
                                                   "Number can be given as string, such as 'five' or 'zwei' etc. In that case, convert them to integer (5, 2 respectively) and set 'number_of_people'"
                                                   "If given value is not integer such as '3.5' or '4/5' etc.; set 'is_count' false and 'number_of_people' not_stated"
                                                   f"User input can be given any language such as 'five men', 'vier mensch' or 'bes kisi'. Consider {language} while responding."
                      }, {"role": "user", "content": user_request}]

    response_init = client.chat.completions.create(
        model='test-deployment',
        messages=messages_init,
    )
    # args_init = json.loads(response_init.choices[0].message.function_call.arguments)
    # return args_init["meal_name"]
    return response_init


def openai_ask_language(user_request):
    messages_check = [{"role": "system", "content": "You are an assistant that determine the language used in user request."
                                                    "Return only the language."
                                                    "Do not make sentence, only return language such as 'English', 'German'."
                       }, {"role": "user", "content": user_request}]

    response_check = client.chat.completions.create(
        model='test-deployment',
        messages=messages_check,
    )
    return response_check.choices[0].message.content


def openai_ask_general_check(input, type, language): # input, type --> if 'input' is really a 'type' -> type in system message, 'input' in user message
    # 2. Ask - Double Check ---
    messages_check = [{"role": "system", "content": f"You are an assistant that check if the given input is actually a {type} or not in {language}."
                                                    "Return json object which consists of 1 field called 'is_that_type'."
                                                    f"Set 'is_that_type' field 'True' in string format if it is {type} in {language}."
                                                    f"Set 'is_that_type' field 'False' in string format if it is not {type} in {language}."                                                    
                                                    f"Language of the input is {language}, so please consider that language during type check."
                       }, {"role": "user", "content": str(input)}]

    response_check = client.chat.completions.create(
        model='test-deployment',
        messages=messages_check,
    )
    return response_check
