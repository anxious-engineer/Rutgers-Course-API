from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sys

# Creates a declarative_base object
Base = declarative_base()

# Courses Class
# Stores information about courses
class Courses(Base):

	__tablename__ = 'Courses'

	subject_notes = Column(String)
	
	prereq_notes = Column(String)

	campus_code = Column(String, nullable = False)

	subject = Column(String, nullable = False)

	course_number = Column(String, nullable = False)

	open_sections = Column(String, nullable = False)

	# Only unique data point for individual courses
	title = Column(String, nullable = False, primary_key = True)
	
	credits = Column(String)
	
	# All course Sections can be accesed via their index in the Sections table

# Sections Class
# Stores information about course sections
class Sections(Base):
	__tablename__ = 'Sections'
	
	exam_code = Column(String)
	
	number = Column(String, nullable = False)
	
	course_number = Column(String, nullable = False)
	
	open_status = Column(Integer, nullable = False) #0 for False | 1 for True
	
	# Associates each section with it's respective Course
	course_title = Column(String, ForeignKey('Courses.title'), nullable = False)
	
	# Every section has a unique registration index number
	index = Column(String, nullable = False, primary_key = True)
	
	courses = relationship(Courses)
	
	# Section meeting times can be accesed via their section_id in the meetingTimes table

# Meeting Times Class
# Stores information about section meeting times
class MeetingTimes(Base):
	__tablename__ = "Meeting_Times"
	
	campus_location_id = Column(Integer)
	
	campus_abrv = Column(String)
	
	building_code = Column(String)
	
	room = Column(Integer)
	
	meeting_mode = Column(String)
	
	meeting_day = Column(String)
	
	pm_code = Column(String)
	
	start_time = Column(String)
	
	end_time = Column(String)
	
	# Associates each Meeting Times with it's respective Section
	section_index = Column(Integer, ForeignKey('Sections.index'))
	
	# Associates each Meeting Time with it's respective Course
	course_title = Column(String, ForeignKey ('Courses.title'))
	
	# Auto generated unique numeric id
	time_id = Column(Integer, nullable = False, primary_key = True)
	
	sections = relationship(Sections)

# Creates SQL engine and binds it to a new database
engine = create_engine('sqlite:///rutgerscourses.db')

# Creates new database
Base.metadata.create_all(engine)