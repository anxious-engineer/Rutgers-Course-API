#!/usr/bin/python3
import sys, os
sys.path.append(os.path.abspath('../'))
from rusoc import api as soc
import pymongo
import argparse
import urllib.request, json

# CONSTANTS FOR PoC
PoC_SEMESTER = "12018"
PoC_CAMPUSES = ['NB', 'NK', 'CM', 'WM', 'AC', 'MC', 'J', 'RV', 'CC', 'CU']
PoC_LEVELS = ["UG", "G"]

# TODO : HIDE & MODULARIZE
PASSWORD = "makingausableapi"
uri = "mongodb+srv://admin:" + PASSWORD + "@poc-5vbvd.mongodb.net/test"

def get_args():
    # parse all the arguments to the client
    parser = argparse.ArgumentParser(description='Create a PoC Database in the RCAPI')
    parser.add_argument('-n','--name', help='Database Name Name', required=True)

    # parse the input
    args = vars(parser.parse_args())
    return args

def extract_course(d):
    keys = [
    "courseNumber",
    "synopsisUrl",
    "title",
    "courseDescription",
    "preReqNotes",
    "credits",
    "courseNotes",
    "expandedTitle"]

    key_map = {
        "courseNumber" : "number",
        "courseDescription" : "description",
        "courseNotes" : "notes",
    }

    new_doc = {}
    for key in keys:
        if d[key]:
            new_key = key_map.get(key) if key_map.get(key) else key
            new_doc[new_key] = d[key]

    return new_doc


def extract_subject(d):
    keys = ["subject"]

    key_map = {
        "subject" : "number",
    }

    new_doc = {}
    for key in keys:
        if d[key]:
            new_key = key_map.get(key) if key_map.get(key) else key
            new_doc[new_key] = d[key]

    return new_doc

def parse_professor(data):
    keys = ["name"]

    new_docs = []

    for d in data:
        if not d['sections']:
            continue
        secs = d['sections']
        for sec in secs:
            if not sec['instructors']:
                continue
            for ins in sec['instructors']:
                new_doc = {}
                for key in keys:
                    if ins[key]:
                        new_doc[key] = ins[key]

                if not new_doc is {}:
                    new_docs.append(new_doc)

    return new_docs

def parse_campus(data):
    keys = ["campusCode"]
    key_map = {
        'campusCode' : 'code'
    }
    code_to_name = {
        'NB' : 'New Brunswick',
        'NK' : 'Newark',
        'CM' : 'Camden',
        'OC' : 'Off Campus',
        'ON' : 'Online'
    }

    new_docs = []

    for d in data:
        new_doc = {}
        for key in keys:
            if d[key]:
                new_key = key_map.get(key) if key_map.get(key) else key
                new_doc[new_key] = d[key]
                if key == 'campusCode':
                    new_key = 'name'
                    if code_to_name.get(d[key]):
                        new_doc[new_key] = code_to_name.get(d[key])

        if not new_doc is {}:
            new_docs.append(new_doc)

    return new_docs

def upsert(collection, doc):
    tar = collection.count(doc)
    if tar == 0:
        collection.insert(doc)
        return
    tar = collection.find(doc)[0]
    return {"_id" : tar["_id"]}

# POPULATES a database with the JSON Data
def populate_database(client, db):
    # Gather Data

    all_urls = soc.get_all_current_course_urls()

    attempts = 1

    fails = open('fails', 'w')

    while attempts > 0:
        print("Attempts Remaing %d" % attempts)
        count = 0
        failed = 0
        total = len(all_urls)
        failures = []
        for url in all_urls:
            print("\r%d of %d Complete | %d Failures | Current -> %s" % (count, total, failed, url), end='')
            # GET DATA
            data = soc.get_clean_JSON(url)

            if len(data) == 0:
                failed += 1
                fails.writelines(url + '\n')
                failures.append(url)
            else:
                # Parse data
                for c in data:
                    references = {
                        "__professor__" : [],
                        "__campus__" : [],
                        "__subject__" : "",
                        "__course__" : []
                    }
                    # Get and insert Subject
                    sub_doc = extract_subject(c)
                    if not sub_doc:
                        continue
                    # Add subject if new
                    sub_doc = upsert(db['subject'], sub_doc)
                    references['__subject__'] = sub_doc
                    # Get and insert course
                    c_doc = extract_course(c)
                    if not c_doc:
                        continue
                    c_doc = upsert(db['course'], c_doc)
                    references['__course__'] = c_doc

                    # Get and insert Professor
                    # Get and insert Campus
                    # Update References
                    update_references(references)
                professors = parse_professor(data)
                if len(professors) > 0:
                    db['professor'].insert(professors)
                # else:
                #     print('\r' + url)

                campuses = parse_campus(data)
                if len(campuses) > 0:
                    db['campus'].insert(campuses)
                # else:
                #     print('\r' + url)
            count+=1
            # print("\tPushed %d professors" % len(professors))
        all_urls = failures
        attempts -= 1

    print(all_urls)
    fails.close()


def attempt_creation(client, db_name):
    # Create PoC DB if neccesary
    if db_name in client.database_names():
        print("%s DB exists!" % (db_name))
        return

    # PoC Database Object
    PoC_DB = client[db_name]

    populate_database(client, PoC_DB)

    print(PoC_DB.collection_names())

def main():
    # Get CLI Args passed to script
    cli_args = get_args()
    # Get DB Name of potentially new collection
    db_name = str(cli_args['name'])

    # Connect to Mongo Cluster
    client = pymongo.MongoClient(uri)

    attempt_creation(client, db_name)

    # Close Mongo Connection
    close_response = client.close()
    print(close_response if close_response else "Goodbye!")

if __name__ == '__main__':
    main()
