import json

from openai import AzureOpenAI

client = AzureOpenAI(
    api_version="2023-09-01-preview"
)


def clean_dish_name(user_request, language):
    messages = [{"role": "system", "content": "You are an assistant that gets dish name from the statement."
                                                   "Return json object which consists of 2 fields."
                                                   "These fields are 'is_valid' and 'dish_name'"
                                                   "Do not give other information in json."
                                                   "Do not give instructions or ingredients in json object."
                                                   "If you can find meal name, set 'is_valid' true, and 'dish_name' name of the dish"
                                                   "If you can not find dish name, set 'is_valid' false, and 'dish_name' not_stated"
                                                   "Dish name can not be just a product such as apple, orange etc. If so, set 'is_valid' false, and 'dish_name' not_stated"
                                                   f"Language of the dish is {language}, so please consider that language during dish search."
                                                   "You must give the list of ingredients using the following JSON schema."
                                                   "JSON schema:\n"
                                                   "{'dish_name': '[DISH_NAME]', 'is_valid': [IS_VALID]}"
                      }, {"role": "user", "content": user_request}]

    return client.chat.completions.create(
        model='test-deployment',
        messages=messages,
        response_format={"type": "json_object"}
    )


def clean_servings_size(user_request, language):
    messages = [{"role": "system", "content": "You are an assistant that gets number of people from the statement."
                                                   "Return json object which consists of 2 fields."
                                                   "These fields are 'is_valid' and 'number_of_people'"
                                                   "Do not give other information in json."
                                                   "If you can find number of people, set 'is_valid' true, and 'number_of_people' people count"
                                                   "If you can not find number of people, set 'is_valid' false, and 'number_of_people' not_stated"
                                                   "People count can be given such as '5 people', '3 men' or just '2000'. Always return just integer not other words."
                                                   "Number can be given as string, such as 'five' or 'zwei' etc. In that case, convert them to integer (5, 2 respectively) and set 'number_of_people'"
                                                   "If given value is not integer such as '3.5' or '4/5' etc.; set 'is_valid' false and 'number_of_people' not_stated"
                                                   f"User input can be given any language such as 'five men', 'vier mensch' or 'bes kisi'. Consider {language} while responding."
                                                   "You must give the list of ingredients using the following JSON schema."
                                                   "JSON schema:\n"
                                                   "{'number_of_people': '[NUMBER_OF_PEOPLE]', 'is_valid': [IS_VALID]}"
                      }, {"role": "user", "content": user_request}]

    return client.chat.completions.create(
        model='test-deployment',
        messages=messages,
        response_format={"type": "json_object"}
    )


def ask_language(user_request):
    messages_check = [
        {"role": "system", "content": "You are an assistant that determine the language used in user request."
                                      "Return only the language."
                                      "Do not make sentence, only return language such as 'English', 'German'."
         }, {"role": "user", "content": user_request}]

    response_check = client.chat.completions.create(
        model='test-deployment',
        messages=messages_check,
    )
    return response_check.choices[0].message.content


def does_input_type_match(input, type,
                          language):  # input, type --> if 'input' is really a 'type' -> type in system message, 'input' in user message
    # 2. Ask - Double Check ---
    messages_check = [{"role": "system",
                       "content": f"You are an assistant that check if the given input is actually a {type} or not in {language}."
                                  "Return json object which consists of 1 field called 'is_correct_type'."
                                  f"Set 'is_correct_type' field 'True' in string format if it is {type} in {language}."
                                  f"Set 'is_correct_type' field 'False' in string format if it is not {type} in {language}."
                                  f"Language of the input is {language}, so please consider that language during type check."
                                  "You must give the list of ingredients using the following JSON schema."
                                  "JSON schema:\n"
                                  "{'is_correct_type': '[IS_CORRECT_TYPE]'}"
                       }, {"role": "user", "content": str(input)}]

    response_check = client.chat.completions.create(
        model='test-deployment',
        messages=messages_check,
        response_format={"type": "json_object"}
    )

    try:
        response_content_json = json.loads(response_check.choices[0].message.content)
        return response_content_json['is_correct_type']
    except ValueError as e:
        return False

