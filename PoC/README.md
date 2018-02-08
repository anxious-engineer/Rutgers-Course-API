# Rutgers Course API - Proof of Concept

The first step of my work on this project is to complete a very rough proof of concept for the API. This will allow me to get a basic understanding of the technologies I'll be using and get some exposure to some of the intricacies that I may face.

__Goal__ : Recreate current SOC API, with a server-less architecture.

*Step 1* - Create Backend DB

*Step 2* - Load SOC API JSON's into DB

*Step 3* - Write Lambda Logic to query Backend DB

*Step 4* - Create API Gateway routes.

*Step 5* - Link Lambda Logic to API Gateway in Dev

*Step 6* - Correctly Configure API to avoid COORS issue.

*Step 7* - Deploy PoC to production.

## Dependencies

- Python 3
- Boto3 (AWS SDK for Python)
- PyMongo


## MongoDB

PoC Collection Documents:
```json
{
  "subject" : 198,
  "semester" : 12018,
  "campus" : "NB",
  "level" : "UG",
  "data" : {}
}
```
