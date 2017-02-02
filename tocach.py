# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from reports.views import sales, customers
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import floatformat, pluralize
from efactura.models import Cuenta
from django.template import defaultfilters
from dateutil.parser import parse
from django.views.decorators.http import require_http_methods

import json
import requests

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

@require_http_methods['GET']
def query_data_temp(request):
    from_date = request.GET.get('from', monthdelta(datetime.now(), -1))
    to_date = request.GET.get('to', datetime.now() - timedelta(days=1))
    if isinstance(from_date, unicode):
        from_date = parse(from_date)
    if isinstance(to_date, unicode):
        to_date = parse(to_date)


    business_id = request.GET.get('id_business')
    branches = []
    branches.append(request.GET.get('branch', 'all'))
    return from_date, to_date, business_id, branches

@require_http_methods['GET']
def total_sales_temp(request):
    from_date, to_date, business_id, branches = query_data_temp(request)

    result = sales.sales_total(business_id, branches, from_date, to_date)
    total_returns = sales.total_in_returns(business_id, branches, from_date,
                                           to_date)
    resp = {}
    total_sales = result.get('total', 0)
    tax_returns = (total_returns.get('iva') or 0) + \
                  (total_returns.get('ice') or 0)
    tax_total = result.get('iva', 0) + result.get('ice', 0) - tax_returns
    subtotal = result.get('total', 0) - (total_returns.get('total') or 0)
    transaction_count = result.get('total_transacciones', 0)

    resp["total_sales"]         = total_sales
    resp["tax_total"]           = tax_total
    resp["subtotal"]            = subtotal
    resp["transaction_count"]   = transaction_count

    return JsonResponse(resp)

@require_http_methods['GET']
def top_items_temp(request):
    from_date, to_date, business_id, branches = query_data_temp(request)
    result = sales.sold_items(business_id, branches, from_date, to_date)[:5]
    products = []
    for i, p in enumerate(result):
        products.append({
            'position': i + 1,
            'name': p.get('producto_nombre'),
            'count': float(p.get('total_unidades')),
            'total': format_currency(p.get('total_vendido', 0))
        })
    return JsonResponse(products)

@require_http_methods['GET']
def ticket_average_temp(request):
    from_date, to_date, business_id, branches = query_data_temp(request)
    result = sales.ticket_average(business_id, branches, from_date, to_date)

    # TODO: cache the number of clients too

    return JsonResponse(result)



def format_currency(val, decimal_places=2):
    return '$' + intcomma(floatformat(val, decimal_places))

def fact_card(title,
              name,
              amount,
              description,
              footer,
              empty_msg,
              empty,
              size=1,
              raw={}):
    return {
        'type': 'fact',
        'name': name,
        'title': title,
        'amount': amount,
        'caption': description,
        'footer': footer,
        'raw': raw,
        'empty': empty,
        'empty_msg': empty_msg,
        'size': size
    }

def list_card(title, name, items, cols, cols_format, empty_msg, empty, size=1):
    return {
        'type': 'list',
        'name': name,
        'title': title,
        'items': items,
        'cols': cols,
        'cols_format': cols_format,
        'empty': empty,
        'empty_msg': empty_msg,
        'size': size
    }

def date_range_to_str(from_date, to_date):
    f = datetime.today() - timedelta(days=30),
    t = datetime.today()
    days = (to_date - from_date).days
    if to_date.date() == date.today() and to_date.date() == from_date.date():
        return 'Hoy'
    elif t.date() == to_date.date() and days <= 30:
        return u'Últimos {} días'.format(days)
    elif to_date.date() == from_date.date():
        return defaultfilters.date(from_date, 'F j')
    else:
        return defaultfilters.date(from_date, 'F j') + " - " + \
             defaultfilters.date(to_date, 'F j')
