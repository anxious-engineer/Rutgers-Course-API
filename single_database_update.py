from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Courses, Sections, MeetingTimes
from urllib2 import urlopen
import contextlib, json, urllib

# Creates sqlalchemy engine and binds it to the course database.
engine = create_engine('sqlite:///rutgerscourses.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
# Creates database session so that data can be manipulated.
session = DBSession()

# Begins iteration over every subject that was imported from the text file.
for sub in range(0,999):

	# print "Subject: %s" % sub

	if sub < 10 :
		strSub = '00' + str(sub)
	elif sub < 100 :
		strSub = '0' + str(sub)
	else :
		strSub = str(sub)

	# Generates the url from the Developers API Key and the current subject
	url = 'http://sis.rutgers.edu/soc/courses.json?subject=' + strSub + '&semester=12017&campus=NB&level=U'
	#url = 'http://sauron.rutgers.edu/~rfranknj/soc/api.php?key=' + apiKey + '&semester=92016&subj=' + strSub + '&campus=NB&level=U'

	# Pulls the json associated with the current subject from the Rutgers Server.
	with contextlib.closing(urllib.urlopen(url)) as response:
		allCourses = json.load(response)

	# Begins iteration over every course that was in the course json Array.
	for course in allCourses:

		#print "\tCourse: %s" % course

		# Gets the array of sections for the current course.
		sections = course['sections']

		# Exits the course loop in case the json for some reason contains no sections.
		if sections == 0:
			break

		# Begin iteration over every section in the  section json Array.
		for section in sections:


			# Gets the unique index for the current subject
			INDEX = section['index']

			# print "\t\tSection: %s" % INDEX

			# Looks for the section associated with the current INDEX in the database
			# return to one with exceptions?
			currentSection = session.query(Sections).filter_by(index = INDEX).first()

			if(currentSection == None) :
				break;

			# Gets the current Open Status of the current section
			# print sub + ":" + course + ":" + section
			isOpen = (currentSection.open_status == 1)

			# Determines if the JSON(New Data) and Database(Potentially Old Data) are the same.
			# If they vary the Database data is overwritten with the JSON Data
			needsUpdate = (isOpen != section['openStatus'])
			isOpen = section['openStatus']

			if needsUpdate:

				# Updates the current section data
				currentSection.open_status = isOpen

				#print course['subject'] + ':' + currentSection.course_number + ':' + currentSection.number + ' Index #' + str(INDEX) + " is now: " + ('open' if isOpen else 'closed')

				# Adds the update to the session
				session.add(currentSection)

				# Commits the new Data
				session.commit()

print "Update Succesful!"
