import sys
sys.path.append('../rutgers')
from soc import *
sys.path.append('../secrets')
from mongo import *
import pymongo
import time


def addCourses(sub):

    times = []

    for c in sub.courses:
        for s in c.sections:
            for m in s.meetings:
                times.append({
                'subject' : sub.number,
                'course_title' : c.title,
                'campus_name' : m.campus,
                'building_code' : m.building,
                'room_number' : m.room,
                'meeting_day' : m.day,
                'begin_time' : str(m.startTime),
                'end_time' : str(m.endTime)
                })


    # times(subject, course_title, campus_name, building_code, room_number, meeting_day, begin_time, end_time)
    return times


def readWhitelist():
    wlfile = open('../data/whitelist')
    wlist = [line.rstrip('\n') for line in wlfile]
    wlfile.close()
    return wlist

if __name__=='__main__':

    # TODO: Generalize Parameters
    # Undergraduate Levels
    LEVEL = 'U'
    # New Brunswick Campus
    CAMPUS = 'NB'
    # Fall Semester for now.
    SEMESTER = '72017'

    # URI to your mongo client here.
    print(MONGO_URI)
    now = time.strftime("%c")
    print(now)
    client = pymongo.MongoClient(MONGO_URI)
    db = client.rutgers
    coll = db['%s-%s-%s' % (LEVEL, CAMPUS, SEMESTER)]



    # TODO : Remove none subject nums
    # Finds subject from 0 to 999
    whiteList = readWhitelist()
    for subject in whiteList:

        # Pulls JSON from soc
        subjectJSON = getJSON(LEVEL, CAMPUS, SEMESTER, subject)

        # Only add JSON's with courses
        if(len(subjectJSON) < 1):
            print(subject + " should be black listed.")
            continue

        newSub = Subject(subject, subjectJSON)

        coll.insert_many(addCourses(newSub))
        # print(newSub)
