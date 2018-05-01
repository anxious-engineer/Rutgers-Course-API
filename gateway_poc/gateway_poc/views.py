from django.http import HttpResponse
from .DB_PoC.query_db import query
import json

def handle_method_request(request):
    # Get method name
    method_name = request.path.replace("/", "")
    if not method_name:
        return HttpResponse(json.dumps({'error' : "No Method Name Given"}), content_type="application/json")

    # Get 'GET' (HA! Funny) params
    url_params = request.GET
    # if not url_params:
    #     return HttpResponse(json.dumps({'error' : "No URL Params Given"}), content_type="application/json")

    # Query Collection
    db_res = query.query(method_name, url_params)

    # Expand Results
    expanded_results = []
    for res in db_res:
        expanded_res = query.expand(res)
        expanded_results.append(expanded_res)

    return HttpResponse(json.dumps(expanded_results, indent=4), content_type="application/json")
