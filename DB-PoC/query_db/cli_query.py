#!/usr/bin/python3
import db_connect
import expansion
import json
import query

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

query_types = json.load(open('query.json'))

config = json.load(open('config.json'))

def build_collections_params(config_json):
    output = {}
    for collection in config_json.keys():
        output[collection] = {}
        coll_config = config_json[collection]
        coll_keys = coll_config['keys']
        for soc_key in coll_keys.keys():
            new_key = soc_key
            # If new name isn't original soc_key name
            if coll_keys[soc_key].get('new_key'):
                new_key = coll_keys.get(soc_key).get('new_key')
            query_type = coll_keys[soc_key].get('query_type')
            output[collection][new_key] = query_type
            if coll_keys[soc_key].get('augmented_keys'):
                augmented_keys = coll_keys[soc_key].get('augmented_keys')
                for k in augmented_keys:
                    output[collection][k] = augmented_keys[k]

    return output

collection_params = build_collections_params(config)
print(json.dumps(collection_params, indent=4))

def main():
    # Connect to Mongo Cluster
    db = db_connect.get_test_db()

    endpoints = db.collection_names()

    for e in endpoints:
        coll = db[e]
        print('%s - %d' % (e, coll.count()))
        # Get Paramater Dictionary
        params = collect_params(coll.name)
        if params == {}:
            continue

        # Query Collection
        db_res = query.query(e, params)
        # Expand Results
        expanded_results = []
        for res in db_res:
            expanded_res = expansion.expand(res)
            expanded_results.append(expanded_res)

        print(json.dumps(expanded_results, indent=4))

def query_collection(coll, p):
    res = coll.find(p)
    return res

def collect_params(coll_name):
    params = {}
    try:
        # Collect
        while True:
            # First Collect a field
            validField = False
            field = None
            while not validField:
                field = input("Enter a Valid Field: ")
                print(CURSOR_UP_ONE + ERASE_LINE, end = '')
                print( collection_params[coll_name].keys() )
                validField = field in collection_params[coll_name].keys()
                validField = validField and field not in params.keys()
            validValue = False
            value = None
            while not validValue:
                value = input("Enter a Valid Value for \'%s\': " % (field))
                print(CURSOR_UP_ONE + ERASE_LINE, end = '')
                validValue = True
            params[field] = value
            print(params)
    except KeyboardInterrupt:
        print('\r' + ERASE_LINE, end = '')
        return params

def sanatize_params(coll_name, params):
    param_types = collection_params[coll_name]
    new_params = {}
    for k in params.keys():
        new_params[k] = {"$regex" : params[k], "$options" : 'i'}

    return new_params

if __name__ == '__main__':
    main()
