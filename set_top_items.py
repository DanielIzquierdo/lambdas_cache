import redis
import os
import json


def lambda_handler(event, context):
    params = event['headers']
    CACHE_HOST = os.environ.get('CACHE_HOST')
    CACHE_PORT = os.environ.get('CACHE_PORT')
    r = redis.Redis(host=CACHE_HOST, port=CACHE_PORT, db=0)
    top_items = event.get('body')
    business = params.get('business')
    date_filter = params.get('filter')
    k = str(business) + '-' + str(date_filter) + '-top_items'
    if business and date_filter and top_items:
        r.set(k, json.dumps(top_items))

    return {
        'sent_to_cache': top_items is not None
    }
