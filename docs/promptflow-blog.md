CI/CD Pipeline for Azure ML Prompt Flow App
Jan 2024

Azure Machine Learning prompt flow is a development tool designed to streamline 
the entire development cycle of AI applications powered by Large Language Models (LLMs).     

With Azure Machine Learning prompt flow, you'll be able to:
* Create executable flows that link LLMs, prompts, and Python tools through a visualized graph.
* Create prompt variants and evaluate their performance through large-scale testing.
* Deploy a real-time endpoint that unlocks the full power of LLMs for your application.

In this document, we created a CI/CD Pipeline for Azure Prompt Flow with GitHub Actions. 
There are 3 Jobs in the Pipeline:      
* Evaluation
* Deployment
        
Steps which are done during "Evalustion" Job are:
* Initial Setup (Installing Requirements and Azure Login)
* Create Compute Instance
* Create Test Environment
* Model Testing
* Test Evaluation
* Remove Test Resources
* Endpoint Creation
* Model Deployment to the Endpoint

Steps which are done during "Deployment" Job are:
* Register Prompt Flow Model
* Setup Endpoint
* Check the Status of Endpoint
* Update PRT_CONFIG 
* Setup Deployment and Check Deployment Status
           
We will explain all these steps one by one in this blog.   
Firstly starting with "Evaluation" Phase of the Pipeline.          

0. **Requirements**       
Before start pipeline, there are severals resources which need to be ready.        
These are:
- GitHub Repository (You can fork sample repository "https://github.com/deepnetworkgmbh/generative-ai.git")
- Please enable GitHub actions for your GitHub Repository (Go to 'settings/actions/general' and enable 'Allow all actions and reusable workflows')
- Create Azure ML Workspace ("https://learn.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources?view=azureml-api-2")
        
1. **Initial Setup**                      
There are several steps need to be done before the 'Test' and 'Deployment'.                
These are:       
* Install az ml extension (Required for 'ml' CLI commands)       
* Azure login with Created Service Principal ("0. Requirements")      
* Set up Python (Python 3.11.4 is used)      
* Install promptflow (Requirements in 'flow/promptflow/web-classification/requirements.txt' are used)       
         
2. **Create Compute Instance**               
To run Prompt Flow Test we need to create compute instance (Virtual Machine) in Azure ML.                     
At the end of the pipeline, created source is deleted.                
* Set Compute and Runtime Names (For further usage)       
* Create Managed Identity (To give required permissions to Compute Instance)       
* Assign "AzureML Data Scientist" role to MSI    
* Create Azure ML Compute Instance (Used VM type is "Standard_DS1_v2", there are several options you can use)     
      
3. **Create Test Environment**              
After creating Compute Resource, we need to create 'Create Test Runtime' which will run Prompt Flow Tests.
          
* We are creating Test Runtime via "POST" request to the Azure ML Workspace (Firstly create access token, and send POST request via it):         
```access_token=$(az account get-access-token | jq -r ".accessToken")```
                
```runtime_url_post=$(echo "https://ml.azure.com/api/${{env.LOCATION}}/flow/api/subscriptions/${{env.SUBSCRIPTION}}/resourceGroups/${{env.GROUP}}/providers/Microsoft.MachineLearningServices/workspaces/${{env.WORKSPACE}}/FlowRuntimes/${{env.RUNTIME_NAME}}?asyncCall=true")```
          
```         
curl --request POST \
--url "$runtime_url_post" \
--header "Authorization: Bearer $access_token" \
--header 'Content-Type: application/json' \
--data "{
\"runtimeType\": \"ComputeInstance\",
\"computeInstanceName\": \"${{env.COMPUTE_NAME}}\",
}"
```
        
* Runtime creation takes some time (About 5 minutes), so we are using ping mechanism to be sure runtime is ready ("GET" request is sent in each 100s):         
```         
http_response="Unavailable"
while : ; do
  echo "Waiting runtime... 1"
  if [ "$http_response" = "null" ]; then
      echo "Exiting from the while loop..."
      break
  fi
  runtime_url_get=$(echo "https://ml.azure.com/api/${{env.LOCATION}}/flow/api/subscriptions/${{env.SUBSCRIPTION}}/resourceGroups/${{env.GROUP}}/providers/Microsoft.MachineLearningServices/workspaces/${{env.WORKSPACE}}/FlowRuntimes/${{env.RUNTIME_NAME}}")
  http_response=$(curl --request GET \
    --url "$runtime_url_get" \
    --header "Authorization: Bearer $access_token" \
    | jq -r '.status')
  echo "Waiting runtime... 2"
  echo $http_response
  sleep 100
done
```          
               
4. **Model Testing**
We have 2 tests in the project:        
* "flow/promptflow/web-classification/run.yml": Running just Prompt Flow to determine possible errors in the Flow.
* "flow/promptflow/web-classification/run_evaluation.yml": Evaluating Model with ground truths.
Example output of the test is below:      
![Prompt Flow Test Results](images/PromptFlowEvaluationResult.png)       
       
You can also add more test data to the "flow/promptflow/web-classification/data.jsonl" file.    

5. **Test Evaluation**
After running tests on the Prompt Flow Model, we are evaluating results. 
To do that, we created Evaluation Script ("flow/promptflow/llmops-helper/assert.py").     
It takes the output of previous step ("4. Model Testing"), and calculate accuracy.     
* If accuracy is higher than 60%, then set 'evaluation' job's result variable ('eval_result') True
* Otherwise: set it False          
      
6. **Remove Test Resources**      
Finally, we remove all the resources which are created during Test Phase.            
These resources are:               
* Compute Resource (Virtual Machine)      
        
Let's move on with "Deployment" Phase.     
Here, we are creating model (Which passed evaluation tests) and deploy it to the Endpoint.   
As Jobs are working on different Virtual Machines in GitHub Actions environment, we need to do all prerequisites first.
That step is same as Evaluation Phase's "0. Requirements" step.               
Afterwards, steps are:           
1. **Register Prompt Flow Model**        
After Testing, model should be stored in Azure ML Studio.      
To do that, model file 'flow/promptflow/deployment/model.yaml' is used.
```
az ml model create --file flow/promptflow/deployment/model.yaml  -g *** -w ***
```
        
2. **Setup Endpoint**
We create endpoint to deploy saved model and answer user requests coming to app.     
Again, we are using Azure CLI commands and endpoint yaml ("flow/promptflow/deployment/endpoint.yaml")
        
3. **Check the Status of Endpoint**
After creating endpoint, checking its status via `az ml online-endpoint show -n demo-endpoint -g *** -w ***` command.
            
4. **Update PRT_CONFIG**      
If our endpoint is running we are changing 'PRT_CONFIG' variable in the 'deployment.yaml' configuration.      
'PRT_CONFIG' is used to connect OpenAI (Connection and Deployments) and our Prompt Flow App.          
You do not need to add something here, with pipeline it will automatically change 'PRT_CONFIG' with your OpenAI Deployment's description as below:     
```
PRT_CONFIG_OVERRIDE=deployment.subscription_id=${{ env.SUBSCRIPTION }},deployment.resource_group=${{ env.GROUP }},deployment.workspace_name=${{ env.WORKSPACE }},deployment.endpoint_name=${{ env.ENDPOINT_NAME }},deployment.deployment_name=${{ env.DEPLOYMENT_NAME }}
```          

5. **Setup Deployment and Check Deployment Status**
Finally, its ready to deploy model which is created in "1. Register Prompt Flow Model" to the endpoint.   
'flow/promptflow/deployment/deployment.yam' is used for deployment in `az ml online-deployment create` command.    

