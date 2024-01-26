# Generative AI
This repository contains projects that use LLMs. Some of these projects are mainly there to demonstrate different use-cases while others are more about the technologies and methods that can be used with LLMs. There will a brief description about each of the projects below and more details are available on the Readme files of the subfolders.

## General Concepts
This folder includes markdown files containing information about general topics that do not fit into any of the projects.

## Comment Reasoner
This project tries to summarize common problems about a given product using an LLM. The LLM looks at the comments in a marketplace(Trendyol) to find these problems.

## Prompt Flow
This project demonstrates the benefits of using Azure Machine Learning Prompt Flow and acts as a step-by-step guide on how to setup a prompt flow yourself.

## Retrieval Augmented Generation (RAG)
This project contains an example RAG application for a chatbot that helps employees of a company with their questions using company documents. This is done by searching through company documents with vector search and providing relevant parts to the LLM. Elasticsearch is used to host the document index.

## Recipe Generation
The goal of this project is to generate recipes for any dish the user asks with LLMs. After taking input from user in speech or text format and sanitizing it, the application generates a recipe by using LLMs. Then each ingredient in the recipe is associated with a product in a product database.

There is also a second interface for the application that takes the ingredients the user has
and generates a dish mostly using those ingredients in a similar manner. Then the user is shown the missing ingredients in the recipe.

## Resume Parser
This project uses LLMs to extract only information we care about from any given resume. This is done through OpenAI Function Calling API.

## Speech to Text
This project uses Azure Speech-to-Text convert speech input to text. Then it showcases the differences in LLM behavior between asking questions directly to an LLM versus translating the questions to English with Azure AI Translation and then asking them.

## Useful links:
* [Introduction to AI with Azure](https://www.youtube.com/watch?v=CuUOt5djqSs)
* [Azure OpenAI Samples Repository](https://github.com/Azure/openai-samples)
* [How Transformers Work](https://www.youtube.com/watch?v=4Bdc55j80l8)
