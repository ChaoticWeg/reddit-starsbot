import json

def read(filename, *, default=None):
    try:
        with open(filename, 'r') as infile:
            return json.load(infile)
    except FileNotFoundError:
        return default

def write(obj, filename):
    with open(filename, 'w') as outfile:
        json.dump(obj, outfile)
