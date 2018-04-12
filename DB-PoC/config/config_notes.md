# 'config.json' Notes

- Collection Name *Required*
  - Parent Keys (Location of key inside nested SOC JSON)
    - *Key is only present if they are required*
    - *Absent Key is equivalent to 'parent_keys : None'*
    - *In order they will be counter in tree/dict*
  - Keys (SOC -> New API) *SHOULD NEVER BE NONE*
    - *Value is only present if they are required*
    - *Absent Value is equivalent to '"new_key" : None,"value_mappings" : None'*
      - Name (Data Name inside SOC JSON)
      - Key Mod Method (Method name that properly formats key data)
      - Mapping (New Mapped Name of Data)
        - *Key is only present if they are required*
        - *Absent Key is equivalent to 'value_mappings : None'*
      - Augmented Keys (Additional names for this key)
        - Name
        - Query Type <See Query Types>
      - Query Type (Data Type used for querying) <See Query Types>
