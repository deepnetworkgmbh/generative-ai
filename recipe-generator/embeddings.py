import json
from sentence_transformers import SentenceTransformer

PRODUCT_DB_PATH = "./recipe-generator/product_names.json"
RECIPE_DB_PATH = "./recipe-generator/new-recipe-db.json"
REMOVAL_LIST_PATH = "./recipe-generator/removal-list.json"

model = SentenceTransformer('all-mpnet-base-v2')

def embed_product_db():
    product_names = []
    product_ids = []
    with open(PRODUCT_DB_PATH, 'r') as file:
        db = json.load(file)
        for product in db["products"]:
            product_names.append(product["name"])
            product_ids.append(product["id"])

    return product_ids, product_names, model.encode(product_names)

def embed_recipe_db():
    recipes = []
    recipe_names = []
    with open(RECIPE_DB_PATH, 'r') as file:
        db = json.load(file)
        for recipe in db:
            recipes.append(recipe)
            recipe_names.append(recipe["name"])

    return recipes, model.encode(recipe_names)

def embed_removal_list():
    with open(REMOVAL_LIST_PATH, 'r') as file:
        removal_list = json.load(file)
        return model.encode(removal_list)

product_ids, product_names, product_embeddings = embed_product_db()
removal_list_embeddings = embed_removal_list()
recipes, recipe_embeddings = embed_recipe_db()