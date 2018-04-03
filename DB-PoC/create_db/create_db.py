#!/usr/bin/python3
import sys, os
sys.path.append(os.path.abspath('../'))
from rusoc import api as soc
import pymongo
import argparse
import urllib.request, json
import course_parsing
import db_connect

def get_args():
    # parse all the arguments to the client
    parser = argparse.ArgumentParser(description='Create a PoC Database in the RCAPI')
    parser.add_argument('-n','--name', help='Database Name Name', required=True)

    # parse the input
    args = vars(parser.parse_args())
    return args

def main():
    # Get CLI Args passed to script
    cli_args = get_args()
    # Get DB Name of potentially new collection
    db_name = str(cli_args['name'])

    # Connect to Mongo Cluster
    client = db_connect.get_client()

    # PoC Database Object
    DB = client[db_name]

    # Create a DB object
    # Create parser object with DB object
    # Parse all courses into it

    parser = course_parsing.Parser(DB) # Parser(DB)
    all_urls = soc.get_all_current_course_urls()
    for url in all_urls:
        data = soc.get_clean_JSON(url)
        parser.parse_course_data(data)

    # Close Mongo Connection
    close_response = client.close()
    print(close_response if close_response else "Goodbye!")

if __name__ == '__main__':
    main()
