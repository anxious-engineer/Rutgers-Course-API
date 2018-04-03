#!/usr/bin/python3
import sys, os
sys.path.append(os.path.abspath('../'))
from rusoc import api as soc
import db_connect
import json

class Parser(object):
    def __init__(self, db):
        self.db = db

    # Mappings
    '''
    {
        <collection_name_1> : {
            "parent_keys" : [
                "<parent_key_1>",
                "<parent_key_2>",
                "<parent_key_3>",
            ],
            "keys" : {
                <key_name_1> : {
                    "new_key" : <new_key>,
                    "key_mod_method" : <key_mod_method_name_1>,
                    "value_mappings" : {
                        <SOC_val_1> : <NEW_API_val_1>,
                        <SOC_val_2> : <NEW_API_val_2>,
                    },
                    "augmented_keys" : [<augmented_key_1>, <augmented_key_2>],
                },
                <key_name_2> : {
                    "new_key" : <new_key>,
                    "key_mod_method" : <key_mod_method_name_1>,
                    "value_mappings" : {
                        <SOC_val_1> : <NEW_API_val_1>,
                        <SOC_val_2> : <NEW_API_val_2>,
                    },
                    "augmented_keys" : [<augmented_key_1>, <augmented_key_2>],
                },
            },
        },
        ...
    }
    '''
    #   - Collection Name *Required*
    #     - Parent Keys (Location of key inside nested SOC JSON)
    #       *Key is only present if they are required*
    #       *Absent Key is equivalent to 'parent_keys : None'*
    #       *In order they will be counter in tree/dict*
    #     - Keys (SOC -> New API) *SHOULD NEVER BE NONE*
    #       *Value is only present if they are required*
    #       *Absent Value is equivalent to '"new_key" : None,"value_mappings" : None'*
    #         - Name (Data Name inside SOC JSON)
    #         - Key Mod Method (Method name that properly formats key data)
    #         - Mapping (New Mapped Name of Data)
    #          *Key is only present if they are required*
    #           *Absent Key is equivalent to 'value_mappings : None'*
    #         - Augmented Keys (Additional names for this key)

    # NOTE : Keys that have values that are Arrays instead of maps,
    # Will be handled implicitly by the parser, which will test 'isinstance(val, list)'
    collection_mappings = {
        "course" : {
            "keys" : {
                "courseNumber" : {
                    "new_key" : "number",
                },
                "courseNotes" : {
                    "new_key" : "notes",
                },
                "courseDescription" : {
                    "new_key" : "description",
                },
                "synopsisUrl" : None,
                "title" : None,
                "preReqNotes" : None,
                "credits" : None,
                "expandedTitle" : None,
            }
        },
        "subject" : {
            "keys" : {
                "subject" : {
                    "new_key" : "number"
                },
            }
        },
        "professor" : {
            "parent_keys" : ["sections", "instructors"],
            "keys" : {
                "name" : {
                    "new_key" : "name",
                    "key_mod_method" : "get_prof_last_name",
                },
            }
        },
        "campus" : {
            "keys" : {
                "campusCode" : {
                    "new_key" : "name",
                    "value_mappings" : {
                        'NB' : 'New Brunswick',
                        'NK' : 'Newark',
                        'CM' : 'Camden',
                        'OC' : 'Off Campus',
                        'ON' : 'Online'
                    },
                    "augmented_keys" : ["code"]
                },
            },
        }
    }

    # Mod methods
    def get_prof_last_name(key):
        if "," in key:
            return key.split(",")[0]
        return key

    def do_nothing(key):
        return key

    MOD_METHODS = {
        "get_prof_last_name" : get_prof_last_name
    }

    def parse_course_data(self, all_data):
        all_new_course_data = {}
        for name in Parser.collection_mappings:
            all_new_course_data[name] = []

        for course in all_data:
            print(course['courseNumber'])
            local_refs = {}
            for name, c_mapping in Parser.collection_mappings.items():
                local_refs[name] = []
                # Current data we parse is always starts as just the current course json
                current_data = [course]
                # print("\t" + name)
                # Do we need to dive in?
                # Here we adjust current data based on parents
                if c_mapping.get('parent_keys'):
                    for p_key in c_mapping['parent_keys']:
                        # print("\t*%s*" % p_key)
                        tmp_data = []
                        for data in current_data:
                            if isinstance(data[p_key], list):
                                for sub_data in data[p_key]:
                                    tmp_data.append(sub_data)
                            else:
                                tmp_data.append(data[p_key])
                        current_data = list(tmp_data)
                # print(current_data)
                for data in current_data:
                    new_doc = {}
                    for key in c_mapping['keys']:
                        name_update_mapping = c_mapping['keys'].get(key)
                        if name_update_mapping:
                            new_key = key if not name_update_mapping.get('new_key') else name_update_mapping['new_key']
                            output_val = data[key] if not name_update_mapping.get('value_mappings') else name_update_mapping['value_mappings'].get(data[key])
                            output_val = Parser.MOD_METHODS.get(name_update_mapping.get('key_mod_method', "None"), Parser.do_nothing)(output_val)
                            new_doc[new_key] = output_val
                            # print("\t\t %s : %s" % (new_key, output_val))
                            if name_update_mapping.get('augmented_keys'):
                                for augmented_key in name_update_mapping.get('augmented_keys'):
                                    new_doc[augmented_key] = data[key]
                                    # print("\t\t %s : %s" % (augmented_key, data[key]))
                        else:
                            new_doc[key] = data[key]
                            # print("\t\t %s : %s" % (key, data[key]))
                    local_refs[name].append(new_doc)
            self.push_course_data_to_db(local_refs)

    def update_references(self, relatives):
        # print("RELATIVES: %s" % relatives)
        for coll, v in relatives.items():
            # Copy Dict
            refs = relatives.copy()
            # Remove coll
            refs.pop(coll, None)
            if isinstance(v, list):
                for i in v:
                    self.upsert_references(i, coll, refs)
            else:
                self.upsert_references(i, coll, refs)

    def upsert_references(self, d_id, coll, refs):
        doc = self.db[coll].find_one({"_id" : d_id})
        if not doc:
            print('Failure Finding doc in %s in upsert_references : %s' % (coll, d_id))
        self.db[coll].update(
            {"_id" : d_id},
            {"$set" : self.merge_references(refs, doc)}
            )

    def merge_references(self, new_refs, old_doc):
        # print(new_refs)
        # print(old_doc)
        # update new_refs name
        new_db_refs = {}
        for ref_name in new_refs:
            new_db_refs[('__%s__' % ref_name)] = list(new_refs[ref_name])
        output_refs = {}
        for ref_name in new_db_refs:
            output_refs[ref_name] = old_doc.get(ref_name, []) + list(set(new_db_refs.get(ref_name, [])) - set(old_doc.get(ref_name, [])))
        return output_refs

    def push_course_data_to_db(self, local_refs):
        db_refs = {}
        # ('__%s__' % name)
        # print(json.dumps(local_refs, indent=4))
        # Build DB refs
        for coll in local_refs:
            db_refs[coll] = []
            for doc in local_refs[coll]:
                db_refs[coll].append(self.upsert_doc(doc, coll))
        self.update_references(db_refs)
        # print(json.dumps(db_refs, indent=4))

    # Returns object id of document that either already exists or is created
    def upsert_doc(self, doc, coll_name):
        collection = self.db[coll_name]
        tar = collection.count(doc)
        if tar == 0:
            collection.insert(doc)
        tar = collection.find_one(doc)
        return tar["_id"]

# Test Parsing Code
def test_course_parsing():
    # TEST
    client = db_connect.get_client()
    test_db_name = "test"
    if test_db_name in client.database_names():
        client.drop_database(test_db_name)
    db = client[test_db_name]
    # Parser should take a DB object on creation
    p = Parser(db)
    # Then Parse data
    test_data = []
    all_urls = soc.get_all_current_course_urls()
    i = 0
    # Iterate over all urls, and get some clean json data
    # while len(test_data) < 1:
    #     test_data = soc.get_clean_JSON(all_urls[i])
    test_data = soc.get_clean_JSON('http://sis.rutgers.edu/oldsoc/courses.json?subject=198&semester=12018&campus=NB&level=UG')
    # Now we've got come clean data!
    # Parse it!
    # print(test_data)
    p.parse_course_data(test_data)

# Entry to Script for parsing test
def main():
    test_course_parsing()

if __name__ == '__main__':
    main()
