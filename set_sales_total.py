import redis
import os
import json


def lambda_handler(event, context):
    params = event['headers']
    CACHE_HOST = os.environ.get('CACHE_HOST')
    CACHE_PORT = os.environ.get('CACHE_PORT')
    print(CACHE_HOST, CACHE_PORT)
    r = redis.StrictRedis(
        host=CACHE_HOST,
        port=CACHE_PORT,
        db=0)
    total_d = event['body']
    business = params.get('business')
    date_filter = params.get('filter')
    if business and date_filter:
        r.set(business + '-' + date_filter, json.dumps(total_d))
    # if business and date_filter:
    #     month_sales_until_yesterday = r.get(business + '-' + date_filter)

    return {
        'res': "ok",
        'event': event
    }
