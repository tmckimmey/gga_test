import re
import datetime
from xml.dom import minidom
import xml.etree.ElementTree as etree


class QuoteRequest(object):

    def __init__(self, filename: str):
        self.filename = filename

    # ideally this would be in a library or separate module
    # Also ideally python's built in libraries would handly pretty printing
    # more elegantly
    @staticmethod
    def fix_pretty_xml(raw: etree.Element) -> str:
        """
        Take an element and return the string representation of the XML sans the
        encoding line and replacing the extra spaces and crs that python's xml
        printing libraries unwittingly inflict on a programmer.

        Based on sample data suggests that the encoding line should/can be removed.
        :param: raw  raw etree element that needs to be converted

        :return: a string representing the tree element
        """
        reparsed = minidom.parseString(etree.tostring(raw, 'utf8'))
        result = reparsed.toprettyxml(indent='  ')
        return re.sub(r' +\n+', '', result).split("\n", 1)[1]

    def set_depart_and_return(self, x: int, y: int) -> str:
        """
        Sets the depart and return date from the the current date when the code
        is executed.

        Since this is a function intended to test an end system, there is no
        validation checking done on depart and return date -- we can construct
        potentially errant xml inputs with this.

        We return the converted string as close to the input as we can. Caller
        is responsible for re-writing the file if desired.

        We can encounter errors from parsing the document -- we'll let those
        propagate up the stack

        :param x: depart date delta
        :param y: return date
        :return:
        """
        tree = etree.parse(self.filename)
        root = tree.getroot()
        today = datetime.datetime.now()

        depart_date = (today + datetime.timedelta(days=x)).strftime("%Y%m%d")
        return_date = (today + datetime.timedelta(days=y)).strftime("%Y%m%d")

        # Look for all DEPART and RETURN elements within each TP if
        # there are multiple of either TP or REQUSTS within the document

        for r in root.findall("REQUEST"):
            for x in r.findall("TP"):
                departs = x.findall("DEPART")
                for y in departs:
                    y.text = depart_date
                returns = x.findall("RETURN")
                for y in returns:
                    y.text = return_date

        return QuoteRequest.fix_pretty_xml(root)


def date_setter(filename, depart_delta, return_delta, output=None):
    """

    :param filename:      input filename
    :param depart_delta:  number of days from today to depart
    :param return_delta:  number of days from today to return
    :param output:        a filename to write to, or, if none, print to the console
                          filename and output can be the same file
    :return: None
    """
    testobj = QuoteRequest(filename)
    newxmlstr = testobj.set_depart_and_return(depart_delta, return_delta)

    if not output:
        print(newxmlstr)
    else:
        with open(output, "w") as f:
            f.write(newxmlstr)