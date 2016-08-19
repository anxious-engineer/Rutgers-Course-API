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

# Reads the list of subject names and numbers from the Subjects.txt file.
with open('Subjects.txt') as sf:
	subjects = sf.readlines()

# Reads sensative Developer Information from the DeveloperInfo.txt file.
with open('DeveloperInfo.txt') as DevFile:
	devInfo = DevFile.readlines()

# Gets the developers Rutgers API Key.
apiKey = str(devInfo[0])[9:]

# Begins iteration over every subject that was imported from the text file.
for sub in subjects:

	# Generates the url from the Developers API Key and the current subject
	url = 'http://sauron.rutgers.edu/~rfranknj/soc/api.php?key=' + apiKey + '&semester=92016&subj=' + sub[:3] + '&campus=NB&level=U'
	
	# Pulls the json associated with the current subject from the Rutgers Server.
	with contextlib.closing(urllib.urlopen(url)) as response:
		allCourses = json.load(response)
	
	# Begins iteration over every course that was in the course json Array.
	for course in allCourses:
		
		# Gets the array of sections for the current course.
		sections = course['sections']
		
		# Exits the course loop in case the json for some reason contains no sections.
		if sections == 0:
			break
		
		# Begin iteration over every section in the  section json Array.
		for section in sections:
		
			# Gets the unique index for the current subject
			INDEX = section['index']
			
			# Looks for the section associated with the current INDEX in the database
			currentSection = session.query(Sections).filter_by(index = INDEX).one()
			
			# Gets the current Open Status of the current section
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