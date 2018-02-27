# Meeting 5

## Concerns

**rusoc Python Module**
Wrote a helper python module that has various utilities for interacting with the current SOC API
  - Useful for this project and anyone interacting with the old api via python.
  - Directly Interacts with the API, so the user just asks for the JSON they want without having to do any web requesting themselves
  - Current API attempts to collect a url 10 times before giving up.


**Data Collection**
  - Issue with some urls failing, when they have valid data
  - Some urls with return empty JSONs, to the script, may have to do with hitting the endpoint so much
  - Need to come up with a way later on to address this:
    - Add Empty JSONs to a second list to attempt collection again

Collection is incredibly slow at the current rate, with the API sleeping to attempt Endpoint Again

  - Still need to Handle Duplicates
  - Consider Splitting Professors Names, **only add last name**

111
  - Methods on Exam
  - Atom Development Environment
  - Java Box

## Meeting Notes
