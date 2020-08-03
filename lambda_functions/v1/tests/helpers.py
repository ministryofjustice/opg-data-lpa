import json
from os.path import join, dirname


def is_valid_schema(data, schema_file):
    """ Checks whether the given data matches the schema """
    schema = load_data(schema_file, as_json=False)
    try:
        validate(data, schema)
        result = True
    except exceptions.ValidationError as e:
        print("well-formed but invalid JSON:", e)
        result = False
    except json.decoder.JSONDecodeError as e:
        print("poorly-formed text, not JSON:", e)
        result = False

    return result


def load_data(filename, as_json=True):
    relative_path = join("test_data", filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as data_file:
        if as_json:
            return data_file.read()
        else:
            return json.loads(data_file.read())
