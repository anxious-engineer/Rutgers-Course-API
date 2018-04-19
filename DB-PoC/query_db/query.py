import db_connect

def query(coll_name, params):
    clean_params = get_sanatization_method(coll_name)(params)
    coll = db_connect.get_test_db()[coll_name]
    print("FINAL PARAMS:")
    print(clean_params)
    res = coll.find(clean_params)
    return res

# Find query method in the hooks module
def get_sanatization_method(name):
    name = "sanatize_" + name
    if name in globals().keys():
        return globals()[name]
    else:
        return sanatize_default

def sanatize_default(params):
    # Santization
    new_params = {}
    for k in params.keys():
        new_params[k] = {"$regex" : params[k], "$options" : 'i'}
    return new_params

def sanatize_string():
    pass
