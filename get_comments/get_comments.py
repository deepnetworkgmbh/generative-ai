import json
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from re import search, match


def get_comments_link_for_product(query):
    # Encode the query string in HTML encoding
    encoded_query = quote(query)

    # Form the URL
    url = f"https://www.trendyol.com/sr?q={encoded_query}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the element with class "prdct-cntnr-wrppr"
    if parent_element := soup.find(class_="prdct-cntnr-wrppr"):
        # Find all elements with class "p-card-wrppr with-campaign-view" within the parent element
        if child_elements := parent_element.find_all(class_="p-card-wrppr with-campaign-view"):
            # Iterate through child elements to find the first one containing an element with "ratings-container" class
            for child in child_elements:
                if ratings_container := child.find(class_="ratings"):
                    # Find the <a> element within the first matching child
                    if link_element := child.find('a'):
                        # Extract and print the link (href) of the <a> element
                        link = link_element.get('href')
                        link = link.replace("?", "/yorumlar?")
                        link = f"https://www.trendyol.com{link}"
                        print(link)
                        return link
            else:
                print("No matching child element found.")
        else:
            print("No child elements found with specified class.")
    else:
        print("Parent element not found.")

    return None


def get_comment_texts(comments_link):
    # Send a GET request to the URL
    response = requests.get(comments_link)
    print(response.content)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    comment_texts = []

    if parent_element := soup.find(class_="reviews"):
        # Find all elements with class "p-card-wrppr with-campaign-view" within the parent element
        if child_elements := parent_element.find_all(class_="comment-text"):
            for child in child_elements:
                if p_element := child.find('p'):
                    print(p_element)
                    comment_texts.append(p_element)
        else:
            print("No child elements found with specified class.")
    else:
        print("Parent element not found.")

    return comment_texts


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


ayristir = lambda berisi, gerisi, yazi: search(f'{berisi}(.*){gerisi}', yazi).group(1)


def get_comments(product_id, product_url):
    print("Product ID:", product_id)
    try:
        product_url, _ = product_url.split("?")
    except ValueError:
        product_url = product_url
    print("Product URL:", product_url)
    comments_url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/reviews/{product_url}/yorumlar"

    kimlik = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    response = requests.get(comments_url, headers=kimlik)
    content_json = json.loads(response.content)
    comments_section = json.loads(ayristir("STATE__ = ", ";", content_json['result']['hydrateScript']))
    comments_data = comments_section['ratingAndReviewResponse']['ratingAndReview']['productReviews']['content']
    return [
        {
            'tarih': comment['lastModifiedDate'],
            'satici': comment['sellerName'],
            'kullanici': comment['userFullName'],
            'yildiz': comment['rate'],
            'yorum': comment['comment']
        }
        for comment in comments_data
    ]


# Given query string
query = "iphone 15"

product = get_product_with_rating(query)
comments = get_comments(product['id'], product['url'])

print("comments:", comments)

# comments_link = get_comments_link_for_product(query)
# comments = get_comment_texts(comments_link)
