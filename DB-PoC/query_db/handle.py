# Find query method in the hooks module
def get_handle_method(key):
    name = "handle_" + str(key)
    if name in globals().keys():
        return globals()[name]
    else:
        return handle_default

def handle_default(data):
    return {"$regex" : data, "$options" : 'i'}

def handle_number(data):
    pass

def handle_string(data):
    pass

def handle_paragraph(data):
    pass
