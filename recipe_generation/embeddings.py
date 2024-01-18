import json

from sentence_transformers import SentenceTransformer

from recipe_constants import *


class Embeddings:
    product_names = []
    product_ids = []
    product_embeddings = []
    removal_list_embeddings = []
    recipes = []
    recipe_embeddings = []
    ingredients_at_home_embeddings = []

    def __init__(self):
        self.__model = SentenceTransformer('all-mpnet-base-v2')
        self.embed_product_db()
        self.embed_removal_list()
        self.embed_recipe_db()

    def embed_product_db(self):
        with open(PRODUCT_DB_PATH, 'r') as file:
            db = json.load(file)
            for product in db["products"]:
                self.product_names.append(product["name"])
                self.product_ids.append(product["id"])

        self.product_embeddings = self.__model.encode(self.product_names)

    def embed_recipe_db(self):
        recipe_names = []
        with open(RECIPE_DB_PATH, 'r') as file:
            db = json.load(file)
            for recipe in db:
                self.recipes.append(recipe)
                recipe_names.append(recipe["name"])

        self.recipe_embeddings = self.__model.encode(recipe_names)

    def embed_removal_list(self):
        with open(REMOVAL_LIST_PATH, 'r') as file:
            removal_list = json.load(file)
            self.removal_list_embeddings = self.__model.encode(removal_list)

    def embed_ingredients_at_home(self):
        with open(INGREDIENTS_AT_HOME, 'r') as file:
            ingredients_at_home = json.load(file)
            self.ingredients_at_home_embeddings = self.__model.encode(ingredients_at_home)

    def encode(self, input):
        return self.__model.encode(input)