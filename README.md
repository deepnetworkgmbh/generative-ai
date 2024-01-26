# Generative AI
This repository contains projects that use LLMs. Some of these projects are mainly there to demonstrate different use-cases while others are more about the technologies and methods that can be used with LLMs. 

Brief descriptions of the projects are listed below, more details are available in the Readme files in the corresponding subfolders.

## General Concepts
This folder includes documentation about general LLM topics.

## Comment Reasoner
This project is showcase for summarization features of LLM. Common problems about a given product is listed by extracting information from the comments about the product. The comments in a marketplace (Trendyol) is retrieved and most common 3 problems are listed.

## (Prompt) Flow
This project demonstrates the implementation, testing and deployment of Azure Machine Learning Prompt Flow. and acts as a step-by-step guide on how to setup a prompt flow yourself.

## Retrieval Augmented Generation (RAG)
This project contains an example RAG application for a chatbot that helps employees of a company with their questions using company documents. This is done by searching through company documents with vector search and providing relevant parts to the LLM. For the search engine, Azure AI Search and Elasticsearch usage is demonstrated.

## Recipe Generation
The recipe generation project serves for two main use-cases:

* Recipe Generation (Recipe to Ingredients): The user provides the dish name and the number of servings, and receives the ingredients list as the output. The list includes the name and quantity (including unit) of each item.
* Ingredients to Recipe: The user is asked about their preferences by the chatbot and is offered a suitable recipe using mostly the ingredients they already have. Once the user agrees on the recipe, the missing ingredients list is created.

## Resume Parser
This project uses LLMs to extract only information we care about from any given resume. This is done through OpenAI Function Calling API.

## Speech to Text
This project uses Azure Speech-to-Text convert speech input to text. Then it showcases the differences in LLM behavior between asking questions directly to an LLM versus translating the questions to English with Azure AI Translation and then asking them.

## Useful links:
* [Introduction to AI with Azure](https://www.youtube.com/watch?v=CuUOt5djqSs)
* [Azure OpenAI Samples Repository](https://github.com/Azure/openai-samples)
* [How Transformers Work](https://www.youtube.com/watch?v=4Bdc55j80l8)
