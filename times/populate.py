from rutgers import soc


def addCourses(sub):
    print(sub)


def readWhitelist():
    wlfile = open('../data/whitelist')
    wlist = [line.rstrip('\n') for line in wlfile]
    wlfile.close()
    return wlist

# TODO: Generalize Parameters
# Undergraduate Levels
LEVEL = 'U'
# New Brunswick Campus
CAMPUS = 'NB'
# Fall Semester for now.
SEMESTER = '92017'

# TODO : Remove none subject nums
# Finds subject from 0 to 999
whiteList = readWhitelist()
for subject in whiteList:

    # Pulls JSON from soc
    subjectJSON = soc.getJSON(LEVEL, CAMPUS, SEMESTER, subject)

    # Only add JSON's with courses
    if(len(subjectJSON) < 1):
        print(subject + " should be black listed.")
        continue

    print(soc.Subject(subject, subjectJSON))