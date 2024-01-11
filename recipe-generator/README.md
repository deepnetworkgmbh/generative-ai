# Recipe Generator
The goal of this repository is to generate cooking recipes from a user input and then associate each ingredient of that
recipe with a product in a product database. This is demonstrated in the following diagram.

![recipe_generator](images/recipe_generator.drawio.png)

## Prerequisites
The application depends on Azure OpenAI deployment. Therefore, you need to set the `AZURE_OPENAI_API_KEY` and the
`AZURE_OPENAI_ENDPOINT` environment variables accordingly. The values can be found in the "Key and Endpoint" section
of your Azure OpenAI resource.
The application also needs the deployment name as the `AZURE_OPENAI_GPT_DEPLOYMENT` environment variable. It the deployment
name in your Azure OpenAI instance that has a GPT-3.5 or GPT-4 model.

The application includes speech-to-text function. It uses Azure AI Speech service. Once the service is created, please 
set the `SPT_API_KEY` and `SPT_REGION` environment variables that you can get the values from the Keys and Endpoints page
of the service.

## Using the Application
The `main.py` script is the entry-point of the application. 
First script will ask user to choose one of the input options ('Speech' or 'Text'). 
For the "Speech" option, three languages (English, German and Turkish) are supported. 
For the "Text" option, you can enter text in any language. 
The inputs do not need to be clean. i.e. you can give sentence as input for both dish name and serving count, 
such as 'I want to cook pizza'; system will extract dish name from the sentence.

Once the inputs are get, it will search within the recipe db. If the recipe does not exist in the db, it asks Azure OpenAI
to get the recipe. 

Subsequently, it adjusts the ingredients quantity to the servings size accordingly. Finally, it returns the ingredients as
a JSON text.

## Creating/Updating the Recipe Database
The application uses the `data/new-recipe-db.json` file as the recipe database. It is created using the `data/existing-recipes-db.json`.
The `recipe_db_generator.py` script uses LLM to convert from the existing db to the new db format.
We kept existing db and the script to showcase the possibility of converting any existing recipe db to the required format.

The script takes a list of recipe names from an already existing recipe database and generates recipes for them.
There is a *NUMBER_OF_RECIPES* variable in the script that determines how many recipes to generate. We kept it low for
minimizing the cost.
