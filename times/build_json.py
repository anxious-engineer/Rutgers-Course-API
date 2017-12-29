import sqlite3
import sys
from datetime import datetime, timedelta
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


def getSubjects(term, campus, level):
    requestURL = 'https://rumobile.rutgers.edu/1/indexes/' + term + '_' + campus + '_' + level + '.json'
    response = urllib.urlopen(requestURL).read()
    data = json.loads(response)
    ids = data.get('ids');
    if ids:
        return sorted([(sub.encode('utf-8')) for sub in ids.keys()])
    return []

def parseTime(pm_code, start_time, end_time):
    if (not pm_code) or (not start_time) or (not end_time):
        return None
    start = datetime.datetime.strptime(start_time, '%H%M')
    end = datetime.datetime.strptime(end_time, '%H%M')
    if pm_code == 'P' and start.hour != 12:
        start += timedelta(hours=12)
        end += timedelta(hours=12)

    if start > end:
        end += timedelta(hours=12)


    return {
        'start' : start.strftime('%H:%M'),
        'end' : end.strftime('%H:%M')
    }

def scrapeTimes(subjectJSON):
    times = {}
    for course in subjectJSON:
        course_name = course.get('title')
        # TODO : Expanded Title?
        sections = course.get('sections')
        if (not course_name) or (not sections):
            continue

        for section in sections:
            meetings = section.get('meetingTimes')
            if not meetings:
                continue

            for meeting in meetings:
                room_number = meeting.get('roomNumber')
                building_code = meeting.get('buildingCode')
                time = parseTime(meeting.get('pmCode'), meeting.get('startTime'), meeting.get('endTime'))
                day = meeting.get('meetingDay')
                if (not room_number) or (not time) or (not day) or (not building_code):
                    continue
                new_time = {
                    'course_name' : course_name.encode('utf-8').strip(),
                    'room' : building_code.encode('utf-8') + '-' + room_number.encode('utf-8'),
                }
                new_time.update(time)

                day = day.encode('utf-8')

                if times.get(day):
                    times[day].append(new_time)
                else:
                    times[day] = []
                    times[day].append(new_time)
    return times

def main():
    # TODO: Generalize Parameters
    # Undergraduate Levels
    LEVEL = 'U'
    # New Brunswick Campus
    CAMPUS = 'NB'
    # Fall Semester for now.
    SEMESTER = '12018'



    # TODO : Remove none subject nums
    # Finds subject from 0 to 999
    subjects = getSubjects(SEMESTER, CAMPUS, LEVEL)
    whiteList = []
    allTimes = {}
    for subject in subjects:

        # Pulls JSON from soc
        subjectJSON = getJSON(LEVEL, CAMPUS, SEMESTER, subject)

        # Only add JSON's with courses
        print(subject)
        if(len(subjectJSON) < 1):
            print(subject + " should be black listed.")
            continue

        newTimes = scrapeTimes(subjectJSON)
        # print(newTimes)
        for day in newTimes.keys():
            if allTimes.get(day):
                allTimes[day].extend(newTimes[day])
            else:
                allTimes[day] = []
                allTimes[day].extend(newTimes[day])
        # newSub = Subject(subject, subjectJSON)
        #
        # addCourses(newSub)
        # print(newSub)

    # for day in allTimes.keys():
    #     allTimes[day] = list(set(allTimes.get(day)))

    print(allTimes)
    with open('../data/12018_NB_U.json', 'w') as outfile:
        json.dump({'times':allTimes}, outfile)

if __name__ == '__main__':
    main()
