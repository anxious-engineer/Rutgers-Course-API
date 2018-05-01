# Rutgers Course API

## Introduction

The **Rutgers Course API** is an attempt to create a server-less and developer friendly version of the Rutgers Schedule of Classes (SOC) API.

There currently exists one API for accessing Rutgers University Schedule of Classes (SOC) Data. This API is not easy to find, is undocumented, and provides only one endpoint.

The currently SOC API does not provide allow for any querying and the data returned contains lots of empty fields, in general is not the easiest to understand, and is some cases unnecessarily duplicates information.

Link to current SOC API Endpoint which provides data for Spring 2018 Undergraduate CS Courses: http://sis.rutgers.edu/oldsoc/courses.json?subject=198&semester=12018&campus=NB&level=UG

This makes it very difficult for Developers to find, understand, and use this API, and provides a tremendous barrier to anyone who wants to use this information to create a program or tool for themselves or for the University.

The aim of my project (currently named the Rutgers Course API), is to overcome all of these issues by providing a publicly available, well documented, and rich versions of the SOC API.

## Development Stages

### Design

### PoC

The first step of my work on this project was to complete a very rough proof of concept for the API. This allowed me to get a basic understanding of the technologies I wanted to use.

Below is a break down of the steps taken to complete this stage:

__Goal__ : Recreate current SOC API, with a server-less architecture.

*Step 1* - Create Backend DB

*Step 2* - Load SOC API JSON's into DB

*Step 3* - Write Lambda Logic to query Backend DB

*Step 4* - Create API Gateway routes.

*Step 5* - Link Lambda Logic to API Gateway in Dev

*Step 6* - Correctly Configure API to avoid COORS issue.

*Step 7* - Deploy PoC to production.

As of writing this, the endpoint for this PoC API that pushes the same functionality as the current SOC API, exists at the following url:

https://7cpgmnapaf.execute-api.us-east-1.amazonaws.com/PoC?subject=198&semester=12018&campus=NB&level=UG

With the basic proof of concept completed with the use of the desired technologies, the next step was to design the new database.

All work and source code for this stage can be found in the `Database-Design/` directory.

## Database Design

The next step was to design the structure of the back-end database that the new API will query from.

The intent of the API is to allow querying on all collections of data (Professors, Courses, Campuses, Times, etc) while exposing/providing the rest of the data linked to the results of that search.

For example if a user wants to find all 4 credit courses, that user will probably want to see the professors that teach those courses and the campuses where those courses are offered.

But, we want to achieve this accessibility of data without creating lots of duplicates. So in order to achieve this goal we will break all course data into related collections and provide database level links to the related data in other collections.

So at the database level in the **Course** collection: credits, description, title, number are stored as fields, while object id's for the documents that hold the names of the professors for the corresponding courses are stored in \_\_reference\_\_ fields.

This means that this related data is not directly accessible and therefore doesn't need to be stored in multiple locations in the database. Instead if related data needs to be accessed the unique object id can be used to find the record and "expand" the data if the user requests it in their query results. 

## DB-PoC


## Query-Dsign
