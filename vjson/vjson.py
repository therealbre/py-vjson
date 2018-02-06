import re
import sys
import json
import shlex

try:
    unicode = unicode
except NameError:
    unicode = str


"""
    Loads our variables json (with validation)
"""
def load_variables(fname):
    with open(fname, "r") as f:
        vars = json.load(f)
        
    for key,value in vars.iteritems():
        if " " in key:
            raise ValueError("Variables cannot contain spaces")
            
        # Need to undo any escaping we did from loading here to
        # prepare for our replacing in the vjson file            
        if isinstance(value, (list, dict)):
            vars[key] = json.loads(json.dumps(value).replace('\\', '\\\\'))
        else:
            vars[key] = value.replace('\\', '\\\\')
        
    return vars


"""
    Variables should be referenced as follows:
        {{ $.variable }}
        
    e.g. Sample json:
        {
            "key": "{{ $.variable }}"
        }
"""
def make_var_string(var):
    return "{{{{ $.{0} }}}}".format(var)
    
    
"""
    Gets all of the variable references in a data set based on
    the following syntax:
        {{ $.variable }}
"""
def get_variables(data):
    expr = re.compile(r'{{\s?\$\.([a-z0-9_.]+)\s?}}', flags=re.IGNORECASE)
    return set(expr.findall(data))
    
  
"""
    Grabs the value from our dictionary given a key. Additionally,
    it will look for nested keys by splitting on the dot(.) char.
    
        e.g. data = {
            "parent" : {
                "subkey": "value"
            }
        }
        
        Use "parent.subkey" to access data["parent"]["subkey"]
"""
def get_value(data, key, default=None):
    if key in data:
        return data.get(key)
    elif '.' in key:
        key, subkey = key.split('.', 1)
        return get_value(data.get(key, {}), subkey)
        
    return default
    
  
"""
    Used to resolve a variable in the dictionary (supports nested vars)
"""
def resolve(var, variables, default=None):
    value = get_value(data=variables, key=var, default=None)
    
    if value is None:
        return default
        
    if isinstance(value, (list, dict,)):
        return json.dumps(value)
    else:
        return "{0}".format(value)
    
  
"""
    Loads json from a string (will look for a #variable declaration if
    variables are not passed as a optional python dictionary)
"""
def loads_vjson(data, variables=None, **kwargs):
    # Split to try to find our variable declaration
    data = data.split("\n")
    
    if data[0].startswith("#variables"):            
        # Get all of our variable filenames
        var_files = shlex.split(data[0])[1:]
        
        # variables
        variables = {}
        for var_fname in var_files:
            variables.update(load_variables(var_fname.strip('"').strip(' ')))
        data = data[1:]

    data = "".join(data)

    if variables:
        ref_vars = get_variables(data)
        
        for v in ref_vars:
            try:
                data = data.replace(make_var_string(v), resolve(v, variables))
            except KeyError:
                raise KeyError("Undeclared variable referenced in file: {0}".format(v))
                
    return json.loads(data, **kwargs)
  
"""
    Loads a json file which can include variables
"""
def load_vjson(fptr, **kwargs):
    if isinstance(fptr, (str, unicode)):
        with open(fptr, "r") as f:
            data = f.read()
    else:
        data = fptr.read()

    return loads_vjson(data, **kwargs)