import urllib.request, json
from datetime import datetime
import time

# Campus Abbreviations used in API calls.
# TODO : Add Validation for Other Campuses
campuses = [
    'NB',
    'NK',
    'CM',
    # 'WM',
    # 'AC',
    # 'MC',
    # 'J',
    # 'RV',
    # 'CC',
    # 'CU',
    # 'ONLINE'
]

# Abbreviations for course levels used in API calls.
levels = [
    'UG',
    'G'
]

# Maps a String 'Digit' represeting a month to the String 'digit'
# that represents the semester each month is in according to the SOC api.
month_to_semester_map = {
    '1' : '1',
     1 : '1',
     '2' : '1',
     2 : '1',
     '3' : '1',
     3 : '1',
     '4' : '1',
     4 : '1',
     '5' : '1',
     5 : '1',
     '6' : '1',
     6 : '1',
     '7' : '7',
     7 : '7',
     '8' : '7',
     8 : '7',
     '9' : '9',
     9 : '9',
     '10' : '9',
     10 : '9',
     '11' : '9',
     11 : '9',
     '12' : '9',
     12 : '9',
}

# Format String for Subject List endpoint url - JSON format
subject_url = 'http://sis.rutgers.edu/soc/subjects.json?semester=%s&campus=%s&level=%s'

# Format String for Course List for a given subject endpoint url - JSON format
course_url = 'http://sis.rutgers.edu/soc/courses.json?subject=%s&semester=%s&campus=%s&level=%s'

# TODO : Add support for summer
# winter: 0, spring: 1, summer: 7, fall: 9
# Returns the SOC String represetation of the current semester (i.e. Today's Semester)
def get_current_semester_string():
    year = datetime.now().year
    month = month_to_semester_map.get(datetime.now().month)
    return "%s%s" % (month, year)

# Returns url for the Subject URL formatted with the given params
def get_subject_url(semester, campus, level):
    return subject_url % (semester, campus, level)

# Returns url for the Course URL formatted with the given params
def get_course_url(subject, semester, campus, level):
    return course_url % (subject, semester, campus, level)

# Returns a list of all Subject URLS for the current semester
def get_all_current_subject_urls():
    urls = []
    current_semester = get_current_semester_string()
    for campus in campuses:
        for level in levels:
            urls.append(get_subject_url(current_semester, campus, level))
    return list(set(urls))

# Returns a list of all Course URLS for the current semester
def get_all_current_course_urls():
    urls = []
    current_semester = get_current_semester_string()
    for campus in campuses:
        for level in levels:
            subject_url = get_subject_url(current_semester, campus, level)
            subjects = get_subject_list_from_url(subject_url)
            for subject in subjects:
                urls.append(get_course_url(subject, current_semester, campus, level))
    return list(set(urls))

# Gets a clean JSON or nothing
def get_clean_JSON(requestURL):
    ATTEMPTS = 10
    data = []
    while ATTEMPTS > 0:
        response = urllib.request.urlopen(requestURL).read()
        data = json.loads(response)
        if len(data) > 0:
            return data
        time.sleep(1)
        ATTEMPTS -= 1
    return data

# Get list of Subjects from Subject URL
def get_subject_list_from_url(requestURL):
    # Gets a clean JSON or nothing
    data = get_clean_JSON(requestURL)
    subjects = []

    # Build Subject Dict from Data
    for sub_dict in data:
        subjects.append(sub_dict.get("code"))

    return list(set(subjects))
