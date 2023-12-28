Useful links:
* https://www.youtube.com/watch?v=CuUOt5djqSs
* https://github.com/Azure/openai-samples
* [How Transformers work](https://www.youtube.com/watch?v=4Bdc55j80l8)
* https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167

## RAG (Retrieval Augmented Generation) vs Fine Tuning:

If you are working with LLMs, fine tuning is mainly used when you need to change the behaviour or style of the LLM. It can also be useful when working with smaller models. RAG is mainly useful when working with dynamic data. It allows you to add your own data to the context when working with LLMs. It also increases the credibility of the LLM and reduces hallucinations. These two techniques can also be used together when necessary. More info can be found [here](https://www.rungalileo.io/blog/optimizing-llm-performance-rag-vs-finetune-vs-both) and [here](https://www.tidepool.so/2023/08/17/.why-you-probably-dont-need-to-fine-tune-an-llm/)

## Prompt Engineering
To improve the quality of the output you can:
* Put the instructions in the beginning instead of the end (Does not matter with GPT-4)

* Instruct the model to provide predefined replies based on specific conditions or situations (System message).

* Give prompt-completion examples in the prompt (Few-shot learning)
* Put a few words at the end of the prompt to get output in desired format (Priming)
* Use clear syntax
* Break down the task into smaller steps
* Provide grounding data

More information can be found [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/advanced-prompt-engineering?pivots=programming-language-chat-completions).

## Azure AI Search
Azure AI Search is a service that provides indexing and querying capabilities. In the context of LLMs this service is very useful when using **RAG**. 


### Access Control
Access control in Azure AI Search can be achieved in 3 levels. These are:
* **Service Level Access Control:** It controls access to the whole Azure AI Search instance. You can use **API Keys** or **Azure RBAC**.

* **Index Level Access Control:** It controls access to the certain indices for the given users. This can only be achieved with **RBAC**. However, the configuration cannot be done on Azure Portal, and is only done through **Powershell** or **Azure CLI**.

* **Document Level Access Control:** This scenario involves limiting the returned search results per user/role. However this is not natively supported in **Azure AI Search**, but it can be achieved using [filtering](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search).


More information on Azure AI Search can be found [here](https://learn.microsoft.com/en-us/azure/search/search-security-overview#authorize-service-management).

### Pricing
Azure AI Search prices can be calculated with the below formula:

    price = # of partitions x # of replicas x price per SU

For high availability Microsoft recommends at least 2 replicas. As a result, Azure AI Search can get quite expensive as the storage size increases.

There is also extra costs if you want to use [Custom Entity Lookup Skill](https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-custom-entity-lookup), [Image Extraction](https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-document-extraction) or [Semantic Ranker](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview).