# Rutgers Course API - Database Proof of Concept

The second step of my work on this project is to complete a very rough proof of concept similar to the original PoC but this time to...prove....the concept....of the Database Design that is in the works.

__Goal__ : Create API with 3 endpoints: Course, Professor, & Campus

*Step 1* -

*Step 2* -

*Step 3* -


## Schema
**Course**
```JSON
{
  "__professor__" : [],
  "__campus__" : [],
  "__subject__" : "",
  "number" : "",
  "synopsisUrl" : "",
  "title" : "",
  "description" : "",
  "preReqNotes" : "",
  "credits" : "",
  "notes" : "",
  "expandedTitle" : "",
}
```
**Professor**
```JSON
{
  "__course__" : [],
  "__campus__" : [],
  "__subject__" : [],
  "name" : "",
}
```
**Campus**
```JSON
{
  "__course__" : [],
  "__professor__" : [],
  "__subject__" : [],
  "name" : "",
  "code" : "",
}
```
**Subject**
```JSON
{
  "__course__" : [],
  "__professor__" : [],
  "__campus__" : [],
  "number" : "",
  "code" : "",
}
```
