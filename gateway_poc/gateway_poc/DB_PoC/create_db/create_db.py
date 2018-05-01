#!/usr/bin/python3
import sys, os
sys.path.append(os.path.abspath('../'))
from rusoc import api as soc
import pymongo
import argparse
import urllib.request, json
import course_parsing
import db_connect
import threading
from threading import Thread

def get_args():
    # parse all the arguments to the client
    parser = argparse.ArgumentParser(description='Create a PoC Database in the RCAPI')
    parser.add_argument('-n','--name', help='Database Name Name', required=True)
    parser.add_argument('-t', '--threaded', help='Run Script Using Multiple Threads', action='store_true')

    # parse the input
    args = vars(parser.parse_args())
    return args

def main():
    # Get CLI Args passed to script
    cli_args = get_args()
    # Get DB Name of potentially new collection
    db_name = str(cli_args['name'])
    run_threaded = cli_args['threaded']

    # Connect to Mongo Cluster
    client = db_connect.get_client()

    # PoC Database Object
    DB = client[db_name]

    # Create a DB object
    # Create parser object with DB object
    # Parse all courses into it

    parser = course_parsing.Parser(DB) # Parser(DB)
    all_urls = soc.get_all_current_course_urls()
    if run_threaded:
        collector = JSON_Collector(all_urls)
        while collector.isIncomplete():
            # Collect Data from collector
            data = collector.dequeue()
            # If there is no data, check again
            if not data:
                continue
            parser.spawn_parse_thread(data)

        parser.join()
    else:
        for url in all_urls:
            data = soc.get_clean_JSON(url)
            parser.parse_course_data(data)

    # Close Mongo Connection
    close_response = client.close()
    print(close_response if close_response else "Goodbye!")

class JSON_Collector(object):
    def __init__(self, urls):
        self.urls = urls
        self.complete_urls = 0
        self.parsed = 0
        self.available_data = []
        self.lock = threading.Lock()
        self.collector_thread = Thread(target = self.collect_data)
        self.collector_thread.start()

    def collect_data(self):
        for url in self.urls:
            new_data = soc.get_clean_JSON(url)
            # Acquire Lock
            self.lock.acquire()
            self.available_data.append(new_data)
            self.complete_urls += 1
            # Release Lock
            self.lock.release()

    def isIncomplete(self):
        # Acquire Lock
        self.lock.acquire()
        if self.complete_urls != 0 and self.available_data != 0:
            # print('---%s - %s---' % (self.complete_urls, len(self.available_data)))
            pass
        output = not(self.complete_urls == len(self.urls) and len(self.available_data) == 0)
        # Release Lock
        self.lock.release()
        return output

    def dequeue(self):
        # Acquire Lock
        self.lock.acquire()
        output = None
        if len(self.available_data) > 0:
            output = self.available_data.pop(0)
            self.parsed += 1
            print(str(self.parsed) + ' of ' + str(len(self.urls)))
        # Release Lock
        self.lock.release()
        return output

if __name__ == '__main__':
    main()
