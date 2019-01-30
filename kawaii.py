import os
import requests
import json
from elasticsearch import Elasticsearch, helpers

FILE_NAME = 'data.json'
DATA_KEY = 'data'
ES_URL = os.environ.get('LIBRARIAN_ES_URL', 'http://localhost:9200')
TARGET_URL = "https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database.json"

def reload_es(es):
  res = requests.get(TARGET_URL)
  j = res.json()
  data = j.get(DATA_KEY, [])
  docs = [
    { '_type': 'anime', '_index': 'animes', '_id': i,  **rest }
    for i, rest in enumerate(data)
  ]

  es.indices.delete(index='animes', ignore=404)
  es.indices.create(index='animes', ignore=400)
  helpers.bulk(es, docs)

if __name__ == '__main__':
  es = Elasticsearch(ES_URL)
  reload_es(es)