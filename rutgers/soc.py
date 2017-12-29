# soc.py

# TODO: ADD ENUMS or constants for levels, campuses, and/or semesters.
import urllib, json
import datetime


def getJSON(level, campus, semester, subject):

    # TODO: Create validate JSONparam method
    # Syntax Checks

    # Check Level
    if not(level == 'U' or level == 'G'):
        # level is not Undergraduate or Graduate
        print("SOC SYNTAX ERROR: level must be 'U' or 'G'.")

    # Check campus
    if not(campus == 'NB' or campus == 'NK' or campus == 'CM'):
        # campus is not New Brunswick, Newark, or Camden
        print("SOC SYNTAX ERROR: campus must be 'NB', 'NK', or 'CM'.")

    # TODO: Check Semester

    # TODO: Check Subject

    # End Syntax Checks

    # Create URL

    requestURL = 'http://sis.rutgers.edu/soc/courses.json?subject=' + subject +'&semester=' + semester + '&campus=' + campus + '&level=' + level

    response = urllib.urlopen(requestURL).read()
    data = json.loads(response)

    return data

def generateTime(time, mCode):

    if time == None:
        return datetime.time(0, 0, 0)

    tStr = str(time)

    minute = int(tStr[2:])

    hour = int(tStr[:2])

    if hour == 12:
        hour = 0

    if mCode == 'P':
        hour += 12

    # print datetime.time(hour, minute, 0)
    return datetime.time(hour, minute, 0)

# Representation of SOC Subject
class Subject(object):

    # Constructs new Subject
    def __init__(self, number, JSON):

        # TODO : Determine if the parameter is needed, can be pulled from json
        # Sets course number (ex: "198" - CS, "640" - Math)
        self.number = number
        # Stores json array of courses
        self.json = JSON

        # List of the subject's course objects
        self.courses = []

        # Adds all courses in json to course list
        for c in self.json:
            self.courses.append(Course(c))

    def __str__(self):
        output = str(self.number)

        for c in self.courses:
            output += '\n' + str(c)

        return output

    # Returns number of courses offered by subject
    def numCourses(self):
        return len(self.courses)


# TODO : Add all JSON fields
# Representation of SOC Course
class Course(object):

    # Constructs new Course
    def __init__(self, JSON):

        # Stores course number
        self.number = JSON['subject']

        # Stores course title
        self.title = JSON['title']

        # Stores course title
        self.campusCode = JSON['campusCode']

        # List of course's section objects
        self.sections = []

        # Adds all sections in json to section list
        for s in JSON['sections']:
            self.sections.append(Section(s))

        # Stores json object containing Course properties
        self.json = JSON

    def __str__(self):
        output = str(self.number) + " - " + str(self.title) + " - " + str(self.campusCode)

        for s in self.sections:
            output += '\n\t' + str(s)

        return output


# TODO : Add all JSON fields
# Representation of SOC Section
class Section(object):

    # Constructs new Section
    def __init__(self, JSON):

        # Stores section index
        self.index = JSON['index']

        # List of section's meetings times
        self.meetings = []

        # Adds all meeting times to section list
        for m in JSON['meetingTimes']:
            self.meetings.append(Meeting(m))

    def __str__(self):
        output = str(self.index)

        for m in self.meetings:
            output += '\n\t\t' + str(m)

        return output

# TODO : Implement generateTime()
# TODO : Add all JSON fields
# Representation of SOC Meeting Time
class Meeting(object):
    # Constructs new Meeting
    def __init__(self, JSON):
        # Stores meeting campus
        self.campus = JSON['campusName']

        # Stores meeting building
        self.building = JSON['buildingCode']

        # Stores meeting room
        self.room = JSON['roomNumber']

        # Stores day of week
        self.day = JSON['meetingDay']

        self.startTime = generateTime(JSON['startTime'], JSON['pmCode'])
        self.endTime = generateTime(JSON['endTime'], JSON['pmCode'])

    def __str__(self):
        return str(self.campus) + ' - ' + str(self.building) + ' - ' + str(self.room) + ' - ' + str(self.startTime) + ' - ' + str(self.endTime)
