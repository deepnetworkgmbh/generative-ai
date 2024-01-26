# RAG (Retrieval Augmented Generation)

## RAG (Retrieval Augmented Generation) vs Fine Tuning:

If you are working with LLMs, fine tuning is mainly used when you need to change the behaviour or style of the LLM. It can also be useful when working with smaller models. RAG is mainly useful when working with dynamic data. It allows you to add your own data to the context when working with LLMs. It also increases the credibility of the LLM and reduces hallucinations. These two techniques can also be used together when necessary. More info can be found [here](https://www.rungalileo.io/blog/optimizing-llm-performance-rag-vs-finetune-vs-both) and [here](https://www.tidepool.so/2023/08/17/.why-you-probably-dont-need-to-fine-tune-an-llm/)

## Azure AI Search

Azure AI Search is a service that provides indexing and querying capabilities. In the context of LLMs this service is very useful when using **RAG**.

### Access Control

Access control in Azure AI Search can be achieved in 3 levels. These are:

* **Service Level Access Control:** It controls access to the whole Azure AI Search instance. You can use **API Keys** or **Azure RBAC**.

* **Index Level Access Control:** It controls access to the certain indices for the given users. This can only be achieved with **RBAC**. However, the configuration cannot be done on Azure Portal, and is only done through **Powershell** or **Azure CLI**.

* **Document Level Access Control:** This scenario involves limiting the returned search results per user/role. However this is not natively supported in **Azure AI Search**, but it can be achieved using [filtering](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search).

More information on security of Azure AI Search can be found [here](https://learn.microsoft.com/en-us/azure/search/search-security-overview#authorize-service-management).

### Pricing
Azure AI Search prices can be calculated with the below formula:
```
price = (number of partitions) x (number of replicas) x (price per SU (Scale Unit))
```

Price per SU is determined depending on the SKU level of the service. As the SKU level increases, the storage amount and replica count of the service increases.

For high availability Microsoft recommends at least 2 replicas. As a result, Azure AI Search can get quite expensive as the storage size increases.

There is also extra costs if you want to use [Custom Entity Lookup Skill](https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-custom-entity-lookup), [Image Extraction](https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-document-extraction) or [Semantic Ranker](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview).

## Azure AI Search RAG
This images shows a way to use Azure AI Search for RAG purposes. This is the flow used in [azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo) repository by Microsoft.

![Azure AI Search RAG flow](images/RAG%20flow.drawio.png)

When using Azure AI Search [this](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167) might be helpful to decide on which searching method to use.

## Elasticsearch RAG
We tried to create a similar flow to the one in the Azure AI Search example. For more information, please check [Elasticsearch README.md](elastic_search/README.md).