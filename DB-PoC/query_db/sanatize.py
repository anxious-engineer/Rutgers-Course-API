import json

config = json.load(open('config.json'))
DEFAULT_TYPE = "default"

def sanatize_params(coll_name, params):
    # Santization
    new_params = {}
    for k in params.keys():
        query_type = get_query_type(coll_name, k)
        new_params[k] = get_sanatize_method(query_type)(params[k])
    return new_params

def get_query_type(coll_name, tar_key):
    coll_keys = config.get(coll_name)
    if not coll_keys:
        return DEFAULT_TYPE
    return coll_keys.get("keys", {}).get(tar_key, {}).get("query_type", DEFAULT_TYPE)

# Find sanatize method in the query module
def get_sanatize_method(key):
    name = "sanatize_" + str(key)
    print("Looking for %s" % (name))
    if name in globals().keys():
        return globals()[name]
    else:
        return sanatize_default

# Default sanatization method
def sanatize_default(data):
    return data

def sanatize_number(data):
    pass

def sanatize_string(data):
    if type(data) != str:
        data = str(data)
    return {"$regex" : data, "$options" : 'i'}

def sanatize_paragraph(data):
    if type(data) != str:
        data = str(data)
    return {"$regex" : data, "$options" : 'i'}

def sanatize_numeric(data):
    output = data
    # Handle numeric splice
    if ':' in data:
        output = {}
        lb, ub = data.split(":")
        if lb != '':
            output["$gte"] = int(lb)
        if ub != '':
            output["$lte"] = int(ub)
    return output
