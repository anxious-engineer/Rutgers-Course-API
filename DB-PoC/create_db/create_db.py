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

def parse_course(data):
    keys = [
    "courseNumber",
    "synopsisUrl",
    "title",
    "courseDescription",
    "preReqNotes",
    "credits",
    "courseNotes",
    "expandedTitle"]

    new_docs = []

    for d in data:
        new_doc = {}
        for key in keys:
            if d[key]:
                new_doc[key] = d[key]

        if not new_doc is {}:
            new_docs.append(new_doc)

    return new_docs

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
    keys = ["name", "code"]

    new_docs = []

    for d in data:
        new_doc = {}
        for key in keys:
            if d[key]:
                new_doc[key] = d[key]

        if not new_doc is {}:
            new_docs.append(new_doc)

    return new_docs

# POPULATES a database with the JSON Data
def populate_database(client, db):
    # Gather Data

    all_urls = soc.get_all_current_course_urls()

    for url in all_urls:
        # GET DATA
        data = soc.get_clean_JSON(url)

        courses = parse_course(data)
        if len(courses) > 0:
            db['course'].insert(courses)
        else:
            print(url)
        # print("\tPushed %d courses" % len(courses))

        professors = parse_professor(data)
        if len(professors) > 0:
            db['professor'].insert(professors)
        else:
            print(url)
        # print("\tPushed %d professors" % len(professors))

            # campuses = parse_campus(data)
            # db['campus'].insert(campuses)
            # print("\tPushed %d campuses, from %s - %s" % (len(campuses), subject, subject_dict.get(subject, "Unknown")))

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
