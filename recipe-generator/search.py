from sentence_transformers import SentenceTransformer, util
from embeddings import *

def search_in_products(query_product_name):
    if index:=__search_in_embeddings(query_product_name, product_embeddings):
        return [product_names[index], product_ids[index]]
    return None

def search_in_removal_list(query_product_name):
    if __search_in_embeddings(query_product_name, removal_list_embeddings) is None:
        return False
    return True

def search_in_recipe_db(query_product_name):
    if index:=__search_in_embeddings(query_product_name, recipe_embeddings):
        return recipes[index]
    return None

def __search_in_embeddings(query, embeddings, threshold=0.7):
    query_embedding = model.encode(query.lower())
    cos_sim = util.cos_sim(embeddings, query_embedding)
    results = []
    for i in range(len(cos_sim)):
        results.append(cos_sim[i][0])
    max_similarity_score = max(results)
    if max_similarity_score.item() < threshold:
        return None
    return results.index(max_similarity_score)