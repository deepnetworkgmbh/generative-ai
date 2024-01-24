# LLM Fine-Tuning

Fine-tuning an LLM is the process of further training a pre-trained model with a well-crafted dataset to increase its performance in a specific task or domain. A fine-tuned model can outperform its base version in terms of both computational costs and latency on the task it specializes in by using fewer tokens in the prompt. However the fine-tuning process can be both expensive and time-consuming depending on the model size and the method used. For this reason it is generally a good idea to try prompt engineering techniques such as "few-shot learning" first and only move onto fine-tuning if the results are not satisfactory.

### When to Use

+ Cannot get good enough results with prompt engineering
+ Want to lower latency and costs by using a smaller model while maintaining output quality
+ Need best performance for a specific task
+ Context size is not enough to fit all of the few-shots

### When **not** to Use

+ Have not tried prompt engineering
+ Working with user data
+ Up-to-date data requirements
+ Not enough available domain-specific data 
+ Need general purpose capabilities

## Fine-Tuning OpenAI Models

OpenAI makes the fine-tuning process very simple. You only need to prepare the dataset for fine-tuning and they handle the rest of it. While this makes it very approachable for even people without any ML experience, it is also quite constraining. The only hyperparameters you can change in the fine-tuning process are:

+ **Number of epochs:** An epoch is a full pass of the training dataset
+ **Learning rate multiplier:** How much the model weights change with each error
+ **Batch size:** Number of dataset samples to go through before updating model weights

It is also not possible to change the fine-tuning method when using OpenAI models. More information on fine-tuning OpenAI models can be found on the [OpenAI fine-tuning guide](https://platform.openai.com/docs/guides/fine-tuning/fine-tuning).

An interesting article comparing the performance, cost and latencies of different fine-tuned OpenAI models for generating code blocks for Flyde can be found [here](https://betterprogramming.pub/openai-api-fine-tuned-models-vs-chat-completion-a-case-study-e3774fadc8c7). Keep in mind that this article is old and use some deprecated models. So prices on the article may not reflect current prices. There is also a [follow-up article](https://medium.com/@gabrielgrinberg/openai-api-fine-tuned-gpt-3-5-vs-base-gpt-3-5-a-case-study-f3619b4f8cd8) that adds the fine tuning of gpt-3.5-turbo as well.

### Preparing the Dataset

OpenAI suggest a dataset with **50-100** examples is a good place to start with fine-tuning. The model can later be further fine-tuned with more data if the results are not sufficient. When crafting the dataset OpenAI recommends:

+ Prioritize quality over quantity
+ Have a diverse set of examples
+ Include edge cases

One thing to keep in mind is that each example should not exceed the context size of the model, or they will be truncated to fit the context.

### OpenAI Pricing

When fine-tuning OpenAI models, there are two types of costs to keep in mind: **initial cost of training** and **cost of using the model**. Initial cost can be calculated by:
    
    base cost per 1k tokens * number of tokens in the input file * number of epochs

Below is an example fine-tuning cost with gpt-3.5-turbo:

![fine-tuning cost with gpt-3.5-turbo](/recipe_generation/images/gpt-3.5-turbo-fine-tuning.png)

Cost of using the fine-tuned models is much more expensive compared to the base models. But one important thing to keep in mind is that a smaller fine-tuned model can have similar output quality to a larger model. Below table shows average costs for **base gpt-3.5-turbo**, **fine-tuned gpt-3.5-turbo** and **gpt-4-turbo**:

![average cost table](/recipe_generation/images/model-costs-per-month.png)

As we can see from the table, it is much cheaper to run a **fine-tuned gpt-3.5-turbo** compared to **base gpt-4-turbo**, if it can reach the desired quality. It is also important to keep in mind that since smaller models run faster, **fine-tuned gpt-3.5-turbo** will have lower latencies.

### Azure OpenAI Pricing

Pricing of Azure OpenAI service is different compared to OpenAI pricing. Current fine-tuning pricing for Azure can be seen below:

![Azure cost table](/recipe_generation/images/azure-costs.png)

Main differences are that costs for fine-tuning are not in tokens but instead in **compute hours**, and running fine tuned models has a **fixed hosting cost** as well as **per 1k token cost**. Upside of using Azure is that the **per 1k token cost** in Azure is much cheaper. This makes it cheaper overall if you are using more than **~2.5 million tokens per hour**.

## Fine-Tuning Strategies
There are many different methods to choose from when fine-tuning