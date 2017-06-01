from rutgers import soc

# Undergraduate Levels
LEVEL = 'U'
# New Brunswick Campus
CAMPUS = 'NB'
# Fall Semester for now.
SEMESTER = '92017'

# TODO : Add all levels, campuses, and semester values to whitelist
def updateWhitelist():

    open('whitelist', 'w').close()


    for num in range(0, 999):

        # Turns temporary num into soc subject format
        if num < 10:
            subject = '00' + str(num)
        elif num < 100:
            subject = '0' + str(num)
        else:
            subject = str(num)

        # Pulls JSON from soc
        subjectJSON = soc.getJSON(LEVEL, CAMPUS, SEMESTER, subject)

        # Only add JSON's with courses
        if len(subjectJSON) > 0:
            print (num)
            wl = open('whitelist', 'a')
            wl.write(subject + '\n')
            wl.close()



updateWhitelist()