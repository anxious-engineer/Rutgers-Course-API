from rutgers.soc import *

# Undergraduate Levels
LEVELS = ['U', 'G']
# New Brunswick Campus
CAMPUS = 'NB'
# Fall Semester for now.
SEMESTERS = ['92016', '12017', '72017', '92017']

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

        for sem in SEMESTERS:
            for lev in LEVELS:
                # Pulls JSON from soc
                subjectJSON = soc.getJSON(lev, CAMPUS, sem, subject)

                # Only add JSON's with courses
                if len(subjectJSON) > 0:
                    print (num)
                    wl = open('whitelist', 'a')
                    wl.write(subject + '\n')
                    wl.close()



updateWhitelist()
