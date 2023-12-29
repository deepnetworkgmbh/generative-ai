import json
import os
from urllib.parse import quote
import requests
from re import search, match

from openai import AzureOpenAI, ChatCompletion
from openai import OpenAI


def get_product_with_rating(query):
    # Encode the query string in HTML encoding
    encoded_query = quote(query)
    url = f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/filter/sr?q={encoded_query}"
    # Send a GET request to the URL
    response = requests.get(url)

    data = json.loads(response.content)

    # Access the "products" list
    products = data.get("result", {}).get("products", [])

    # Find the first element in products with a "ratingScore" element
    first_with_rating_score = next(
        (product for product in products if "ratingScore" in product),
        None
    )

    if first_with_rating_score:
        # Access the details of the first element with a "ratingScore"
        print(first_with_rating_score)
        return first_with_rating_score
    else:
        print("No element found with a 'ratingScore' element.")
        return None


def get_comments(product_id, product_url, page):
    #print("Product ID:", product_id)
    try:
        product_url, _ = product_url.split("?")
    except ValueError:
        product_url = product_url
    #print("Product URL:", product_url)
    comments_url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/reviews{product_url}/yorumlar?page={page}"

    kimlik = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}

    response = requests.get(comments_url, headers=kimlik)
    content_json = json.loads(response.content)

    hydrate_script_section = search(f'STATE__ = (.*);', content_json['result']['hydrateScript']).group(1)
    hydrate_script_section_json = json.loads(hydrate_script_section)

    comments_section = hydrate_script_section_json['ratingAndReviewResponse']['ratingAndReview']['productReviews']
    total_pages = comments_section['totalPages']
    comments_content = comments_section['content']
    comments = [
        {
            'tarih': comment['lastModifiedDate'],
            'satici': comment['sellerName'],
            'kullanici': comment['userFullName'],
            'yildiz': comment['rate'],
            'yorum': comment['comment']
        }
        for comment in comments_content if comment['rate'] < 5
    ]
    if total_pages > page + 1:
        comments += get_comments(product_id, product_url, page+1)
    return comments


def ask_gpt(type, messages):
    if type == 'azure':
        openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2023-12-01-preview",
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        response = openai_client.chat.completions.create(
            model="test-deployment",
            messages=messages
        )
        return response.choices[0].message
    elif type == 'openai':
        openai_client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY']
        )
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo-0301",
            messages=messages
        )
        return response.choices[0].message
    elif type == 'ollama':
        response = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": "llama2:13b", "messages": messages, "stream": False},
        )
        return json.loads(response.content)['message']


query = input("Enter the product name and model you would like to search for: ")
product = get_product_with_rating(query)
comments = get_comments(product['id'], product['url'], page=0)
pure_comments = [comment['yorum'] for comment in comments]
message_content = f"PRODUCT: {query}\n" + '\n'.join(pure_comments)
print("User comments: \n\n" + message_content)
print("--------------------------------------")

messages=[
    {"role": "system", "content": "You are an expert that reads user comments and point out 3 main problems that the users have experienced about the product."
                                  "User will give you a list comments for the product."
                                  "Tell up to 3 main problems as bullets points."
                                  "Tell problems only about the product. Don't list problems about delivery or seller communication."
                                  "Don't give explanations before the problems, just list the problems."
                                  "Try to give detail about the problem. Don't use other information, just use the information in the comments."
                                  "If you cannot infer any problems, return None as message content."
                                  "Product name will be given as PRODUCT:product name in the user's message."},
    {"role": "user", "content": message_content}
]

azure_message = ask_gpt("azure", messages)
ollama_message = ask_gpt("ollama", messages)

print(f"Azure AI says:\n{azure_message.content}")
print("--------------------------------------")
print(f"Ollama says:\n{ollama_message['content']}")
