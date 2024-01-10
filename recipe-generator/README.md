# Recipe Generator
The goal of this repository is to generate cooking recipes from a user input and then associate each ingredient of that recipe with a product in a product database. This is demonstrated in the following diagram.

![recipe_generator](/recipe-generator/images/recipe_generator.drawio.png)

## Creating the Recipe Database
To create the recipe database, you can run **recipe_db_generator.py**. It takes a list of recipe names from an already existing recipe database and generates recipes for them. There is a *NUMBER_OF_RECIPES* variable that determines how many recipes to generate.

## Using the Application
After creating the recipe database, you can run **main.py** with 2 parameters. One positional argument which is the **dish name**, and one optinal argument which is the **number of servings**. If no **number of servings** are provided a default value is used instead.