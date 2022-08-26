from collections import namedtuple
from datetime import datetime
from datetime import timezone as tz
from pytz import timezone

import csv
import os

def return_jmeter_failures(file_name):
    with open(os.path.join('resources',
                           file_name), newline="\n") as infile:
        reader = csv.reader(infile)
        Data = namedtuple("Data", next(reader))
        failure_color = "\x1b[7;33;41m"# get names from column headers
        print("{}Failures grouped by labels are: \n".format(failure_color))
        [print('{lb}: \n'
               '  response code: {rc} \n'
               '  response message: {rm} \n'
               '  failure: message{fm} \n'
               '  time: {ts}\n'.format(lb=data.label,
                                   rc=data.responseCode,
                                   rm=data.responseMessage,
                                   fm=data.failureMessage,
                                   ts=str(datetime.fromtimestamp(int(data.timeStamp)/1000)
                                          .replace(tzinfo=tz.utc).astimezone(timezone("US/Pacific"))
                                          .strftime("%Y-%m-%d %H:%M:%S PST"))))
         for data in map(Data._make, reader) if data.responseCode != '200']
color = "\x1b[1;33;40m"
file_name = input("{}Please enter the jmeter jtl file name with the csv content(Extension should be included): ".format(color))
return_jmeter_failures(file_name)