# Meeting 8

## Updates

Attempted to write threaded db_creation
> It worked
But the lengthy execution time comes from the updates on a single doc at a time
Which in the current parser is unavoidable, and might not be that bad of a fix

./create_db -n <name> -t
>-t flag
runs threaded version

Mongo Will be really nice for querying.

Just need to define a query structure.

Similar to the JSON designed for the parser.

Might add more fields to the current JSON, to provide context for the query handler

Parser and Query Handler, will only be dependent upon the single JSON.

All updates to the single JSON will be reflected immediately.

May need to define query structure once a day with DB creation.

**Query CLI**
Started basic query builder via CLI

Works for DB-PoC collections, will be the basis of the query handler, but currently serves as a Query PoC

## Future

Define Query Structure - *Medium Difficulty*

Implement Query Structure - *Easy Difficulty*

Implement Endpoints (AWS) - *Medium Difficulty*

Implement full API - *Easy - Medium Difficulty*
  - This should be as easy as updating the single JSON
  - And adding some augmenting methods

Documentation - *Easy Difficulty*
