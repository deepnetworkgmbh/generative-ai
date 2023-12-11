Useful links:
* https://www.youtube.com/watch?v=CuUOt5djqSs
* https://github.com/Azure/openai-samples
* [How Transformers work](https://www.youtube.com/watch?v=4Bdc55j80l8)

## RAG vs Fine Tuning:
If you are working with LLMs, fine tuning is mainly used when you need to change the behaviour or style of the LLM. It can also be useful when working with smaller models. RAG is mainly useful when working with dynamic data. It allows you to add your own data to the context when working with LLMs. It also increases the credibility of the LLM and reduces hallucinations. These two techniques can also be used together when necessary. More info can be found [here](https://www.rungalileo.io/blog/optimizing-llm-performance-rag-vs-finetune-vs-both) and [here](https://www.tidepool.so/2023/08/17/.why-you-probably-dont-need-to-fine-tune-an-llm/)

## Prompt Engineering
To improve the quality of the output you can:
* Put the instructions in the beginning istead of the end (Does not matter with GPT-4)
* Tell the model to answer with a set response in certain situations (System message)
* Give prompt-completion examples in the prompt (Few-shot learning)
* Put a few words at the end of the prompt to get output in desired format (Priming)
* Use clear syntax
* Break down the task into smaller steps
* Provide grounding data

More information can be found [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/advanced-prompt-engineering?pivots=programming-language-chat-completions).