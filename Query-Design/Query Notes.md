**Query Params**
  - Endpoint/Collection
  - Query Type
    - Find a special way to encode
    - "Like" by Default
    - Numeric Slicing for gt lt, ranges
      - 3: -> greater then 3
      - :3 -> less then 3
      - 1:3 -> 1 to 3
  - Target Properties
  - Values
  - Encode Expansion (Disabled by Default)


```JSON
{
  "Endpoint" : "Course",
  "params" : {
    "credits" : "3",
    "title" : "intro"
  }
}
```

This should query the course collection for documents with 3 credits and intro in the title.
