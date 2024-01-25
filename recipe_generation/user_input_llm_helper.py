import json
import logging
from enum import Enum
from copy import deepcopy

from openai import AzureOpenAI


class Language(Enum):
    ENGLISH = 1
    GERMAN = 2
    TURKISH = 3


class UserInputType(Enum):
    DISH_NAME = 1
    SERVINGS = 2


CLEAN_SERVINGS_MESSAGES = {
    Language.ENGLISH: [
        {
            "role": "system",
            "content": """From now on I will give you a text and you will find the number in the given text and give me the number in numeric form. 
                If you can find number, set 'is_valid' to true, and 'number' to number.
                Otherwise set 'is_valid' to false, and 'number' to \"not_stated\".
                Do not put the resulting Json into ```json ``` code block.
                JSON schema:
                {\"number\": \"[number]\", \"is_valid\": [IS_VALID]}"""
        },
        {
            "role": "user",
            "content": "Get the number from this text: {user_request}"
        }],
    Language.GERMAN: [
        {
            "role": "system",
            "content": """Von nun an werde ich Ihnen einen Text geben und Sie werden die Nummer im angegebenen Text finden und mir die Nummer in numerischer Form geben.
                Wenn Sie die Zahl finden können, setzen Sie 'is_valid' auf true und 'number' auf den nummer.
                Andernfalls setzen Sie 'is_valid' auf false und 'number' auf \"not_stated\".
                Fügen Sie den resultierenden JSON nicht in den Codeblock ```json ``` ein.
                JSON schema:
                {\"number\": \"[nummer]\", \"is_valid\": [IS_VALID]}"""
        },
        {
            "role": "user",
            "content": "Holen Sie sich die Nummer aus diesem Text: {user_request}"
        }],
    Language.TURKISH: [
        {
            "role": "system",
            "content": """Bundan sonra sana bir metin vereceğim ve sen de verilen metindeki sayıyı bulup bana sayısal biçimde vereceksin.
                Cevap verirken aşağıdaki json şemasını kullan.
                {\"number\": \"[SAYI]\", \"is_valid\": [IS_VALID]}
                Eğer metinde sayı varsa, 'is_valid' değerini true olarak ve 'number' değerini bulduğun sayı olarak ayarla.
                Eğer metinde sayı yoksa 'is_valid' değerini false olarak ve 'number' değerini \"not_stated\" olarak ayarla.
                Ortaya çıkan Json'u ```json ``` kod bloğuna koyma."""
        },
        {
            "role": "user",
            "content": "Verilen metindeki sayıyı bul: {user_request}"
        }]
}

CLEAN_DISH_NAME_MESSAGES = {
    Language.ENGLISH: [
        {
            "role": "system",
            "content":"""From now on I will give you a text and you will find the dish name in the given text and give me the dish name.
                If you can find dish name, set 'is_valid' to true, and 'dish_name' to name of the dish.
                Otherwise set 'is_valid' to false, and 'dish_name' to \"not_stated\".
                Do not put the resulting Json into ```json ``` code block.
                JSON schema:
                {\"dish_name\": \"[DISH_NAME]\", \"is_valid\": [IS_VALID]}"""
        },
        {
            "role": "user",
            "content": "Find the name of the dish in the given text: {user_request}"
        }],
    Language.GERMAN: [
        {
            "role": "system",
            "content": """From now on I will give you a text and you will find the dish name in the given text and give me the dish name.
                If you can find dish name, set 'is_valid' to true, and 'dish_name' to name of the dish.
                Otherwise set 'is_valid' to false, and 'dish_name' to \"not_stated\".
                Do not put the resulting Json into ```json ``` code block.
                JSON schema:
                {\"dish_name\": \"[DISH_NAME]\", \"is_valid\": [IS_VALID]}"""
        },
        {
            "role": "user",
            "content": "Finden Sie den Namen des Lebensmittels im angegebenen Text: {user_request}"
        }],
    Language.TURKISH: [
        {
            "role": "system",
            "content": """Bundan sonra sana bir metin vereceğim ve sen de verilen metinde yemeğin adını bulup bana yemeğin adını vereceksin.
                Eğer metinde yemek ismi varsa, 'is_valid'i true olarak ve 'dish_name'i yemeğin adı olarak ayarla.
                Eğer metinde yemek ismi yoksa 'is_valid'i false ve 'dish_name'i \"not_stated\" yap.
                Ortaya çıkan Json'u ```json ``` kod bloğuna koyma.
                JSON schema:
                {\"dish_name\": \"[DISH_NAME]\", \"is_valid\": [IS_VALID]}"""
        },
        {
            "role": "user",
            "content": "Verilen metindeki yemek ismini bul: {user_request}"
        }]
}

VALIDATION_MESSAGES_DISH_NAME = {
    Language.ENGLISH: [
        {
            "role": "system",
            "content":"""Starting now, I'll provide you with text, and your task is to determine whether the given text represents a dish or not.
                If the text is a dish name, set the 'is_correct_type' field to true.
                If the text is not a dish name, set the 'is_correct_type' field to false.
                Ensure the resulting JSON follows this schema:
                {\"is_correct_type\": [IS_CORRECT_TYPE]}"""
        },
        {
            "role": "user",
            "content": "{input}"
        }
    ],
    Language.GERMAN: [
        {
            "role": "system",
            "content":"""Ab sofort werde ich Ihnen einen Text geben, und Ihre Aufgabe ist es festzustellen, ob der gegebene Text ein Gericht repräsentiert oder nicht.
                Falls der Text den Namen eines Gerichts darstellt, setzen Sie das Feld 'is_correct_type' auf true.
                Falls der Text keinen Gerichtsnamen darstellt, setzen Sie das Feld 'is_correct_type' auf false.
                Stellen Sie sicher, dass das resultierende JSON diesem Schema folgt:
                {\"is_correct_type\": [IS_CORRECT_TYPE]}"""
        },
        {
            "role": "user",
            "content": "{input}"
        }
    ],
    Language.TURKISH: [
        {
            "role": "system",
            "content":"""Artık size bir metin vereceğim ve verilen metnin bir yemek olup olmadığını belirlemeniz gerekecek.
                Eğer metin bir yemek adını temsil ediyorsa, 'is_correct_type' alanını true olarak ayarlayın.
                Eğer metin bir yemek adı değilse, 'is_correct_type' alanını false olarak ayarlayın.
                Sonuçlanan JSON'un şu şemaya uymasını sağlayın:
                {\"is_correct_type\": [IS_CORRECT_TYPE]}"""
        },
        {
            "role": "user",
            "content": "{input}"
        }
    ]
}

VALIDATION_MESSAGES_SERVINGS_COUNT = {
    Language.ENGLISH: [
        {
            "role": "system",
            "content":"""Starting now, I'll provide you with text, and your task is to determine whether the given text represents a number.
                It can be a number in text (e.g. twenty five) or numerical form (25).
                If the text is a representation of a number, set the 'is_correct_type' field to true.
                Otherwise, set the 'is_correct_type' field to false.
                Ensure the resulting JSON follows this schema:
                {\"is_correct_type\": IS_CORRECT_TYPE}"""
        },
        {
            "role": "user",
            "content": "{input}"
        }],
    Language.GERMAN: [
        {
            "role": "system",
            "content":"""Ab sofort werde ich Ihnen Texte zur Verfügung stellen, und Ihre Aufgabe besteht darin, festzustellen, ob der gegebene Text eine Zahl darstellt.
             Es kann sich um eine Zahl im Text handeln (z.B. fünfundzwanzig) oder in numerischer Form (25).
             Wenn der Text eine Darstellung einer Zahl ist, setzen Sie das Feld 'is_correct_type' auf true. 
             Andernfalls setzen Sie das Feld 'is_correct_type' auf false. 
             Stellen Sie sicher, dass das resultierende JSON diesem Schema folgt:
                {\"is_correct_type\": IS_CORRECT_TYPE}"""
        },
        {
            "role": "user",
            "content": "{input}"
        }],
    Language.TURKISH: [
        {
            "role": "system",
            "content":"""Bundan sonra sana bir metin vereceğim ve senin görevin verilen metnin bir sayıyı temsil edip etmediğini belirlemektir.
                Metin, rakamsal (25) ya da yazılı (yirmi beş) olarak sayı içerebilir.
                Eğer metin bir sayıyı ifade ediyorsa, 'is_correct_type' alanını true olarak ayarla.
                Aksi halde, 'is_correct_type' alanını false olarak ayarla.
                Sonuçlanan JSON'un şu şemaya uymasını sağla:
                {\"is_correct_type\": IS_CORRECT_TYPE}
                """
        },
        {
            "role": "user",
            "content": "{input}"
        }]
}

class UserInputLlmHelper:

    def __init__(self, azure_openai_client: AzureOpenAI, azure_openai_model: str):
        self.azure_openai_model = azure_openai_model
        self.azure_openai_client = azure_openai_client

    def clean_dish_name(self, user_request, language: Language):
        messages = CLEAN_DISH_NAME_MESSAGES[language]
        messages[1]['content'] = messages[1]['content'].format(user_request=user_request)

        return self.azure_openai_client.chat.completions.create(
            model=self.azure_openai_model,
            messages=messages,
            response_format={"type": "json_object"}
        )

    def clean_servings(self, user_request, language: Language):
        messages = CLEAN_SERVINGS_MESSAGES[language]
        messages[1]['content'] = messages[1]['content'].format(user_request=user_request)

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

    def does_input_type_match(self, input, type: UserInputType, language: Language):
        response = self.check_input_type_match(input, type, language)

        try:
            response_content_json = json.loads(response.choices[0].message.content)
            return response_content_json['is_correct_type']
        except ValueError as e:
            logging.debug(e)
            return False

    def check_input_type_match(self, input, type: UserInputType, language: Language):
        if type == UserInputType.DISH_NAME:
            messages = deepcopy(VALIDATION_MESSAGES_DISH_NAME[language])
        else:
            messages = deepcopy(VALIDATION_MESSAGES_SERVINGS_COUNT[language])
        messages[1]['content'] = messages[1]['content'].format(input=input)

        print(messages[0]['content'])
        print(messages[1]['content'])
        return self.azure_openai_client.chat.completions.create(
            model=self.azure_openai_model,
            messages=messages,
            response_format={"type": "json_object"},
            top_p=0.1,
            temperature=0.1
        )
