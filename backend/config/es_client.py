from elasticsearch import Elasticsearch

es_client = Elasticsearch(
    hosts=["http://elasticsearch:9200"],
    verify_certs=False
)
