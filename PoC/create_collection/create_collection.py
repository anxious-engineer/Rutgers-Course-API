import pymongo
import argparse, sys
import urllib.request, json

# CONSTANTS FOR PoC
PoC_SEMESTER = "12018"
PoC_CAMPUSES = ['NB', 'NK', 'CM', 'WM', 'AC', 'MC', 'J', 'RV', 'CC', 'CU']
PoC_LEVELS = ["UG", "G"]

# TODO : HIDE & MODULARIZE
PASSWORD = "makingausableapi"
uri = "mongodb+srv://rcapi-admin:" + PASSWORD + "@rcapi-f8yp4.mongodb.net/test"
DB = "PoC"

def get_args():
    # parse all the arguments to the client
    parser = argparse.ArgumentParser(description='Create a PoC Collection in the RCAPI-PoC DB')
    parser.add_argument('-n','--name', help='Collection Name', required=True)

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

# POPULATES a collection with the JSON Data
def populate_collection(client, collection):
    # Gather Data
    # Push to Collection One Subject at a time


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
                # PUSH DATA
                document = {
                    "DATA" : data,
                    "SEMESTER" : PoC_SEMESTER,
                    "CAMPUS" : campus,
                    "LEVEL" : level,
                    "SUBJECT" : subject,
                }
                print("\tPushed %d courses, for %s - %s" % (len(data), subject, subject_dict.get(subject, "Unknown")))
                collection.insert(document)

def attempt_creation(client, coll_name):
    # Create PoC DB if neccesary
    if DB in client.database_names():
        print("%s DB exists!" % (DB))
    else:
        print("Creating %s DB!" % (DB))

    # print(client.database_names())

    # PoC Database Object
    PoC_DB = client[DB]

    # Detemine if collection exists
    if coll_name in PoC_DB.collection_names():
        print("%s already exists in %s DB!" % (coll_name, DB))
        return
    else:
        print("Creating %s in %s DB!" % (coll_name, DB))

    new_coll = PoC_DB.create_collection(coll_name)

    print(new_coll)

    populate_collection(client, new_coll)

    print(new_coll.count())

def main():
    # Get CLI Args passed to script
    cli_args = get_args()
    # Get Column Name of potentially new collection
    coll_name = str(cli_args['name'])

    # Connect to Mongo Cluster
    client = pymongo.MongoClient(uri)

    attempt_creation(client, coll_name)

    # Close Mongo Connection
    close_response = client.close()
    print(close_response if close_response else "Goodbye!")

if __name__ == '__main__':
    main()
