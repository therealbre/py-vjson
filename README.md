# py-vjson
Load json with a variable template.

## Install
Download the repository and run the setup.py.

```SHELL
> python setup.py install
```

## Usage
vjson was implemented to work interchangably with json. The common load(s)/dump(s) functions are all supported.

Sample Usage:

```PYTHON
import vjson
with open("data.json", "r") as f:
  data = vjson.load(f)
  
print(vjson.dumps(data, indent=4))
```

### Variables File

A variables file is a json file used to describe the relationship between variable names and values. The key's within the variable file's json are used to specify the name of the variables. Variables will be referenced in the data file using the syntax `{{ $.var_name }}`. Nesting variable names within the json is acceptable and is accessed by dot-joining the variable names on access such as `{{ $parent.child_var }}`.

Sample syntax for the variables file (Seen as `/var/data/variables.json` in main json example below):

```JSON
{
  "var_name": "var_value",
  "var_list": [
    1, 2, 3
  ],
  "var_dict": {
    "var_dict_key": "var_dict_value"
  },
  "parent": {
    "child_var": "child_value"
  }
}
```

### Data File

A vjson file should specify 1 or more variable files to include at the start of the file using the declaration `#variables [path]` (see example below). The `#variables` declaration uses shlex parsing to find all variable files. Multiple files may be specified with space separation between them.

To use a variable, the json should reference the variables using the syntax `{{ $.var_name }}`. The data file will replace any references to the variable with the value specified in the variables file. Nested variable names can be accessed by dot-joining the variable names on access such as `{{ $var_name.nested_var }}`.

Sample syntax for the main json file:

```
#variables "/var/data/variables.json"
{
  "my_key": "{{ $.var_name }},
  "nested": "{{ $.parent.child_value }}",
  "list": {{ $.var_list }},
  "dictionary": {{ $.var_dict }}
}
```
