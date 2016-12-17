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

# # Reads sensative Developer Information from the DeveloperInfo.txt file.
# with open('DeveloperInfo.txt') as DevFile:
# 	devInfo = DevFile.readlines()
#
# # Gets the developers Rutgers API Key.
# apiKey = str(devInfo[0])[9:]

# Begins iteration over every subject that was imported from the text file.
for sub in subjects:

	# Prints the current subject whose data is being pulled.
	print sub[:3]

	# Generates the url from the Developers API Key and the current subject
	url = 'http://sis.rutgers.edu/soc/courses.json?subject=' + sub[:3] + '&semester=12017&campus=NB&level=U'

	# print url

	# Pulls the json associated with the current subject from the Rutgers Server.
	with contextlib.closing(urllib.urlopen(url)) as response:
		allCourses = json.load(response)

	# Creates a list of the imported courses for the current subject
	# This is done beacuse for some reason some courses are list in
	# two seperate arrays in the json.
	importedCourses = []

	# Begins iteration over every course that was in the course json Array.
	for course in allCourses:

		# Stores the current course numerical identifier
		COURSE_NUMBER = course['courseNumber']

		# Generates a unique course title.
		# Note: the subject and course numbers were added to the end
		# because several subjects have courses with the same name.
		# For example Independent Study is a course listed in both
		# the Computer Science and Mathematics subjects.
		TITLE = (course['title'] + ' (' + course['subject'] + ':' + COURSE_NUMBER + ')')

		# print '\t' + COURSE_NUMBER + " : " + TITLE

		# Makes sure that the current course has not already been created
		if COURSE_NUMBER not in importedCourses:

			#print '\t\t%s' % (COURSE_NUMBER not in importedCourses)

			# Adds the current course to the list of imported courses
			importedCourses.append(COURSE_NUMBER)

			# Creates a new course to for the database
			newCourse = Courses(campus_code = course['campusCode'], subject = course['subject'], course_number = COURSE_NUMBER, title = TITLE, subject_notes = course['subjectNotes'], open_sections = course['openSections'], credits = course['credits'])

			# Adds it to the session to be commited
			session.add(newCourse)
			#session.commit()

		# Gets the array of sections for the current course.
		sections = course['sections']

		# Exits the course loop in case the json for some reason contains no sections.
		if sections == 0:
			break

		# Begins iteration over every section that was in the sections json Array.
		for section in sections:

			# Gets the unique index for the current subject
			INDEX = section['index']

			# Creates a new section to for the database
			newSection = Sections(number = section['number'], course_number = course['courseNumber'], open_status = ('1' if (section['openStatus']) else '0'), index = INDEX, exam_code = section['examCode'], course_title = TITLE, courses = newCourse)

			# Adds it to the session to be commited
			session.add(newSection)
			#session.commit()

			# Gets the array of Meeting Times for the current section.
			meetingTimes = section['meetingTimes']

			# Begins iteration over every Meeting Time that was in the meetingTimes json Array.
			for time in meetingTimes:

				# Because Rutgers stores it's meeting times in the 12 hours AM PM format,
				# the following If Else statement converts all meetingTimes to the 24 hour
				# military format to make time representation simpiler

				# Makes sure that the meetingTime has a stored time, so meetingTimes are
				# listed with empty times.
				if(time['startTime'] != None):

					# Determines the whether the meeting times are AM or PM
					if(time['pmCode'] == 'P'):

						# If PM, all times under 1200 are increased by 1200, so 12:00 PM becomes
						# 1200 and 3:00 PM becomes 1500
						START_TIME = str(int(time['startTime']) + 1200)  if (int(time['startTime']) < 1200) else time['startTime']
						END_TIME = str(int(time['endTime']) + 1200) if (int(time['endTime']) < 1200) else time['endTime']

					else:

						# If AM, the start time is imported without modification, but the if the endTime
						# is less than the start time, the end time is increased by 1200. So if a course
						# is listed as AM, but it ends in the PM, the 24 hr time format is still preserved.
						# For example is a course starts at 11:30 AM, but ends at 1:30 PM, then 0130, must
						# be converted to 1330
						START_TIME = time['startTime']
						END_TIME = (int(time['endTime']) + 1200) if (int(time['endTime']) < int(time['startTime'])) else time['endTime']

				else:

					# Ensures that null times are still imported
					START_TIME = time['startTime']
					END_TIME = time['endTime']

				# Creates a new meeting time to for the database
				newMeetingTime = MeetingTimes(campus_location_id = time['campusLocation'], campus_abrv = time['campusAbbrev'], building_code = time['buildingCode'], room = time['roomNumber'], meeting_day = time['meetingDay'], pm_code = time['pmCode'], start_time = START_TIME, end_time = END_TIME, section_index = INDEX, course_title = TITLE, sections = newSection)

				# Adds it to the session to be commited
				session.add(newMeetingTime)
				#session.commit()

	#Commits all new imported data
	try:
		session.commit()
	except Exception as ex:
		session.rollback()
		print ex.__class__
