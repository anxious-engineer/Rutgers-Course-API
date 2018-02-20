#!/usr/bin/python3
import pymongo
import argparse, sys
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

# Gets a clean JSON or nothing
def get_clean_JSON(requestURL):
    response = urllib.request.urlopen(requestURL).read()
    data = json.loads(response)
    return data

# Gets JSON represeting Course data for given params from SOC API
def get_subject_course_data(SEMSTER, CAMPUS, LEVEL, SUBJECT):
    # Populate with
    url = "http://sis.rutgers.edu/oldsoc/courses.json?subject=" + SUBJECT + "&semester=" + SEMSTER + "&campus=" + CAMPUS + "&level=" +  LEVEL
    data = get_clean_JSON(url)
    return data

# Gets JSON of subjects from SOC API
def get_subject_dict(SEMSTER, CAMPUS, LEVEL):
    # sub_code : sub_desc
    subjects = {}
    # Populate with
    url = "http://sis.rutgers.edu/oldsoc/subjects.json?semester=" + SEMSTER + "&campus=" + CAMPUS + "&level=" +  LEVEL
    data = get_clean_JSON(url)

    # Build Subject Dict from Data
    for sub_dict in data:
        sub_code = sub_dict.get("code")
        sub_desc = sub_dict.get("description")
        subjects[sub_code] = sub_desc

    return subjects

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


    # Get and Push Data for each subject, campus, level
    # NOTE : THIS WILL TAKE A WHILE, COULD BE MULTI-THREADED
    # THOUGH NOT SURE HOW THE CONNECTIONS WOULD WORK WITH MULTIPLE THREADS

    for campus in PoC_CAMPUSES:
        for level in PoC_LEVELS:
            print("CAMPUS: %s | LEVEL: %s" % (campus, level))
            # Get Subjects
            subject_dict = get_subject_dict(PoC_SEMESTER, campus, level)
            subject_list = subject_dict.keys()
            for subject in subject_list:
                # GET DATA
                print("\tGetting data for %s - %s" % (subject, subject_dict.get(subject, "Unknown")))
                data = get_subject_course_data(PoC_SEMESTER, campus, level, subject)

                courses = parse_course(data)
                db['course'].insert(courses)
                print("\tPushed %d courses, from %s - %s" % (len(courses), subject, subject_dict.get(subject, "Unknown")))

                professors = parse_professor(data)
                db['professor'].insert(professors)
                print("\tPushed %d professors, from %s - %s" % (len(professors), subject, subject_dict.get(subject, "Unknown")))

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
