import redis
import os
# import json


def lambda_handler(event, context):
    top_items = None
    params = event['queryParams']
    CACHE_HOST = os.environ.get('CACHE_HOST')
    CACHE_PORT = os.environ.get('CACHE_PORT')
    r = redis.Redis(host=CACHE_HOST, port=CACHE_PORT, db=0)
    business = params.get('business')
    date_filter = params.get('filter')
    if business and date_filter:
        top_items = r.get(business + '-' + date_filter + '-top_items')

    return {
        "res": top_items
    }
