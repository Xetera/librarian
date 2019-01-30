from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import kawaii
import os

app = Flask(__name__)

ES_URL = os.environ.get('LIBRARIAN_ES_URL', 'http://localhost:9200')
PRODUCTION = bool(os.environ.get('LIBRARIAN_PRODUCTION', 'False'))
REFRESH_KEY = os.environ.get('LIBRARIAN_KEY', '123')
PORT = int(os.environ.get('LIBRARIAN_PORT', '3030'))
QUERY_LIMIT = int(os.environ.get('LIBRARIAN_QUERY_LIMIT', '25'))

es = Elasticsearch(ES_URL)

def specify_search(query):
  if ':' in query:
    key, value = query.split(':')
    if key == 'title':
      return { 'multi_match': { 'query': value, 'fields': ['title', 'synonyms']  }  }
    return { 'match': { key: value } }
  return { 'query_string': { 'query': query } }

def parse_limit(limit):
  try:
    request = int(limit)
    if request >= QUERY_LIMIT or request <= 0:
      return QUERY_LIMIT
    return request 
  except:
    return QUERY_LIMIT

@app.route('/search/<query>', methods=['get'])
def search(query):
  limit = request.args.get('limit')
  search_query = specify_search(query)

  limited = { 'size': parse_limit(limit) } if limit else {}
  a = es.search(index='animes', body={ 'query': search_query, **limited })

  datas = a['hits']
  datas['count'] = len(datas['hits'])
  return jsonify(datas)

@app.route('/reload', methods=['post'])
def reload():
  if request.headers.get('Authorization') == REFRESH_KEY:
    kawaii.reload_es(es)
    return jsonify({ 'result': 'ok' })
  return jsonify({ 'result': 'unauthorized' })

if __name__=='__main__':
  app.run(host='0.0.0.0', debug=not PRODUCTION, port=PORT)
