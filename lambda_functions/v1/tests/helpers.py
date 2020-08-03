import json
from os.path import join, dirname


def load_data(filename, as_json=True):
    relative_path = join("test_data", filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as data_file:
        if as_json:
            return data_file.read()
        else:
            return json.loads(data_file.read())
