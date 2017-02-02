import redis
import os
import json


def lambda_handler(event, context):
    params = event['headers']
    CACHE_HOST = os.environ.get('CACHE_HOST')
    CACHE_PORT = os.environ.get('CACHE_PORT')
    r = redis.Redis(host=CACHE_HOST, port=CACHE_PORT, db=0)
    total_d = event.get('body')
    business = params.get('business')
    date_filter = params.get('filter')
    k = str(business) + '-' + str(date_filter) +'-clients'
    if business and date_filter and total_d:
        r.set(k, json.dumps(total_d))

    return {
        'sent_to_cache': total_d is not None
    }