import json
from flask import request, render_template

def autocomplete_view(items_getter, item_template, **kwargs):
    query = request.values['query']
    items = items_getter(query, **kwargs)
    data = [{'id': item['id'],
             'title': item['title'],
             'data': item['data'],
             'html': render_template(item_template, **item)
            } for item in items]
    return json.dumps(data)