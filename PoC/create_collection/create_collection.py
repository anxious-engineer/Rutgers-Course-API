import pymongo
import argparse, sys

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

    # Add Data
    for i in range(100):
        new_coll.insert({"msg" : i})

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
