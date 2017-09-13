import sqlite3
import sys
sys.path.append('../rutgers')
from soc import *


def addCourses(sub):

    times = []

    for c in sub.courses:
        for s in c.sections:
            for m in s.meetings:
                times.append((str(sub.number), str(c.title), str(m.campus), str(m.building), str(m.room), str(m.day), str(m.startTime), str(m.endTime)))

    # Creates Connection to Database
    connection = sqlite3.connect('times.db')

    if connection is not None:

        # Create Table
        connection.executemany(
            """INSERT INTO times(subject, course_title, campus_name, building_code, room_number, meeting_day, begin_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            times)
        connection.commit()
        connection.close()

    else:
        print("Error Connecting to times Database.")


def readWhitelist():
    wlfile = open('../data/whitelist')
    wlist = [line.rstrip('\n') for line in wlfile]
    wlfile.close()
    return wlist


def main():
    # TODO: Generalize Parameters
    # Undergraduate Levels
    LEVEL = 'U'
    # New Brunswick Campus
    CAMPUS = 'NB'
    # Fall Semester for now.
    SEMESTER = '72017'

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

        addCourses(newSub)
        # print(newSub)


if __name__ == '__main__':
    main()
