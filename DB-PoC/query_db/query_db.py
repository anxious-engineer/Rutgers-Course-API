#!/usr/bin/python3
import db_connect
import expansion
import json

def main():
    # Connect to Mongo Cluster
    client = db_connect.get_client()
    db_name = 'test'

    db = client[db_name]

    endpoints = db.collection_names()

    for e in endpoints:
        coll = db[e]
        print('%s - %d' % (e, coll.count()))
        # Get Paramater Dictionary
        params = collect_params(coll)
        if params == {}:
            continue

        sanatized_params = sanatize_params(params)

        print("FINAL PARAMS:")
        print(sanatized_params)

        # Query Collection
        db_res = query_collection(coll, sanatized_params)
        # Expand Results
        expanded_results = []
        for res in db_res:
            expanded_res = expansion.expand(res)
            expanded_results.append(expanded_res)

        print(json.dumps(expanded_results, indent=4))

validFields = {
    "campus" : ["code", "name"],
    "subject" : ["number"],
    "professor" : ["name"],
    "course" : ["number", "notes", "description", "synopsisUrl", "title", "preReqNotes", "credits", "expandedTitle"]
}

def query_collection(coll, p):
    res = coll.find(p)
    return res

def collect_params(coll):
    params = {}
    try:
        # Collect
        while True:
            # First Collect a field
            validField = False
            field = None
            while not validField:
                field = input()
                validField = field in validFields[coll.name] and field not in params.keys()
            validValue = False
            value = None
            while not validValue:
                value = input()
                validValue = True
            params[field] = value
            print(params)
    except KeyboardInterrupt:
        print('\r', end = '')
        return params

def sanatize_params(params):
    new_params = {}
    for k in params.keys():
        new_params[k] = {"$regex" : params[k], "$options" : 'i'}

    return new_params

    return new_params
if __name__ == '__main__':
    main()
