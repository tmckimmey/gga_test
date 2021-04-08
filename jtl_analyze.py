#!/usr/bin/env python3

# Input: list of jtl files
# Ouptut: print out...
#               label, responseCode, responseMessage, failureMessage, time (conv to PST)
#
# Default processes data/Jmeter_log1.jtl and data/Jmeter_log2.jtl and report on the non-200 status
# codes and does so in a CSV (for the supplied test data, responseMessage fields are blank)

# Options allow passing in arbitrary status codes, parameters to display and a pretty print mode
#


import sys
import csv
import datetime
import pytz
import argparse

prog_desc = """
Process jtl files and displays fields for things that don't match success responses.
Default behavior is to report label, responseCode, responseMessage, failureMessage and 
time in PST"""

success_responses = [200]

print_fields = ["label", "responseCode", "responseMessage", "failureMessage"]

parser = argparse.ArgumentParser(description=prog_desc)
parser.add_argument('files', type=str, metavar="file", nargs='*',
                    default=["data/Jmeter_log1.jtl", "data/Jmeter_log2.jtl"])
parser.add_argument('-p', '--pretty-print', default=False, action='store_true', help="Pretty Print")
parser.add_argument('--print-fields', type=str, metavar="field", nargs='*', default=print_fields)
parser.add_argument('--accept-codes', type=int, metavar="result codes", nargs='*', default=success_responses)
args = parser.parse_args()

for file in args.files:
    try:
        with open(file, "r") as f:
            reader = csv.reader(f, delimiter=',')

            # look at row 0, this should be our header row -- if we
            # don't have a header row, we're a bit out of luck as to
            # where the various fields will be
            header_row = next(reader)
            offset_timestamp = header_row.index("timeStamp")
            offset_response_code = header_row.index("responseCode")

            # based on the supplied or default list of columns, let's obtain their
            # offsets from the header file. Just in case anyone switches the log format
            # we
            try:
                offsets = {field: header_row.index(field) for field in args.print_fields}
            except ValueError as e:
                print(f"Unable to find field in header: {e}", file=sys.stderr)
                sys.exit(1)

            # limit out output to just those that we don't consider 'good'
            error_responses = [
                row for row in reader
                if int(row[offset_response_code]) not in args.accept_codes]

            for x in error_responses:

                # timezone conversion handling.
                timestamp = datetime.datetime.fromtimestamp(int(x[offset_timestamp]) / 1000.0)
                timestamp = timestamp.astimezone(pytz.timezone('America/Los_Angeles'))
                timestamp_string = timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")

                # establish a list of fields and their keys in case we pretty print
                limited_fields = [
                    (y, x[offsets[y]]) for y in args.print_fields
                ]

                # spec requested the timestamp be last in this
                limited_fields.append(("timeStamp", timestamp_string))

                if not args.pretty_print:
                    # csv, blanks accounted for
                    print(",".join([el[1] for el in limited_fields]))
                else:
                    # human-readable, more or less
                    for field in limited_fields:
                        print(f"{field[0]:25}: {field[1]}")
                    print()

    except IOError as e:
        print(f"ERROR: Unable to open file {file}", file=sys.stderr)
