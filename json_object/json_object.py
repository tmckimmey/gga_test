from typing import Union

import json




class JsonObject(object):
    def __init__(self, data: Union[str, dict]):
        self.data = data if type(data) is dict else json.loads(data)

    @staticmethod
    def find_and_remove_all_elements(data, element_name):

        if type(data) is dict:
            if element_name in data:
                del data[element_name]
            for key in data.keys():
                JsonObject.find_and_remove_all_elements(data[key], element_name)
        if type(data) is list:
            for item in data:
                JsonObject.find_and_remove_all_elements(item, element_name)

    def remove_element(self, element):
        JsonObject.find_and_remove_all_elements(self.data, element)
        return self.tostring()

    def tostring(self):
        return json.dumps(self.data, indent=2)


def json_object_element_remove(filename, element, output=None):
    """

    :param filename: input filename
    :param element:  element to remove
    :param output:   Output filename, or None to print
    :return: None
    """

    jobject = JsonObject(open(filename).read())
    out_str = jobject.remove_element(element)

    if not output:
        print(out_str)
    else:
        with open(output, "w") as f:
            f.write(out_str)
