# PYTHON EXERCISES

## Summary

For exercise 1 and 2, run python3 main.py

For exercise 3, run jtl_anayzle.py

## Exercise 1
Create a python method that takes arguments int X and int Y,
and updates DEPART and RETURN fields
in test_payload1.xml:

- DEPART gets set to X days in the future from the current date
(whatever the current date is at the moment of executing the code)
- RETURN gets set to Y days in the future from the current date

### Solution

quote_request/quote_request.py

QuoteRequest.set_depart_and_return(x: int, y: int)

Returns a string with the necessary replacements made in-line and returned as a 
string. Sample implementation call, output==filename to overwite input file, None
for stdout or any arbitrary filename for output :

Example Use:

date_setter(filename, depart_delta, return_delta, output=None)

## Exercise 2
Create a python method that takes a json element as an argument, and removes that element from test_payload.json 
(e.g. "statecode" element ).

### Solution
json_object/json_object.py

JsonObject.remove_element(self, element)

Removes the elements from the data in place for the element. Returns the string 
representation of the data.

This assumes that there can be multiple instances of that tag in the 
json object in various sublevels. This will attempt to nuke all instances of 
that specific element.

Example Use:

json_object_element_remove(filename, element, output=None)

If output and filename are identical, the file is overwritten with the new value.

## Exercise 3
Create a python script that parses jmeter log files,
and in the case if there are any non-successful endpoint responses recorded in the log,
prints out the label, response code, response message, failure message,
and the time of non-200 response in human-readable format in PST timezone

### Solution

jtl_analyze.py

jtl_analyze.py -h for options

Some nods made toward continuing to behave if the underlying file changes and options to 
corral the dataset a bit without having to touch code

The pretty print was added because I had convinced myself something was terribly wrong 
when all of the responseMessage fields turned up blank. It doesn't use this option by default.