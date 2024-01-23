import json
import logging

from openai import AzureOpenAI


class UserInputLlmHelper:

    def __init__(self, azure_openai_client: AzureOpenAI, azure_openai_model: str):
        self.azure_openai_model = azure_openai_model
        self.azure_openai_client = azure_openai_client

    def clean_dish_name(self, user_request, language):
        lang_instruction = ""
        if language != "not known language":
            lang_instruction = f"Language of the dish is {language}, so please consider that language during evaluation."

        messages = [
            {
                "role": "system",
                "content": "You are an assistant that extracts dish name from the given text."

                           "Do not give other information in json."
                           "Do not give instructions or ingredients in json object."
                           "If you can find dish name, set 'is_valid' to true, and 'dish_name' to name of the dish."
                           "Otherwise set 'is_valid' to false, and 'dish_name' to \"not_stated\"."
                           "If so, set 'is_valid' false, and 'dish_name' \"not_stated\"."
                           # f"{lang_instruction}"
                           "You must give the list of ingredients using the following JSON schema."
                           "Do not put the resulting Json into ```json ``` code block."
                           "JSON schema:\n"
                           "{\"dish_name\": \"[DISH_NAME]\", \"is_valid\": [IS_VALID]}"
            },
            {
                "role": "user",
                "content": f"Extract the dish name from the following text: {user_request}"
            }
        ]

        return self.azure_openai_client.chat.completions.create(
            model=self.azure_openai_model,
            messages=messages,
            response_format={"type": "json_object"}
        )

    def clean_servings(self, user_request, language):

        FEW_SHOTS = [
            {"role": "user", "content": "Elf Touristen besuchten das Museum."},
            {"role": "assistant", "content": '{"number_of_people": "11", "is_valid": True}'},
            {"role": "user", "content": "Eight men go fishing"},
            {"role": "assistant", "content": '{"number_of_people": "8", "is_valid": True}'},
            {"role": "user", "content": "Beş adam kafede oturuyorlar."},
            {"role": "assistant", "content": '{"number_of_people": "5", "is_valid": True}'}
        ]

        messages = [
            {
                "role": "system",
                "content": "You are an assistant that gets number of people from the statement."
                           "Return json object which consists of 2 fields."
                           "These fields are 'is_valid' and 'number_of_people'"
                           "Do not give other information in json."
                           "If you can find number of people, set 'is_valid' true, and 'number_of_people' people count."
                           "If you can not find number of people, set 'is_valid' false, and 'number_of_people' not_stated."
                           "People count can be given such as '5 people', '3 men', '6 guests', '8 customers' or just '2000'. Always return just integer not other words."
                           "Number can be given as string, such as 'five', 'elf', 'elli' or 'zwei' etc. In that case, convert them to integer (5, 2 respectively) and set 'number_of_people'."
                           "If given value is not integer such as '3.5' or '4/5' etc.; set 'is_valid' false and 'number_of_people' not_stated."
                           # f"User input can be given any language such as 'five men', 'vier mensch' or 'bes kisi'. Consider {language} while responding."
                           "You must give the list of ingredients using the following JSON schema."
                           "Do not put the resulting Json into ```json ``` code block."
                           "JSON schema:\n"
                           "{\"number_of_people\": '[NUMBER_OF_PEOPLE]', \"is_valid\": [IS_VALID]}"
            },
            *FEW_SHOTS,
            {
                "role": "user",
                "content": f"Get the servings from the following paragraph: {user_request}"
            }
        ]

        return self.azure_openai_client.chat.completions.create(
            model=self.azure_openai_model,
            messages=messages,
            response_format={"type": "json_object"},
            top_p=0.2,
            temperature=0.1
        )

    def determine_language(self, user_request: str):
        messages = [
            {
                "role": "user",
                "content":
                    "You are an assistant that determines the language for a given text."
                    "Only if the input does not match with any language, return 'not known language'."
                    "Only return the language such as 'English', 'German'."
                    "Respond with 'English' if the input matches with multiple languages."
                    "If the input consists of only numbers, return 'not known language'. "
                    f"What language is the following text?: {user_request}."
            }
        ]

        response = self.azure_openai_client.chat.completions.create(
            model=self.azure_openai_model,
            messages=messages
        )
        return response

    def does_input_type_match(self, input, type, language):
        response = self.check_input_type_match(input, type, language)

        try:
            response_content_json = json.loads(response.choices[0].message.content)
            return response_content_json['is_correct_type']
        except ValueError as e:
            logging.debug(e)
            return False

    def check_input_type_match(self, input, type, language):
        FEW_SHOTS = [
            {"role": "user", "content": "'Eighty' is integer"},
            {"role": "assistant", "content": '{"is_correct_type": True}'},
            {"role": "user", "content": "'Sechzehn' is integer"},
            {"role": "assistant", "content": '{"is_correct_type": True}'},
            {"role": "user", "content": "'Yirmi dokuz' is integer"},
            {"role": "assistant", "content": '{"is_correct_type": True}'},
            {"role": "user", "content": "'Grilled chicken' is dish name"},
            {"role": "assistant", "content": '{"is_correct_type": True}'},
            {"role": "user", "content": "'Kartoffelsalat' is dish name"},
            {"role": "assistant", "content": '{"is_correct_type": True}'},
            {"role": "user", "content": "'Hamsi tava' is dish name"},
            {"role": "assistant", "content": '{"is_correct_type": True}'}
        ]


        messages = [
            {
                "role": "system",
                "content": f"You are an assistant that check if the given input is actually a {type} or not."
                           "Return json object which consists of 1 field called 'is_correct_type'."
                           f"Set 'is_correct_type' field true in boolean format if it is {type}."
                           f"Set 'is_correct_type' field false in boolean format if it is not {type}."
                           # f"Language of sentences (And numbers) can be given German, English or Turkish. So please consider all of these 3 languages."
                           # f"Language of the input is {language}, so please consider that language during type check."
                           "You must give the list of ingredients using the following JSON schema."
                           "Do not put the resulting Json into ```json ``` code block."
                           "JSON schema:\n"
                           "{\"is_correct_type\": [IS_CORRECT_TYPE]}"
            },
            *FEW_SHOTS,
            {
                "role": "user",
                "content": str(input)
            }
        ]

        return self.azure_openai_client.chat.completions.create(
            model=self.azure_openai_model,
            messages=messages,
            response_format={"type": "json_object"},
            top_p=0.2,
            temperature=0.1
        )
