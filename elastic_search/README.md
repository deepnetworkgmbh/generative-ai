
## Environment Setup

Set the `OPENAI_API_KEY` environment variable to access the OpenAI models.

To connect to your Elasticsearch instance, use the following environment variables:

```bash
export ELASTIC_CLOUD_ID = <ClOUD_ID>
export ELASTIC_USERNAME = <ClOUD_USERNAME>
export ELASTIC_PASSWORD = <ClOUD_PASSWORD>
```
For local development with Docker, use:

```bash
export ES_URL="http://localhost:9200"
```

And run an Elasticsearch instance in Docker with
```bash
docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.9.0
```

## Usage

For loading the fictional workplace documents, run the following command from the root of this repository:

```bash
python ingest.py
```

However, you can choose from a large number of document loaders [here](https://python.langchain.com/docs/integrations/document_loaders).  

1. docker network create elastic

2. docker pull docker.elastic.co/elasticsearch/elasticsearch:8.11.3

3. docker run --name es01 --net elastic -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.11.3

4. docker pull docker.elastic.co/kibana/kibana:8.11.3

5. docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.11.3

## Chain
