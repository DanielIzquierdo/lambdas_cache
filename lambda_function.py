import redis
# import json


def lambda_handler(event, context):
    month_sales_until_yesterday = None
    params = event['queryParams']
    r = redis.Redis(
        host='dashboardcache-001.ggh8va.0001.usw2.cache.amazonaws.com',
        port=6379,
        db=0)
    # total_d = {'total': 148.64,
    #            'taxes_total': 15.93,
    #            'subtotal': 132.71,
    #            'transaction_count': 3.0}
    # r.set('0991234567001-month', json.dumps(total_d))
    business = params.get('business')
    date_filter = params.get('filter')
    if business and date_filter:
        month_sales_until_yesterday = r.get(business + '-' + date_filter)

    return {
        "res": month_sales_until_yesterday
        if month_sales_until_yesterday else None
    }
