# Prompt Engineering

To improve the quality of the output you can:

* Put the instructions in the beginning instead of the end (Does not matter with GPT-4)

* Instruct the model to provide predefined replies based on specific conditions or situations (System message).

* Give prompt-completion examples in the prompt (Few-shot learning)
* Put a few words at the end of the prompt to get output in desired format (Priming)
  * Example:
    * System message: You are an AI assistant that helps people find information. Answer in as few words as possible.
    * User: John Smith is married to Lucy Smith. They have five kids, and he works as a software engineer at Microsoft. What search queries should I do to fact-check this? One possible search query is:
    * Assistant: "John Smith married Lucy Smith five kids software engineer Microsoft"

  * "One possible search query is" part **primes** the model to produce a single output.

* Use clear syntax
* Break down the task into smaller steps
* Provide grounding data

More information can be found [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/advanced-prompt-engineering?pivots=programming-language-chat-completions).
