![MLOps Diagram](images/mlops_diagram2.png)
## What is the MLOps ##
Different teams (Data Scientists, ML Engineers etc.).       
MLOps Stages are:    
* Train Data Collection
* Development of ML model
* Evaluation
* Feedback
* If evaluation is successfull, deploy/store model 
* Create endpoint 
* Deploy model to endpoint
       
MLOps is aiming to automate repetitive tasks such as:
* Testing
* Deployments
* Monitoring       
      
## What are the differences between classical pipelines ##
* MLOps includes various teams such as data scientists or ML researchers etc. (Google, https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
* MLOps focuses on model deployment, but classical pipelines focus on software deployment (Model validation, accuracy etc.)
* MLOps includes data quality, classical pipelines are not so much
* MLOps considers dataset evolving (Google, https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

![MLOps Diagram 2 - Google](images/mlops_diagram3.png)
![MLOps Diagram 3 - Google](images/mlops_diagram4.png)

## What is the LLMOps ##
LLMOps is MLOps for LLMs.      
Manage the lifecycle of LLM-powered applications, including development, deployment, and maintenance.    
      
* Instead of training model like in MLOps with huge amount of data, use zero or few-shot learning (High quality selected samples)
* Feature engineering is less important than MLOps because LLM can learn from raw data.
* In MLOps we have evaluation metrics such as accuracy, precision, recall, F1-score etc., but in LLMOps we have ROUGE, BERT, and BLEU score which focus on measuring the similarity of a response to a provided reference answer.

![MLOps - Microsoft](images/llmops_vs_mlops1.png)
![LLMOps - Microsoft](images/llmops_vs_mlops_2.png)

## What is the Azure Speech Service ##
Two types of language detection mechanisms: 
* **At-start LID:** Identifies the language once within the first few seconds of audio. 
Use at-start LID if the language in the audio won't change. 
With at-start LID, a single language is detected and returned in less than 5 seconds.
        
* **Continuous LID:** Can identify multiple languages for the duration of the audio. 
Use continuous LID if the language in the audio could change. 
Continuous LID doesn't support changing languages within the same sentence. 
For example, if you're primarily speaking Spanish and insert some English words, it will not detect the language change per word

## What is the Azure Translater Service ##
