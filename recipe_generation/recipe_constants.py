import os

DEFAULT_NUMBER_OF_SERVINGS = 4

file_dir = os.path.dirname(os.path.abspath(__file__))
PRODUCT_DB_PATH = f"{file_dir}/data/product_names.json"
RECIPE_DB_PATH = f"{file_dir}/data/new-recipe-db.json"
REMOVAL_LIST_PATH = f"{file_dir}/data/removal-list.json"
INGREDIENTS_AT_HOME = f"{file_dir}/data/ingredients_at_home.json"
