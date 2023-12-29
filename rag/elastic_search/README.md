# RAG Using Elasticsearch
![RAG flow with Elasticsearch](elastic_search/images/Elasticsearch%20RAG%20flow.drawio.png)
## Environment Setup

Set the following environment variables to access the Azure OpenAI models:
```bash
export AZURE_OPENAI_ENDPOINT=<AZURE_OPENAI_ENDPOINT>
export AZURE_OPENAI_API_KEY=<AZURE_OPENAI_API_KEY>
```

For connecting to your Elasticsearch instance, use the following environment variables:
```bash
export ELASTIC_CLOUD_ID=<ClOUD_ID>
export ELASTIC_USERNAME=<ClOUD_USERNAME>
export ELASTIC_PASSWORD=<ClOUD_PASSWORD>
```

For local development with Docker, follow these steps instead:
1. Create Docker network
```bash
docker network create elastic 
```
2. Run Elasticsearh container
```bash
docker run -d --name es01 --net elastic -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.11.3
```
Note: If you decide to use a different port for the Elasticsearch container, you should set:
```bash
export ES_URL=http://localhost:<your-port>
```

3. Run Kibana container. If you do not want to install Kibana, you can skip the rest of these steps.
```bash
docker run -d --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.11.3
```
4. Open a browser and go to http://localhost:5601
5. Click **Configure manually** and paste `http://es01:9200`. Then click **Check Adress** and **Configure Elastic**.
6. To find the verification code you can either look to the logs of the Kibana container or run **bin\kibana-verification-code.bat**.
7. Enter the verification code.

## Usage

To load the pdf documents, run **ingest.py** from the root of this repository.

For different types of documents, you can choose from a large number of document loaders [here](https://python.langchain.com/docs/integrations/document_loaders).

After loading the files you can run **main.py** to start the app.