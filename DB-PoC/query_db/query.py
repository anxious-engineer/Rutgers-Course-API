import db_connect
import sanatize

def query(coll_name, params):
    clean_params = sanatize.sanatize_params(coll_name, params)
    coll = db_connect.get_test_db()[coll_name]
    print("FINAL PARAMS:")
    print(clean_params)
    res = coll.find(clean_params)
    return res

def expand(doc):
    db = db_connect.get_test_db()
    output_doc = {}
    for key in doc:
        if key == '_id':
            continue
        if isRefKey(key):
            output_doc[key] = []
            for ref_id in doc[key]:
                ref_doc = db[key.strip("_")].find_one({"_id" : ref_id})
                output_doc[key].append(strip_references(ref_doc))
        else :
            output_doc[key] = doc[key]
    for key, val in output_doc.items():
        if isinstance(val, list) and len(val) == 1:
            output_doc[key] = val[0]
    return output_doc

def strip_references(doc):
    output_doc = doc.copy()
    for key in doc:
        if key == '_id' or isRefKey(key):
            output_doc.pop(key, None)
    return output_doc

def isRefKey(key):
    return (key.startswith("__") and key.endswith("__"))
