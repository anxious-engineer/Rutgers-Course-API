# soc.py

# TODO: ADD ENUMS or constants for levels, campuses, and/or semesters.
import urllib, json


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