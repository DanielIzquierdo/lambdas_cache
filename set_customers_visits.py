import redis
import os
import json


def lambda_handler(event, context):
    params = event['headers']
    CACHE_HOST = os.environ.get('CACHE_HOST')
    CACHE_PORT = os.environ.get('CACHE_PORT')
    r = redis.Redis(host=CACHE_HOST, port=CACHE_PORT, db=0)
    customer_visits = event.get('body')
    business = params.get('business')
    date_filter = params.get('filter')
    k = str(business) + '-' + str(date_filter) + '-customer_visits'
    if business and date_filter and customer_visits:
        r.set(k, json.dumps(customer_visits))

    return {
        'sent_to_cache': customer_visits is not None
    }
