from vjson import *
import json


"""
    Load from file pointer or file name
"""
def load(fptr, **kwargs):
    return load_vjson(fptr, **kwargs)

    
"""
    Load from string of data. Specify variables using a
    python dictionary and the kwarg "variables".
"""
def loads(data, **kwargs):
    return loads_vjson(data, **kwargs)
    

"""
    Invokes the json library dump
"""
def dump(data, fptr, **kwargs):
    return json.dump(data, fptr, **kwargs)
    
    
"""
    Invokes the json library dumps
"""
def dumps(data, **kwargs):
    return json.dumps(data, **kwargs)