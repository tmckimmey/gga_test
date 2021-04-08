from quote_request import date_setter
from json_object import JsonObject, json_object_element_remove

if __name__ == '__main__':
    date_setter('data/test_payload1.xml', 5, 7)
    json_object_element_remove("data/test_payload.json", "statecode")
