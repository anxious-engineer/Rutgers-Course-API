#!/usr/bin/python3
import db_connect
import json

client = db_connect.get_client()
test_db_name = "test"
db = client[test_db_name]

def expand_test_professors():
    profs = db['professor'].find()
    for prof in profs:
        print(json.dumps(expand(prof), indent=4))
        input()

def expand_test_courses():
    courses = db['course'].find()
    for course in courses:
        print(json.dumps(expand(course), indent=4))
        input()


def expand(doc):
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

def main():
    print(client)
    expand_test_courses()
    expand_test_professors()

if __name__ == '__main__':
    main()
