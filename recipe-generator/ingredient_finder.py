import json
from sentence_transformers import SentenceTransformer, util

__model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

def embed_db(file):
    product_names = []
    product_ids = []
    with open(file, 'r') as file:
        db = json.load(file)
        for product in db["products"]:
            product_names.append(product["name"])
            product_ids.append(product["id"])

    return product_ids, product_names, __model.encode(product_names)

def embed_removal_list(file):
    with open(file, 'r') as file:
        removal_list = json.load(file)
        return __model.encode(removal_list)

def search_in_products(query_product_name):
    return __search_in_embeddings(query_product_name, __product_embeddings, __product_names, __product_ids)

def search_in_removal_list(query_product_name):
    if __search_in_embeddings(query_product_name, __removal_list_embeddings) is None:
        return False
    return True

def __search_in_embeddings(query_product_name, list_embeddings, *lists_to_append):
    query_embedding = __model.encode(query_product_name.lower())
    cos_sim = util.cos_sim(list_embeddings, query_embedding)
    results = []
    for i in range(len(cos_sim)):
        cur_result = [cos_sim[i][0]]
        for j in lists_to_append:
            cur_result.append(j[i])
        results.append(cur_result)
    results = sorted(results, key=lambda x: x[0], reverse=True)
    if results[0][0].item() < 0.7:
        return None
    return results[0]

__product_ids, __product_names, __product_embeddings = embed_db("./recipe-generator/product_names_en.json")
__removal_list_embeddings = embed_removal_list("./recipe-generator/removal-list.json")